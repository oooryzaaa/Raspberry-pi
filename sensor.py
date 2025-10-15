import RPi.GPIO as GPIO
import time

# Gunakan penomoran BCM
GPIO.setmode(GPIO.BCM)

# Atur GPIO
TRIG = 23
ECHO = 25

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def hitung_jarak():
    # Set TRIG rendah untuk memastikan tidak ada pulsa
    GPIO.output(TRIG, False)
    time.sleep(0.5)

    # Kirim pulsa selama 10 mikrodetik
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout_start = time.time()

    # Waktu sinyal mulai
    while GPIO.input(ECHO) == 0:
        waktu_mulai = time.time()
        if time.time() - timeout_start > 1:  # Timeout jika lebih dari 1 detik
            print("Timeout: Tidak menerima sinyal mulai.")
            return None

    timeout_start = time.time()

    # Waktu sinyal diterima kembali
    while GPIO.input(ECHO) == 1:
        waktu_akhir = time.time()
        if time.time() - timeout_start > 1:  # Timeout jika lebih dari 1 detik
            print("Timeout: Tidak menerima sinyal akhir.")
            return None

    durasi = waktu_akhir - waktu_mulai

    # Kecepatan suara = 34300 cm/s
    jarak = durasi * 17150
    jarak = round(jarak, 2)

    return jarak

try:
    while True:
        jarak = hitung_jarak()
        if jarak is not None:
            print(f"Jarak: {jarak} cm")
        else:
            print("Gagal mengukur jarak.")
        time.sleep(1)

except KeyboardInterrupt:
    print("Menghentikan program")
    GPIO.cleanup()
