# ESP32 Project Repository

## 📋 Device Information
**ESP32-38Pin (CP2102)** - Ini adalah perangkat yang saya gunakan secara spesifik.

![ESP32 38Pin](https://images.prom.ua/4524657729_w1280_h640_plata-razrabotchika-esp32.jpg)

**Spesifikasi Board:**
- **Tipe:** ESP32-WROOM-32
- **Chip:** ESP32-D0WDQ6
- **USB-TTL:** CP2102
- **Pin:** 38 pin (19 di setiap sisi)
- **Flash Memory:** 4MB
- **SRAM:** 520KB
- **Clock Speed:** 240MHz
- **WiFi:** 2.4GHz 802.11 b/g/n
- **Bluetooth:** Bluetooth 4.2 BR/EDR dan BLE

**Pinout khusus board ini:**
- GPIO yang tersedia: 0-19, 21-23, 25-27, 32-39
- Pin input only: GPIO 34, 35, 36, 39
- DAC: GPIO 25, 26
- ADC: Semua GPIO kecuali GPIO 6-11 (terhubung ke flash memory)

## 🛠️ Persyaratan Khusus untuk Device Ini

### **Driver Wajib (Windows 10/11)**
Karena menggunakan chip CP2102, **WAJIB install driver ini:**
1. Download driver dari: [https://github.com/takathena/esp32driver](https://github.com/takathena/esp32driver)
2. Atau dari situs resmi: [CP210x USB to UART Bridge](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

### **Kabel USB yang Cocok**
- Gunakan kabel USB **data** (bukan hanya charger)
- Port USB 2.0/3.0 di laptop/PC
- Hindari USB hub eksternal (direct connect lebih baik)

## 💻 Software yang Saya Gunakan

### **1. Thonny IDE**
- Versi: 4.0 atau terbaru
- Setting khusus untuk device ini:
  ```
  Interpreter: MicroPython (ESP32)
  Port: COMx (akan terdeteksi setelah driver diinstall)
  ```

### **2. Firmware MicroPython**
- Gunakan firmware khusus ESP32: `esp32-idf4-xxxxx.bin`
- Download dari: [micropython.org/download/esp32](https://micropython.org/download/esp32/)

## 📥 Setup untuk Device Ini

### **Langkah 1: Install Driver**
1. Download driver CP2102 dari repo saya
2. Install driver (Run as Administrator jika perlu)
3. Restart komputer

### **Langkah 2: Flash Firmware**
```bash
# Untuk device ini, gunakan perintah:
esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 firmware.bin
```
> **Catatan:** COM3 bisa berbeda di device Anda

### **Langkah 3: Clone Repository**
```bash
git clone https://github.com/takathena/esp32.git
cd esp32
```

## ⚙️ Konfigurasi Khusus Device

### **Setting GPIO untuk Board Ini**
```python
# config.py - Setting khusus untuk ESP32-38Pin
LED_PIN = 2  # LED built-in di pin GPIO2
BUTTON_PIN = 0  # Button boot di GPIO0

# Pin yang aman digunakan:
SAFE_PINS = [2, 4, 5, 12, 13, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33]
```

### **Power Management**
Device ini memiliki:
- Input voltage: 5V via USB
- Operating voltage: 3.3V
- Maximum current per pin: 40mA
- **Hindari** memberi voltage lebih dari 3.3V ke GPIO!

## 🚀 Cara Pakai dengan Device Ini

### **1. Connect Device**
- Colokkan ESP32 ke USB laptop
- Tunggu hingga terdeteksi (LED merah menyala)
- Buka Thonny, pilih port yang muncul (misal: COM3)

### **2. Upload Code**
```python
# Contoh sederhana untuk test device
from machine import Pin
import time

led = Pin(2, Pin.OUT)  # GPIO2 untuk LED built-in

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```

### **3. Troubleshooting Khusus Device**

**Masalah: Device tidak terdeteksi**
```
Solusi:
1. Pastikan driver CP2102 terinstall
2. Coba ganti kabel USB
3. Coba port USB lain di laptop
4. Cek Device Manager (Windows) → Ports (COM & LPT)
```

**Masalah: Gagal upload code**
```
Solusi:
1. Tekan tombol BOOT saat upload
2. Kurangi baud rate ke 115200
3. Coba esptool dengan perintah erase_flash dulu
```

## 📁 Struktur File untuk Device Ini
```
esp32/
├── lib                 # library untuk mendeteksi sensor
├── main.py             # File utama (auto run)
└── examples/           # Contoh yang sudah di-test di device ini
    ├── basic/          # Basic GPIO control
    ├── wifi/           # WiFi connection
    └── sensors/        # Sensor yang compatible
```

## ⚠️ Hal Penting tentang Device Ini

### **Pin yang Tidak Bisa Digunakan:**
- **GPIO 6-11**: Terhubung ke flash memory (JANGAN dipakai!)
- **GPIO 28-31**: Tidak ada di board 38-pin

### **Fitur Khusus:**
- Ada LED built-in di GPIO2
- Ada button built-in di GPIO0 (boot button)
- Support capacitive touch pada GPIO: 0, 2, 4, 12-15, 27-33

### **Rekomendasi Sensor:**
Sensor yang sudah saya test bekerja baik:
- DHT11/DHT22 (pin 4, 5, 18, 19)
- HC-SR04 (pin 12, 13, 14, 15)
- BMP280 (I2C: SCL=22, SDA=21)

---

**Note:** Semua code di repo ini sudah di-test di **ESP32-38Pin (CP2102)** yang saya gunakan. Jika ada masalah, kemungkinan besar karena perbedaan board.
