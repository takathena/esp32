from machine import Pin, I2C
import ssd1306, time, math, network, socket

class MonitoringAir:
    def __init__(self,
                 trig=5, echo=18,
                 scl=22, sda=21,
                 led_merah=25, led_kuning=26, led_hijau=27, buzzer=14,
                 tinggi_tandon=30.0, jari_jari=10.0,
                 ssid="Kelompok3 Monitoring Air"):
        # === Setup Ultrasonik ===
        self.trig = Pin(trig, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)

        # === Setup OLED ===
        i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)

        # === LED & Buzzer ===
        self.led_merah = Pin(led_merah, Pin.OUT)
        self.led_kuning = Pin(led_kuning, Pin.OUT)
        self.led_hijau = Pin(led_hijau, Pin.OUT)
        self.buzzer = Pin(buzzer, Pin.OUT)

        # === Parameter Tandon ===
        self.TINGGI_TANDON = tinggi_tandon
        self.JARI_JARI = jari_jari

        # === WiFi AP ===
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=ssid)

        # === Webserver ===
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen(1)

    # === Sensor Ultrasonik ===
    def read_distance(self):
        self.trig.value(0)
        time.sleep_us(2)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        timeout = time.ticks_add(time.ticks_us(), 30000)
        while self.echo.value() == 0:
            if time.ticks_diff(timeout, time.ticks_us()) <= 0:
                return self.TINGGI_TANDON
        t1 = time.ticks_us()

        timeout = time.ticks_add(time.ticks_us(), 30000)
        while self.echo.value() == 1:
            if time.ticks_diff(timeout, time.ticks_us()) <= 0:
                return self.TINGGI_TANDON
        t2 = time.ticks_us()

        durasi = time.ticks_diff(t2, t1)
        return (durasi * 0.0343) / 2

    # === Hitung level & volume ===
    def get_level_volume(self):
        jarak = self.read_distance()
        tinggi_air = self.TINGGI_TANDON - jarak
        tinggi_air = max(0, min(tinggi_air, self.TINGGI_TANDON))
        volume = math.pi * (self.JARI_JARI ** 2) * tinggi_air / 1000.0
        return tinggi_air, volume

    # === Update OLED ===
    def update_display(self, level, volume):
        self.oled.fill(0)
        self.oled.text("Monitoring Air", 0, 0)
        self.oled.text("Level: {:.1f} cm".format(level), 0, 20)
        self.oled.text("Vol : {:.1f} L".format(volume), 0, 40)
        self.oled.show()

    # === Kontrol LED & Buzzer ===
    def kontrol_led_buzzer(self, level):
        self.led_merah.value(0)
        self.led_kuning.value(0)
        self.led_hijau.value(0)
        self.buzzer.value(0)

        if level < 10:
            self.led_merah.value(1)
        elif level < 20:
            self.led_kuning.value(1)
        else:
            self.led_hijau.value(1)
            self.buzzer.value((time.ticks_ms() // 500) % 2)

    # === Halaman Web ===
    def webpage(self, level, volume):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="2">
            <title>Monitoring Air</title>
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

    # === Serve HTTP Client ===
    def serve_client(self, level, volume):
        try:
            self.s.settimeout(0.1)
            cl, addr = self.s.accept()
            cl.recv(1024)
            response = self.webpage(level, volume)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            print("Client:", addr)
        except OSError:
            pass
