from unidecode import unidecode
from random import randint
from time import sleep
import threading
import requests
import mysql.connector
import json
import uuid
import time
import sys


counter_general = 0
result_txarrak = ''
mydb = ''
mycursor = ''
limitea = ''
airlines= []
vuelos = []
escalas = []

escalasLock = threading.Lock()
vuelosLock = threading.Lock()
airlinesLock = threading.Lock()
uuidLock = threading.Lock()
txarrakLock = threading.Lock()
counterLock= threading.Lock()
insertLock= threading.Lock()


mydb = mysql.connector.connect(
        host="localhost",
        user="amets",
        passwd="",
        database="2019abendua"
    )
mycursor = mydb.cursor()
limitea = int(sys.argv[2]) + 1

with open('apikeys.txt') as f:
    keys = f.readlines()
with open('ida1.json') as f:
    nondikFile = f.readlines()
#    nondikFile.pop(0)
with open('ida.json') as f:
    noraFile = f.readlines()

def addInsert(i,j,k):
    global insertLock, vuelos, escalas, airlines
    insertLock.acquire()
    airlines = airlines + i
    vuelos = vuelos + j
    escalas = escalas + k
    addCounter()
    if getCounter() % 30 == 0:
        sql0 = "INSERT IGNORE INTO airlines (flight_company_code, flight_company_name, link_image) VALUES (%s, %s, %s)"
        insert_airlines(sql0, airlines)
        sql1 = "INSERT INTO vuelos (id, iata_origen, airport_origen, dia_salida, hora_salida, iata_destino, airport_destino, dia_llegada, hora_llegada, duration, n_escalas, flight_company_code, flight_number, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_vuelos(sql1, vuelos)
        sql2 = "INSERT INTO escalas (id, airport_origen, dia_salida, hora_salida, airport_destino, dia_llegada, hora_llegada, flight_company_code, flight_number, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_escalas(sql2, escalas)
        vuelos=[]
        airlines = []
        escalas = []
    insertLock.release()


def insert_vuelos(sql,val):
    mycursor.executemany(sql,val)
    mydb.commit()


def insert_escalas(sql,val):
    mycursor.executemany(sql,val)
    mydb.commit()


def insert_airlines(sql,val):
    mycursor.executemany(sql,val)
    mydb.commit()


def getUuid():
    global uuidLock
    uuidLock.acquire()
    result = int(time.time()*1000000.0)
    uuidLock.release()
    return result


def getCounter():
    global counterLock
    counterLock.acquire()
    global counter_general
    counter = counter_general
    counterLock.release()
    return counter


def addCounter():
    global counterLock
    counterLock.acquire()
    global counter_general
    counter_general = counter_general + 1
    counterLock.release()


class worker(threading.Thread):
    def __init__(self, x,i,y,key):
        threading.Thread.__init__(self)
        self.vuelos_sin_escalas_vuelos = []
        self.vuelos_sin_escalas_airlines = []
        self.vuelos_con_escalas_escalas = []
        self.origen =x
        self.destino = i
        self.key = key
        self.date = y
    def run(self):
        try:
            if (self.origen != self.destino):
                nora = self.origen.replace('\n', '')
                nondik = self.destino.replace('\n', '')
                key = keys[randint(0, 139)].replace('\n', '')
                date = sys.argv[1] + '-' + str(self.date)
                result = self.getData(nondik, nora, date, key)
                if result != "":
                    carriers = json.loads(result)["Carriers"]
                    itineraries = json.loads(result)["Itineraries"]
                    legs = json.loads(result)["Legs"]
                    places = json.loads(result)["Places"]
                    seg = json.loads(result)["Segments"]
                    self.processData(carriers, itineraries, legs, places,seg, nondik, nora)
                    addInsert(self.vuelos_sin_escalas_airlines,self.vuelos_sin_escalas_vuelos,self.vuelos_con_escalas_escalas)
        except Exception as e:
            print(e)

    def getData(self, nondik, nora, date, key):
        response = requests.request("POST",
                                    "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
                                    headers={"X-RapidAPI-Key": key,
                                             "Content-Type": "application/x-www-form-urlencoded"}, data={
                "cabinClass": "economy",
                "children": 0,
                "infants": 0,
                "groupPricing": "false",
                "country": "ES",
                "currency": "EUR",
                "locale": "es-ES",
                "originPlace": nondik + '-sky',
                "destinationPlace": nora + '-sky',
                "outboundDate": date,
                "adults": 1
            })

        if response.status_code != 201:
            #addError(nondik + "/"+ nora + "/" + date)
            newThread = worker(nora,nondik,date.split("-")[2],key)
#            newThread = worker(nondik,nora,date.split("-")[2],key)
            newThread.start()
            print("Error---->"+response.content.decode('utf-8'))
            return ""
            sleep(0.3)
        sleep(15)
        r = response.headers["Location"]
        r = r.split("/")[len(r.split("/")) - 1]
        response = requests.request("GET",
                                    "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/{" + r + "}?sortType=price&sortOrder=asc&pageIndex=0&pageSize=10",
                                    headers={"X-RapidAPI-Key": key})
        return response.content.decode('utf-8')

    def processData(self, carriers, itineraries, legs, places, seg,nondik,nora):
        data = []
        carriers_hiztegia_izena = {}
        carriers_hiztegia_kodea = {}
        carriers_hiztegia_linka = {}
        for c in carriers:
            carriers_hiztegia_izena[str(c["Id"])] = c["Name"]
            carriers_hiztegia_kodea[str(c["Id"])] = c["Code"]
            carriers_hiztegia_linka[str(c["Id"])] = c["ImageUrl"]
        hegaldiak_lista = []
        for i in itineraries:
            vector = []
            lowestPrice = i["PricingOptions"][0]["Price"]
            link = i["PricingOptions"][0]["DeeplinkUrl"]
            destId = ''
            origenId = ''
            salida = ''
            entrada = ''
            precio = ''
            legId = i["OutboundLegId"]
            segmentsIds = []
            for j in legs:
                if legId == j["Id"]:
                    destId = j["DestinationStation"]
                    origenId = j["OriginStation"]
                    hegaldiak_lista.append(j["Duration"])
                    salida = j['Departure']
                    entrada = j['Arrival']
                    segmentsIds = j["SegmentIds"]
            segments = []
            for i in segmentsIds:
                for j in seg:
                    if i == j["Id"]:
                        auxSalida = ''
                        auxEntrada = ''
                        auxDeparture = j["DepartureDateTime"]
                        auxArrival = j["ArrivalDateTime"]
                        auxDuration = j["Duration"]
                        auxCarrier = j["Carrier"]
                        auxFlightNumber = j["FlightNumber"]
                        obj = {}
                        for k in places:
                            if k["Id"] == j["OriginStation"]:
                                auxSalida = k["Name"]
                            if k["Id"] == j["DestinationStation"]:
                                auxEntrada = k["Name"]
                        obj = {"salida": auxSalida, "entrada": auxEntrada, "departure": auxDeparture,
                               "arrival": auxArrival, "duration": auxDuration, "price": lowestPrice, "link": link,
                               "carrier": auxCarrier, "flightnumber": auxFlightNumber}
                        vector.append(obj)
                        break
            data.append(vector)
        cont = 0
        counter = 0
        duraziyua = 0
        counter_hegaldiak = 0
        for i in data:
            if len(i) > 1:
                counter = len(i) - 1
                rnd = getUuid()
                iata_origen = nondik
                dia_salida = i[0]["departure"].split("T")[0]
                hora_salida = i[0]["departure"].split("T")[1]
                airport_salida = unidecode(i[0]["salida"])
                iata_destino = nora
                dia_llegada = i[int(counter)]["arrival"].split("T")[0]
                hora_llegada = i[int(counter)]["arrival"].split("T")[1]
                airport_destino = unidecode(i[int(counter)]["entrada"])
                prezio = str(i[0]["price"])
                escalas = str(len(i) - 1)
                duration_total = str(hegaldiak_lista[counter_hegaldiak])
                link_flight = str(i[0]["link"])
                cont = 1
                val5 = (
                    str(rnd), iata_origen, airport_salida, dia_salida, hora_salida, iata_destino, airport_destino,
                    dia_llegada, hora_llegada, duration_total, escalas, 'XXXXXX', 'XXXXXX', prezio)
                self.vuelos_sin_escalas_vuelos.append(val5)
                for j in range(len(i)):
                    es_airport_origen = unidecode(i[j]["salida"])
                    es_dia_salida = i[j]["departure"].split("T")[0]
                    es_hora_salida = i[j]["departure"].split("T")[1]
                    es_airport_destino = unidecode(i[j]["entrada"])
                    es_dia_llegada = i[j]["arrival"].split("T")[0]
                    es_hora_llegada = i[j]["arrival"].split("T")[1]
                    es_flight_company_code = str(carriers_hiztegia_kodea.get(str(i[j]["carrier"])))
                    es_flight_number = str(i[j]["flightnumber"])
                    es_duration = str(i[j]["duration"])
                    comp_izena = str(carriers_hiztegia_izena.get(str(i[j]["carrier"])))
                    comp_kodea = str(carriers_hiztegia_kodea.get(str(i[j]["carrier"])))
                    comp_linka = str(carriers_hiztegia_linka.get(str(i[j]["carrier"])))
                    val3 = (comp_kodea, comp_izena, comp_linka)
                    val4 = (
                        str(rnd), es_airport_origen, es_dia_salida, es_hora_salida, es_airport_destino, es_dia_llegada,
                        es_hora_llegada, comp_kodea, es_flight_number, es_duration)
                    self.vuelos_sin_escalas_airlines.append(val3)
                    self.vuelos_con_escalas_escalas.append(val4)

            else:
                iata_origen = nondik
                dia_salida = i[0]["departure"].split("T")[0]
                hora_salida = i[0]["departure"].split("T")[1]
                airport_salida = unidecode(i[0]["salida"])
                iata_destino = nora
                rnd = getUuid()
                dia_llegada = i[0]["arrival"].split("T")[0]
                hora_llegada = i[0]["arrival"].split("T")[1]
                airport_destino = unidecode(i[0]["entrada"])
                prezio = str(i[0]["price"])
                escalas = str(len(i) - 1)
                duration_total = str(hegaldiak_lista[counter_hegaldiak])
                duration = str(i[0]["duration"])
                flight_izena = str(carriers_hiztegia_izena.get(str(i[0]["carrier"])))
                flight_kodea = str(carriers_hiztegia_kodea.get(str(i[0]["carrier"])))
                flight_number = str(i[0]["flightnumber"])
                link_flight = str(i[0]["link"])
                link_image = str(carriers_hiztegia_linka.get(str(i[0]["carrier"])))
                val0 = (flight_kodea, flight_izena, link_image)
                val1 = (
                    str(rnd), iata_origen, airport_salida, dia_salida, hora_salida, iata_destino, airport_destino,
                    dia_llegada, hora_llegada, duration_total, escalas, flight_kodea, flight_number, prezio)
                self.vuelos_sin_escalas_airlines.append(val0)
                self.vuelos_sin_escalas_vuelos.append(val1)
            counter_hegaldiak = counter_hegaldiak + 1

if __name__ == "__main__":
    if (len(sys.argv) <= 2):
        print("Sartu hilabetea. Example: \npython script.py 2019-07 2 10 \n 2 lehen eguna eta 22 azkena izanik, bihar barne")
        sys.exit()
    threads = []

    '''t = worker(nondikFile[0],noraFile[1],str(1).zfill(2),keys[23])
    t.start()'''

    cont = 0
    for i in noraFile:
        for x in nondikFile:
            for y in range(1, limitea):
                y = str(y).zfill(2)
                key = keys[cont%139]
                t = worker(x,i,y,key)
                threads.append(t)
                t.start()
#                sleep(0.1375) #lenengo 6 egunak 0.2kin  # 0.1375 ondo diju #0.5ekin ondo dji mysql
                sleep(0.3)
                cont = cont+1