from machine import Pin, I2C
import ssd1306, time, math, network, socket

# === Setup Ultrasonik ===
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# === Setup OLED ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Setup LED dan Buzzer ===
led_merah = Pin(25, Pin.OUT)   # LED Merah ke GPIO25
led_kuning = Pin(26, Pin.OUT)  # LED Kuning ke GPIO26
led_hijau = Pin(27, Pin.OUT)   # LED Hijau ke GPIO27
buzzer = Pin(14, Pin.OUT)      # Buzzer ke GPIO14

# === Parameter Tandon ===
TINGGI_TANDON = 30.0   # cm
JARI_JARI = 10.0       # cm

# === Fungsi baca jarak dengan timeout ===
def read_distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Tunggu echo naik (max 30 ms)
    timeout = time.ticks_add(time.ticks_us(), 30000)
    while echo.value() == 0:
        if time.ticks_diff(timeout, time.ticks_us()) <= 0:
            return TINGGI_TANDON  # anggap kosong

    t1 = time.ticks_us()

    # Tunggu echo turun (max 30 ms)
    timeout = time.ticks_add(time.ticks_us(), 30000)
    while echo.value() == 1:
        if time.ticks_diff(timeout, time.ticks_us()) <= 0:
            return TINGGI_TANDON

    t2 = time.ticks_us()

    durasi = time.ticks_diff(t2, t1)
    jarak = (durasi * 0.0343) / 2  # cm
    return jarak

# === Buat Hotspot (AP Mode) ===
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="Kelompok3 Monitoring Air")
print("Access Point:", ap.ifconfig())

# === mDNS biar bisa diakses via nama ===
try:
    import mdns
    mdns_server = mdns.Server()
    mdns_server.start("monitoringair", "Monitoring Air IoT")
    print("mDNS aktif: akses http://monitoringair.local/")
except Exception as e:
    print("Gagal start mDNS:", e)

# === Webserver ===
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print('Web server running...')

# === Halaman web ===
def webpage(level, volume):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <title>Monitoring Air</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; text-align: center; }}
            h2 {{ color: #0077cc; }}
            .box {{ margin: 20px auto; padding: 20px; border: 1px solid #ccc; width: 250px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <h2>Monitoring Level Air</h2>
        <div class="box">
            <p><b>Tinggi Air:</b> {level:.1f} cm</p>
            <p><b>Volume:</b> {volume:.1f} L</p>
        </div>
    </body>
    </html>
    """
    return html

# === Loop utama ===
while True:
    # Baca sensor
    jarak = read_distance()
    tinggi_air = TINGGI_TANDON - jarak
    if tinggi_air < 0:
        tinggi_air = 0
    if tinggi_air > TINGGI_TANDON:
        tinggi_air = TINGGI_TANDON

    volume = math.pi * (JARI_JARI**2) * tinggi_air / 1000.0

    # Update OLED
    oled.fill(0)
    oled.text("Monitoring Air", 0, 0)
    oled.text("Level: {:.1f} cm".format(tinggi_air), 0, 20)
    oled.text("Vol : {:.1f} L".format(volume), 0, 40)
    oled.show()

    print("Level:", tinggi_air, "cm | Volume:", volume, "L")

    # === Logika LED & Buzzer ===
    led_merah.value(0)
    led_kuning.value(0)
    led_hijau.value(0)
    buzzer.value(0)

    if tinggi_air < 10:  # Rendah
        led_merah.value(1)
    elif tinggi_air < 20:  # Sedang
        led_kuning.value(1)
    else:  # Penuh / dekat
        led_hijau.value(1)
        buzzer.value((time.ticks_ms() // 500) % 2)  # bunyi beep tiap 0.5 detik

    # === Webserver ===
    try:
        s.settimeout(0.1)
        cl, addr = s.accept()
        request = cl.recv(1024)
        response = webpage(tinggi_air, volume)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        print("Client served:", addr)
    except OSError:
        pass

    time.sleep(1)
