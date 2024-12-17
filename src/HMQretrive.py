import paho.mqtt.client as mqtt


def on_connect(client, userdata, status, flags):
    client.subscribe("MC-Project-Lat")
    client.subscribe("MC-Project-Lng")
    client.subscribe("MC-Project-Sat")

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))


broker_address = "3.88.172.217"
broker_port = 1883


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_forever()



