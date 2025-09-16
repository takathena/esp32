import time
from monitoringair import MonitoringAir

app = MonitoringAir()

while True:
    level, volume = app.get_level_volume()
    app.update_display(level, volume)
    app.kontrol_led_buzzer(level)
    app.serve_client(level, volume)

    print("Level:", level, "cm | Volume:", volume, "L")
    time.sleep(1)
