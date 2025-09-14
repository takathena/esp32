import network
import time

# Ganti dengan SSID dan password WiFi kamu
SSID = "gendis"
PASSWORD = "77777777"

# Buat objek WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Mencoba konek ke WiFi...")

# Tunggu sampai terkoneksi
while not wlan.isconnected():
    print("Belum konek, coba lagi...")
    time.sleep(1)

print("Berhasil konek!")
print("IP Address:", wlan.ifconfig()[0])
print("Detail Jaringan:", wlan.ifconfig())  
# (IP, Subnet Mask, Gateway, DNS)

