import time 
from umqttsimple import MQTTClient
import ubinascii
import machine
import esp
esp.osdebug(None)
import gc
gc.collect()
from machine import Pin 
import json

class Assinar: 
    #construtor 
    def __init__(self, topico):
        self.led = Pin(27, Pin.OUT)
        self.mqtt_server = 'test.mosquitto.org'
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.topic_sub = topico.encode()

    def msg_cb(self, topic, msg):
        print((topic, msg))
        try:
            message = json.loads(msg.decode())  # Analisa a mensagem JSON
            cmd = message.get("cmd")
            if cmd == "on":
                self.led.on()  # Acende o LED
            elif cmd == "off":
                self.led.off()  # Apaga o LED
        except ValueError as e:
            print("Erro ao analisar a mensagem JSON:", e)

    def connect_and_subscribe(self):
        cliente = MQTTClient(self.client_id, self.mqtt_server)
        cliente.set_callback(self.msg_cb)
        cliente.connect()
        cliente.subscribe(self.topic_sub)
        print('Conectado')
        return cliente

    def restart_and_reconnect(self):
        print("Erro ao conectar")
        time.sleep(10)
        machine.reset()

    def start(self):
        try:
            cliente = self.connect_and_subscribe()
        except OSError as e:
            self.restart_and_reconnect()


        while True:
            try:
                cliente.check_msg()
            except OSError as e:
                self.restart_and_reconnect()