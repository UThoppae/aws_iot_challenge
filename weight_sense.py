import ssl
import sys
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

print("Open SSK Version :" + ssl.OPENSSL_VERSION)


def configure():
    myMQTTClient = AWSIoTMQTTClient("PiWeightSense")
    myMQTTClient.configureEndpoint("<unique_id>.iot.us-east-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("/home/pi/kloudiot/aws_iot/root_CA_VeriSign.pem",
                                      "/home/pi/kloudiot/aws_iot/n_virginia_region_<id>.private.key", "/home/pi/kloudiot/aws_iot/n_virginia_region_<id>.cert.pem.crt")
    myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing

    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(2)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(30)
    return myMQTTClient


def connect(myMQTTClient):
    myMQTTClient.connect()
    return myMQTTClient


def subscribe(myMQTTClient, topic, callback):
    myMQTTClient.subscribe(topic, 1, callback)
    return myMQTTClient


def unsubscribe(myMQTTClient, topic):
    myMQTTClient.unsubscribe(topic)
    return myMQTTClient


def sendMessage(myMQTTClient, topic, payload):
    try:
        myMQTTClient.publish(topic, payload, 0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        myMQTTClient.disconnect()
