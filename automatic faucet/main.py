from machine import Pin, PWM, time_pulse_us
import time

# --- Konfigurasi pin ---
TRIG_PIN = 5      # TRIG HC-SR04
ECHO_PIN = 18     # ECHO HC-SR04
BUZZER_PIN = 23   # Buzzer aktif
LED_PIN = 2       # LED
SERVO_PIN = 19    # Servo signal

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
buzzer = Pin(BUZZER_PIN, Pin.OUT)
led = Pin(LED_PIN, Pin.OUT)
servo = PWM(Pin(SERVO_PIN), freq=50)  # Servo pakai PWM 50Hz

def get_distance():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)  # timeout 30ms
    distance = (duration * 0.0343) / 2
    return distance

# Fungsi untuk atur sudut servo
def set_servo_angle(angle):
    min_us = 500   # pulse terpendek (0 derajat)
    max_us = 2500  # pulse terpanjang (180 derajat)
    us = min_us + (angle / 180) * (max_us - min_us)
    duty = int((us / 20000) * 1023)  # konversi ke duty 10-bit (0–1023)
    servo.duty(duty)

# --- Variabel status ---
in_range = False

while True:
    try:
        jarak = get_distance()
        print("Jarak: {:.2f} cm".format(jarak))

        if 1 <= jarak <= 10:
            led.value(1)
            set_servo_angle(90)  # servo ke 90 derajat

            if not in_range:  # baru masuk range
                buzzer.value(1)
                time.sleep(0.2)
                buzzer.value(0)
                in_range = True
        else:
            led.value(0)
            buzzer.value(0)
            set_servo_angle(0)  # servo balik ke 0 derajat
            in_range = False

        time.sleep(0.2)

    except OSError as e:
        print("Gagal baca:", e)
        time.sleep(1)
