import librosa
import RPi.GPIO as GPIO
import time

# Configureer GPIO-pinnen voor LEDs
GPIO.setmode(GPIO.BCM)
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)

# Functie om LEDs te laten knipperen met een bepaalde snelheid (BPM)
def blink_LED(bpm):
    interval = 60.0 / bpm  # Bereken de tijd tussen knippers op basis van BPM
    while True:
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(interval / 2)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(interval / 2)

# Functie om BPM van mp4-bestand te detecteren
def detect_BPM(mp4_file):
    y, sr = librosa.load(mp4_file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    return tempo

if __name__ == "__main__":
    mp4_file = "jouw_bestand.mp4"  # Vervang dit door het pad naar jouw mp4-bestand
    bpm = detect_BPM(mp4_file)
    print(f"Gedetecteerde BPM: {bpm}")
    blink_LED(bpm)