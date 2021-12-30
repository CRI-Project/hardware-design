###################################################################
#                                                                 #                      
#############################ATTENTION#############################
###################################################################
#                                                                 #
# change http://xxx.xxx.xxx.xxx:port to your ip address and port  #
#                                                                 #
###################################################################
import RPi.GPIO as GPIO
import time
import requests
import board
import busio
import adafruit_scd30
import Adafruit_GPIO.SPI as SPI
import signal

SCD30_device = 19
sleep_interval = 6
warm_up = 5
flag  = 0
JSON_MESSAGE_ID = 1

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SCD30_device,GPIO.OUT)
    GPIO.output(SCD30_device,GPIO.HIGH)
    return()

def deviceON():
    print("the device is on")
    GPIO.output(SCD30_device,GPIO.HIGH)
    return()

def deviceOFF():
    print("the device is off")
    GPIO.output(SCD30_device,GPIO.LOW)
    return()

def getRespberrySerial():
    respberry_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6] == 'Serial':
               respberry_serial = line[10:26]
        f.close()
    except:
        respberry_serial = 'ffffffffffffffff'
    return respberry_serial

def sensorInitialization():
        response = requests.post('http://xxx.xxx.xxx.xxx:port//climate/sensor/save', json={
        "id": 1, # change this to your sensor id
        "isopen": 0, 
        "name": "sensor_1"  # change this to your sensor name
    })
    if response.json()['msg'] == 'success':
        print("The sensor has been initialized")
    else:
        print("The sensor has been initialized before.")
        
def getSensorStatus():
    response =requests.get("http://xxx.xxx.xxx.xxx:port//climate/sensor/info/1")
    status = (response.json()['sensor'])['isopen']
    return status
        
def sendData(ppm, temperature, humidity):
    response = requests.post('http://xxx.xxx.xxx.xxx:port//sendSensorDataMessage',json ={
                                 "humidity":humidity,
                                 "ppm":ppm,
                                 "processorCode":"0003",
                                 "latitude":25.2042,
                                 "longitude":113.2030,
                                 "status":"200",
                                 "sensorName":str(getRespberrySerial()),
                                 "temperature":temperature,
                                 "jsonMessageId":JSON_MESSAGE_ID
                                 })
    print("State code:", response.status_code)
    print(response.json())

# this function has not been used.
# def sendTestData(ppm, temperature, humidity):
#     # change http://xxx.xxx.xxx.xxx:port to your ip address and port
#     response = requests.post('http://xxx.xxx.xxx.xxx:port//sendSensorDataTestMessage',json ={
#                                  "humidity":humidity,
#                                  "ppm":ppm,
#                                  "processorCode":"0003",
#                                  "temperature":temperature,
#                                  })
#     print("State code:", response.status_code)
#     print(response.json())

def print_scd_data():
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        sendData(str("%0.2f"% scd.CO2), str("%0.2f"% scd.temperature), str("%0.2f"% scd.relative_humidity))
        sendTestData(str("%0.2f"% scd.CO2), str("%0.2f"% scd.temperature), str("%0.2f"% scd.relative_humidity))
    return()

setup()
sensorInitialization()

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
time.sleep(warm_up)
scd = adafruit_scd30.SCD30(i2c)
# scd.measurement_interval(6)

while True:
    i = get_Position()
    print("condition:" +i)
    print("flag: "+str(flag))
    if i == "1" and flag == "0":
        deviceON()   
        time.sleep(warm_up)
        flag = "1"
    elif i == "1" and flag =="1":
        print_scd_data()
        JSON_MESSAGE_ID += 1
    elif i == "0":
        deviceOFF()
        flag = "0"
    time.sleep(sleep_interval)



