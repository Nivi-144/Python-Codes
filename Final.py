#!/usr/bin/env python3
"""
Raspberry Pi Code - Fire Detection System with BlueDot Motor Control
Controls motors via BlueDot and Relay module for Water Pump based on fire detection
"""

import serial
import time
import RPi.GPIO as GPIO
from bluedot import BlueDot
from signal import pause
import threading

# -------- Serial Configuration --------
SERIAL_PORT = '/dev/ttyACM0'  # Change to /dev/ttyUSB0 if needed
BAUD_RATE = 9600

# -------- Motor Pin Setup --------
ENA = 18
IN1 = 23
IN2 = 24
ENB = 19
IN3 = 27
IN4 = 22

# -------- Relay Pin Setup --------
RELAY_PIN = 17  # GPIO17 (Pin 11)

# -------- GPIO Setup --------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup motor pins
pins = [ENA, IN1, IN2, ENB, IN3, IN4]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# -------- Relay Control Functions (Water Pump) --------
def pump_off():
    """Turn Water Pump OFF via Relay - Switches pin to INPUT to 'hide' signal from relay"""
    GPIO.setup(RELAY_PIN, GPIO.IN)

def pump_on():
    """Turn Water Pump ON via Relay - Switches pin to OUTPUT and pulls LOW to trigger relay"""
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.LOW)

# Start in OFF state
pump_off()

# PWM setup
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(0)  # Start at 0 speed
pwmB.start(0)

# -------- Serial Functions --------
def setup_serial():
    """Initialize serial connection to Arduino"""
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for connection to establish
        print("Serial connection established with Arduino")
        return ser
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}")
        print(f"Details: {e}")
        return None

def read_sensor_data(ser):
    """Read and parse sensor data from Arduino"""
    try:
        if ser.in_waiting > 0:
            # Read line from serial
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # Parse CSV data: mq2,mq7,mq135,flame,temp,hum
                data = line.split(',')
                
                if len(data) == 6:
                    mq2 = int(data[0])
                    mq7 = int(data[1])
                    mq135 = int(data[2])
                    flame = int(data[3])
                    temp = float(data[4])
                    hum = float(data[5])
                    
                    return {
                        'mq2': mq2,
                        'mq7': mq7,
                        'mq135': mq135,
                        'flame': flame,
                        'temperature': temp,
                        'humidity': hum
                    }
    except Exception as e:
        print(f"Error reading data: {e}")
    
    return None

def display_sensor_data(data):
    """Display sensor readings"""
    print("\n" + "="*50)
    print("SENSOR READINGS")
    print("="*50)
    print(f"MQ-2 (Smoke/LPG)    : {data['mq2']}")
    print(f"MQ-7 (CO)           : {data['mq7']}")
    print(f"MQ-135 (Air Quality): {data['mq135']}")
    print(f"Flame Sensor        : {'FIRE DETECTED!' if data['flame'] == 0 else 'No Fire'}")
    print(f"Temperature         : {data['temperature']} C")
    print(f"Humidity            : {data['humidity']} %")
    print("="*50)

# -------- Motor Control Functions --------
def forward(speed=70):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def backward(speed=70):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def turn_left(speed=70):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def turn_right(speed=70):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def stop():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

# -------- BlueDot Control Functions --------
def move(pos):
    """Control rover based on BlueDot position"""
    x = pos.x  # -1 (left) to 1 (right)
    y = pos.y  # -1 (down) to 1 (up)
    
    # Calculate speed based on distance from center (0-100%)
    distance = pos.distance
    speed = int(distance * 100)
    speed = max(30, min(speed, 100))  # Limit between 30-100%
    
    # Determine direction based on angle
    angle = pos.angle
    
    if y > 0.3:  # Forward zone
        if abs(x) < 0.3:  # Going straight
            forward(speed)
        elif x > 0:  # Forward-right
            turn_right(speed)
        else:  # Forward-left
            turn_left(speed)
    elif y < -0.3:  # Backward zone
        backward(speed)
    elif abs(x) > 0.3:  # Left/Right only
        if x > 0:
            turn_right(speed)
        else:
            turn_left(speed)
    else:
        stop()

def pressed():
    print("BlueDot pressed!")

def released():
    print("BlueDot released - stopping rover")
    stop()

# -------- Sensor Monitoring Thread --------
def sensor_monitoring_thread(ser):
    """Background thread for continuous sensor monitoring"""
    try:
        while True:
            # Read sensor data from Arduino
            data = read_sensor_data(ser)
            
            if data:
                # Display the data
                display_sensor_data(data)
                
                # Fire Detection Logic
                # Check if flame sensor detects fire (flame == 0 means fire detected)
                if data['flame'] == 0:
                    print("\n" + "!"*60)
                    print("!!! ALERT: FIRE DETECTED! !!!")
                    print("!!! ACTIVATING WATER PUMP TO EXTINGUISH FIRE !!!")
                    print("!"*60 + "\n")
                    
                    # Turn ON Water Pump via Relay
                    pump_on()
                    
                else:
                    # No fire detected - Keep water pump OFF
                    pump_off()
                
            time.sleep(0.5)  # Match Arduino delay
            
    except Exception as e:
        print(f"\nError in sensor monitoring: {e}")

# -------- Main Function --------
def main():
    """Main program loop"""
    print("="*60)
    print("Fire Detection System with BlueDot Motor Control")
    print("="*60)
    print("\nInitializing components...")
    
    # Setup serial connection
    print("\n1. Connecting to Arduino...")
    ser = setup_serial()
    if ser is None:
        print("Failed to connect to Arduino. Exiting...")
        return
    
    # Start sensor monitoring in background thread
    print("\n2. Starting sensor monitoring thread...")
    sensor_thread = threading.Thread(target=sensor_monitoring_thread, args=(ser,), daemon=True)
    sensor_thread.start()
    
    # Create BlueDot instance
    print("\n3. Starting BlueDot motor controller...")
    bd = BlueDot()
    
    # Attach event handlers
    bd.when_pressed = pressed
    bd.when_moved = move
    bd.when_released = released
    
    print("\n" + "="*60)
    print("BlueDot rover controller started")
    print("="*60)
    print("Waiting for connection...")
    print(f"Server address: {bd.server.server_address}")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        pause()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop()
        pump_off()  # Ensure water pump is OFF
        pwmA.stop()
        pwmB.stop()
        if ser:
            ser.close()
        GPIO.cleanup()
        print("Cleanup complete")

if __name__ == "__main__":
    main()