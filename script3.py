from gpiozero import SPIDevice
import time

LED_COUNT = 60  # Number of LEDs in your strip
spi = SPIDevice(0, 0)  # SPI bus 0, device 0 (you may need to adjust this)

def send_color(color):
    data = [color] * LED_COUNT * 3
    spi.write(data)

try:
    while True:
        send_color(0xFF0000)  # Set all LEDs to red
        time.sleep(1)
        send_color(0x00FF00)  # Set all LEDs to green
        time.sleep(1)
        send_color(0x0000FF)  # Set all LEDs to blue
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
