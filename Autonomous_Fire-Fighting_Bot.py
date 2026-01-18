import RPi.GPIO as GPIO
import time

FLAME_SENSOR_PIN = 2
RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_SENSOR_PIN, GPIO.IN)

def pump_on():
    # To turn an Active-Low relay ON, we set it to Output Low
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.LOW)

def pump_off():
    # To turn it OFF, we turn the pin into an INPUT
    # This 'hides' the pin from the relay so it can't see the 3.3V
    GPIO.setup(RELAY_PIN, GPIO.IN)

try:
    print("System Starting... Pump should stay OFF.")
    while True:
        if GPIO.input(FLAME_SENSOR_PIN) == 0:
            print("FIRE DETECTED! -> Pump ON")
            pump_on()
        else:
            print("No Fire -> Pump OFF")
            pump_off()
            
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()