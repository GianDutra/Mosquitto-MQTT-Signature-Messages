import time
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import assinar

print("Connecting to WiFi", end="")
station = network.WLAN(network.STA_IF)
station.active(True)
print(station.scan())
station.connect('Wokwi-GUEST', '')
while not station.isconnected():
  print(".", end="")
  time.sleep(0.1)

print('Connection successful')
print(station.ifconfig())

assinar = assinar.Assinar('hello')
assinar.start()