import network
import socket
import time

# ---- Konfigurasi WiFi ----
SSID = "gendis"
PASSWORD = "77777777"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Mencoba konek ke WiFi...")
while not wlan.isconnected():
    time.sleep(1)
    print("Belum konek...")

print("Berhasil konek!")
print("IP ESP32:", wlan.ifconfig()[0])

# ---- Web Server ----
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Web server jalan di http://%s" % wlan.ifconfig()[0])

while True:
    cl, addr = s.accept()
    print('Koneksi dari', addr)
    request = cl.recv(1024)
    print("Request:", request)

    response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <!DOCTYPE html>
    <html>
    <head><title>ESP32 Web Server</title></head>
    <body>
        <h1>Halo dari ESP32 oke</h1>
        <p>ESP32 sudah bisa jadi web server!</p>
    </body>
    </html>
    """

    cl.send(response)
    cl.close()

