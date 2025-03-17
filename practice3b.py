import paho.mqtt.client as mqtt

# MQTT-instellingen
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "orangepi/sensors"

# Callbackfunctie wanneer de verbinding is gemaakt
def on_connect(client, userdata, flags, rc):
    print(f"Verbonden met code {rc}")
    # Abonneer je op het topic
    client.subscribe(MQTT_TOPIC)

# Callbackfunctie wanneer er een bericht binnenkomt
def on_message(client, userdata, msg):
    print(f"Bericht ontvangen op {msg.topic}: {msg.payload.decode()}")

# Maak een MQTT-client aan
client = mqtt.Client()

# Stel de callbackfunctie in
client.on_connect = on_connect
client.on_message = on_message

# Verbind met de MQTT-broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start de loop om berichten te ontvangen
client.loop_forever()
