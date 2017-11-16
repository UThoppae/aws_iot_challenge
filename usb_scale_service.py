import usb.core
import usb.util
from weight_sense import *
import time
from random import *


topic = "PiWeightSense/CHI_IL_SCALE_LOC1_001"
myMQTTClient = configure()
previousWeight = 0.0


print("Connecting...")


def test(client, userdata, message):
    print("test...." + str(message.payload))

device = None

try:

    myMQTTClient.connect()
    print("Connected.")
    myMQTTClient.subscribe(topic, 1, test)
    time.sleep(1)
    VENDOR_ID = 0x0922
    PRODUCT_ID = 0x8003
    print("Connected...")

    while True:
        # find the USB device
        if device is None:
            # time.sleep(60*60)
            device = usb.core.find(idVendor=VENDOR_ID,
                                   idProduct=PRODUCT_ID)
            print("Device ::: " + str(device))
            print("-----------")
            reattach = False
            if device and device.is_kernel_driver_active(0):
                reattach = True
                device.detach_kernel_driver(0)

                # use the first/default configuration
                device.set_configuration()
                # first endpoint
                endpoint = device[0][(0, 0)][0]

        if device:

            # read a data packet
            attempts = 10
            data = None
            while data is None and attempts > 0:
                try:
                    data = device.read(endpoint.bEndpointAddress,
                                       endpoint.wMaxPacketSize)
                except usb.core.USBError as e:
                    data = None
                    if e.args == ('Operation timed out',):
                        attempts -= 1
                        continue

                if data:

                    weight = float(data[4] + data[5] * 256)

                    if weight != previousWeight and weight > 0.0:

                        message = "{\"device_id\":\"USB_SCL_001\",\"weight\":\"" + \
                            str(weight) + "\"}"

                        previousWeight = weight

                        myMQTTClient.publish(topic, message, 0)

                        print("Weight : " + str(weight) + " kg")

        else:
            print("No Device Found")

        time.sleep(3)

except:
    print("Unexpected error:", sys.exc_info()[1])
    raise
finally:
    if(myMQTTClient):
        myMQTTClient.disconnect()
