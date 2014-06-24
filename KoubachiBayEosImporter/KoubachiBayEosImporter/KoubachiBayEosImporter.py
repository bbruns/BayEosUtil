
import datetime, time, re, sys, os, logging, logging.config, traceback
import BayEosClient
import KoubachiClient

def main():
    bayEosUri = "dummyBayEosUri"
    bayEosUser = "dummyuser"
    bayEosPwd = "dummypassword"
    koubachiUri = "http://api.koubachi.com/v2/"
    koubachiPwd = "dummyKoubachiPwd"
    koubachiApp = "dummyKoubachiApp"
    koubachiSensorMac = "dummyKoubachiSensorMac"
    bayEosAirTemperatureId = 200528
    bayEosLightEmissionId = 200530
    bayEosSoilMoistureId = 200529
    bayEosBatteryLevelId = 200533
    loggerConfFileName = "koubachiImporter.conf"
    bayEos = None

    status = 0
    baseFolder = "."
    if len(sys.argv) > 1:
        baseFolder = sys.argv[1]

    logging.config.fileConfig(baseFolder + "/" + loggerConfFileName)
    logger = logging.getLogger("root")

    try:
        koubachi = KoubachiClient.KoubachiClient(koubachiUri, koubachiApp, koubachiPwd)
        connectOk = koubachi.checkRightApiVersion()
        if connectOk:
            logging.info("Successfully connected to Koubachi sensor #%s." % (koubachiSensorMac))
        else:
            logging.error("Failed to connect to Koubachi sensor #%s." % (koubachiSensorMac))

        batteryLevelTag = koubachi.getBatteryLevelTag()
        soilMoistureTag = koubachi.getSoilMoistureTag()
        lightEmissionTag = koubachi.getLightEmissionTag()
        temperatureTag = koubachi.getTemperatureTag()
        timeSuffixTag = koubachi.getTimeSuffixTag()

        recentSensorReadings = koubachi.getRecentSensorReadings(koubachiSensorMac)

        bayEos = BayEosClient.BayEosClient(bayEosUri, bayEosUser, bayEosPwd)
        bayEos.connect()
        if bayEos.isConnected:
            logging.info("Successfully connected to '%s'" % (bayEosUri))
        else:
            logging.info("Failed to connect to '%s'" % (bayEosUri))

        temperatureVal = recentSensorReadings[temperatureTag] #in Celsius
        lightEmissionVal = recentSensorReadings[lightEmissionTag] #in Lux
        soilMoistureVal = recentSensorReadings[soilMoistureTag] #in Percent
        batteryLevelVal = recentSensorReadings[batteryLevelTag] #in Percent
        addedTemperature = bayEos.addSingleValue(bayEosAirTemperatureId, recentSensorReadings[temperatureTag+timeSuffixTag], temperatureVal)
        addedLightEmission = bayEos.addSingleValue(bayEosLightEmissionId, recentSensorReadings[lightEmissionTag+timeSuffixTag], lightEmissionVal)
        addedSoilMoisture = bayEos.addSingleValue(bayEosSoilMoistureId, recentSensorReadings[soilMoistureTag+timeSuffixTag], soilMoistureVal)
        addedBatteryLevel = bayEos.addSingleValue(bayEosBatteryLevelId, recentSensorReadings[batteryLevelTag+timeSuffixTag], batteryLevelVal)

        allOk = addedTemperature and addedLightEmission and addedSoilMoisture and addedBatteryLevel
        if allOk:
            logging.info("Successfully imported values for temperature (%d): %f degC, light-emission (%d): %f lux, soil-moisture (%d): %f %%, battery-level (%d): %f %%" % \
                         (bayEosAirTemperatureId, temperatureVal, bayEosLightEmissionId, lightEmissionVal, bayEosSoilMoistureId, soilMoistureVal, bayEosBatteryLevelId, batteryLevelVal))
        else:
            logging.warn("Failed to import at least one sensor value, temperature: %s, light-emission: %s, soil-moisture: %s, battery-level: %s" % (addedTemperature, addedLightEmission, addedSoilMoisture, addedBatteryLevel))

        bayEos.disconnect()
      
        
    except:
        logging.error("exception catched: %s" %(traceback.format_exc()))
        status = 1
        if bayEos is not None:
            if bayEos.isConnected:
                bayEos.disconnect()

    logging.debug("script terminated with ret: %d" % (status))       

if __name__ == "__main__":
    main()  
