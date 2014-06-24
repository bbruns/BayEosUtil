import urllib, urllib2
import json
import datetime, time

class KoubachiClient(object):
    """simple client to reat out values from Koubachi WIFI Plant Sensor"""


    def __init__(self, serverUri = "", appKey = "", secret = ""):
        self.serverUri = serverUri
        self.appKey = appKey
        self.secret = secret
        self.koubachiAuth = urllib.urlencode({'user_credentials': secret, 'app_key': appKey})

    def checkRightApiVersion(self):
        return '{"version":2}'==self.requestResource()

    def requestResource(self, uriPath = ""):
        req = urllib2.Request(self.serverUri + uriPath + "?" + self.koubachiAuth)
        req.add_header('Accept', 'application/json')
        res = urllib2.urlopen(req)

        return res.read()

    """returns dictionary with unique MAC of sensors as key, value is list of associated plant IDs"""
    def getSensorToPlantMapping(self):
        allSensors = self.requestResource("user/smart_devices")
        objAllSensors = json.loads(allSensors)
        sensorMap = {}
        for sensor in objAllSensors:
            sensorMac = sensor[u'device'][u'mac_address']
            plantIds = []
            for plant in sensor[u'device'][u'plants']:
                plantIds.append(plant[u'id'])
            sensorMap[sensorMac] = plantIds
        
        return sensorMap 

    def getAllPlantIds(self):
        allPlants = self.requestResource("plants")
        objAllPlants = json.loads(allPlants)
        plantIds = []
        for plant in objAllPlants:
            plantIds.append(plant[u'plant'][u'id'])

        return plantIds

    def convertTimeStringToDateTime(self, measureTimeStr):
        fac = 1
        if measureTimeStr[20]=='-':
            fac = -1
        intHourOffset=int(measureTimeStr[21:22])*fac
        measureTime = time.strptime(measureTimeStr[0:19], '%Y-%m-%dT%H:%M:%S')
        return datetime.datetime(*measureTime[:6]) - datetime.timedelta(hours=intHourOffset)

    def parseLeadingFloatString(self, floatStr):
        for i in range(0,len(floatStr)):
            if not floatStr[i].isdigit() and not (floatStr[i]==".") and not (floatStr[i]=="-"):
                break

        return float(floatStr[0:i])

    def getBatteryLevelTag(self):
        return "virtual_battery_level"

    def getSoilMoistureTag(self):
        return "relative_soil_moisture"

    def getTemperatureTag(self):
        return "temperature_value"
    
    def getLightEmissionTag(self):
        return "light_emission_value"

    def getTimeSuffixTag(self):
        return "_time"

    """timestamps are in UTC-time, temperature is in Celsius, soil-moisture in %, light emission in lux"""
    def getRecentSensorReadings(self, sensorMac):
        allRecentReadings = self.requestResource("user/smart_devices/" + sensorMac)
        objAllRecentReadings= json.loads(allRecentReadings)
        
        batteryLevelTag = self.getBatteryLevelTag()
        soilMoistureTag = self.getSoilMoistureTag()
        lightEmissionTag = self.getLightEmissionTag()
        temperatureTag = self.getTemperatureTag()
        timeSuffixTag = self.getTimeSuffixTag()

        sensorValuesMap = {}
        sensorValuesMap[batteryLevelTag] = 100.0*objAllRecentReadings[u'device'][u'virtual_battery_level'] #is already a float value
        sensorValuesMap[batteryLevelTag+timeSuffixTag] = self.convertTimeStringToDateTime(objAllRecentReadings[u'device'][u'last_transmission'])
        sensorValuesMap[soilMoistureTag] = self.parseLeadingFloatString(objAllRecentReadings[u'device'][u'recent_soilmoisture_reading_value'])
        sensorValuesMap[soilMoistureTag+timeSuffixTag] = self.convertTimeStringToDateTime(objAllRecentReadings[u'device'][u'recent_soilmoisture_reading_time'])
        sensorValuesMap[temperatureTag] = self.parseLeadingFloatString(objAllRecentReadings[u'device'][u'recent_temperature_reading_value'])
        sensorValuesMap[temperatureTag+timeSuffixTag] = self.convertTimeStringToDateTime(objAllRecentReadings[u'device'][u'recent_temperature_reading_time'])
        sensorValuesMap[lightEmissionTag] = self.parseLeadingFloatString(objAllRecentReadings[u'device'][u'recent_light_reading_value'])
        sensorValuesMap[lightEmissionTag+timeSuffixTag] = self.convertTimeStringToDateTime(objAllRecentReadings[u'device'][u'recent_temperature_reading_time'])

        return sensorValuesMap

