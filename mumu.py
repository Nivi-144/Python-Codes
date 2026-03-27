#!/usr/bin/env python3
"""
Raspberry Pi Code - Fire Detection System with BlueDot Motor Control
Controls motors via BlueDot | Pump relay now handled by Arduino via Serial
NOW WITH AI/ML Fire Detection using trained Random Forest model
+ Pump Speed Control via Laptop Gesture Controller (UDP port 9999)
FIX: Servo now stops instantly when fire is detected during sweep and locks.
"""

import serial
import time
import RPi.GPIO as GPIO
from bluedot import BlueDot
from signal import pause
import threading
import joblib
import numpy as np
import socket

# ── Detection mode + image fire status globals ───
detection_mode    = 1             # 1=sensors, 2=image, 3=both (set from PUMP.py)
image_fire_status = "IMAGE_SAFE"  # updated by image_alert_receiver_thread

# -------- Serial Configuration --------
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE   = 9600

# ──────────────────────────────────────────────────────────────
# MOTOR PIN SETUP
# ──────────────────────────────────────────────────────────────
ENA = 18   # RIGHT side
IN1 = 23   
IN2 = 24   

ENB = 13   # LEFT side
IN3 = 27   
IN4 = 22   

# -------- GPIO Setup --------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# -------- PWM setup for motors --------
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(0)
pwmB.start(0)

# -------- Pump PWM Speed Pin --------
PUMP_PWM_PIN = 25
GPIO.setup(PUMP_PWM_PIN, GPIO.OUT)
pump_speed_pwm = GPIO.PWM(PUMP_PWM_PIN, 1000)
pump_speed_pwm.start(0)

# ──────────────────────────────────────────────────────────────
# SERVO SETUP
# ──────────────────────────────────────────────────────────────
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(7.5)                  

# -------- Global State --------
gesture_speed     = 0
fire_active       = False
was_fire_active   = False
current_pwm_speed = 0

# -------- Servo State --------
servo_locked_angle = 90      
servo_sweeping     = False   
latest_flame_ao    = 1023    
latest_flame_do    = 1       # 1 = no fire, 0 = fire

# ======================================================
# SERVO CONTROL
# ======================================================
def servo_set_angle(angle):
    """Move servo to given angle (0-180)."""
    angle = max(0, min(180, int(angle)))
    duty  = 2.5 + (angle / 180.0) * 10.0
    servo_pwm.ChangeDutyCycle(duty)

def servo_auto_sweep_thread():
    """
    Continuously sweeps servo 0<->180. 
    If fire is detected (Analog < 500 or Digital == 0), it STOPS and LOCKS.
    """
    global servo_locked_angle, fire_active
    direction = 1
    angle     = 90
    
    while True:
        # If the main system marks fire_active, stay at the current angle
        if fire_active:
            # Check if fire has cleared to resume
            time.sleep(0.1)
            continue

        # Check local sensor readings to see if we hit fire DURING the sweep
        # Analog threshold 500 or Digital 0
        if latest_flame_ao < 500 or latest_flame_do == 0:
            print(f"[SERVO] Fire Sensed at {angle} deg! Locking and stopping sweep.")
            servo_locked_angle = angle
            # We don't sleep here, the fire_active flag from the monitor thread 
            # will keep us in the 'if fire_active' loop above until it's out.
            time.sleep(0.1)
            continue

        # Normal Sweep Logic
        angle += direction * 3 # Adjust step size for speed/precision
        if angle >= 180:
            angle     = 180
            direction = -1
        elif angle <= 0:
            angle     = 0
            direction = 1
            
        servo_set_angle(angle)
        servo_locked_angle = angle
        time.sleep(0.05) # Adjust for sweep smoothness

def set_pump(speed):
    """Set pump PWM speed (0-100)."""
    global current_pwm_speed
    speed = max(0, min(100, int(speed)))
    if speed == 0:
        pump_speed_pwm.ChangeDutyCycle(0)
        current_pwm_speed = 0
    else:
        pump_speed_pwm.ChangeDutyCycle(speed)
        current_pwm_speed = speed

# ======================================================
# ML MODEL LOADING
# ======================================================
MODEL_PATH   = '/home/pi/fire_project/fire_model.pkl'
SCALER_PATH  = '/home/pi/fire_project/scaler.pkl'
ENCODER_PATH = '/home/pi/fire_project/label_encoder.pkl'

try:
    fire_model    = joblib.load(MODEL_PATH)
    scaler        = joblib.load(SCALER_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False

# ======================================================
# FIRE DETECTION LOGIC
# ======================================================
def predict_fire_status_ml(mq2, mq7, mq135, flame, temperature, humidity):
    try:
        features        = np.array([[mq2, mq7, mq135, flame, temperature, humidity]])
        features_scaled = scaler.transform(features)
        prediction      = fire_model.predict(features_scaled)
        raw_label = label_encoder.inverse_transform(prediction)[0]
        raw_upper = str(raw_label).upper()
        if "FIRE" in raw_upper: return "FIRE"
        elif "WARN" in raw_upper or "SMOKE" in raw_upper: return "WARNING"
        else: return "SAFE"
    except: return None

def basic_fire_detection(data):
    if data['flame'] == 0 or data['flame_ao'] < 500:
        return "FIRE"
    elif data['temperature'] > 55 or data['mq2'] > 500:
        return "WARNING"
    return "SAFE"

def check_fire_status(data):
    if ML_AVAILABLE:
        result = predict_fire_status_ml(data['mq2'], data['mq7'], data['mq135'], data['flame'], data['temperature'], data['humidity'])
        if result: return result
    return basic_fire_detection(data)

def get_combined_status(sensor_status):
    global detection_mode, image_fire_status
    if detection_mode == 2:
        return "FIRE" if image_fire_status == "IMAGE_FIRE" else "SAFE"
    if detection_mode == 3:
        if image_fire_status == "IMAGE_FIRE" or sensor_status == "FIRE": return "FIRE"
    return sensor_status

def handle_fire_status(status):
    global fire_active, was_fire_active
    if status == "FIRE":
        if not fire_active:
            print("!!! FIRE DETECTED - STOPPING & PUMPING !!!")
        fire_active = True
        was_fire_active = True
        stop()
        set_pump(100)
    else:
        fire_active = False
        if was_fire_active:
            print("Fire cleared - resuming sweep.")
            set_pump(0)
            was_fire_active = False

# ======================================================
# RECEIVER THREADS
# ======================================================
def pump_speed_receiver_thread():
    global gesture_speed
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9999))
    while True:
        try:
            data, _ = sock.recvfrom(16)
            speed = int(data.decode().strip())
            gesture_speed = speed
            if not fire_active: set_pump(speed)
        except: pass

def image_alert_receiver_thread():
    global image_fire_status
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 9998))
    while True:
        try:
            data, _ = sock.recvfrom(32)
            image_fire_status = data.decode().strip()
        except: pass

def mode_receiver_thread():
    global detection_mode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9997))
    while True:
        try:
            data, _ = sock.recvfrom(8)
            detection_mode = int(data.decode().strip())
        except: pass

# -------- Serial & Monitoring --------
def setup_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        return ser
    except: return None

def read_sensor_data(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        data = line.split(',')
        if len(data) == 7:
            return {
                'mq2': int(data[0]), 'mq7': int(data[1]), 'mq135': int(data[2]),
                'flame': int(data[3]), 'flame_ao': int(data[4]),
                'temperature': float(data[5]), 'humidity': float(data[6])
            }
    except: pass
    return None

def sensor_monitoring_thread(ser):
    global fire_active, latest_flame_ao, latest_flame_do
    while True:
        data = read_sensor_data(ser)
        if data:
            latest_flame_ao = data['flame_ao']
            latest_flame_do = data['flame']
            status = get_combined_status(check_fire_status(data))
            handle_fire_status(status)

# -------- Motor Control --------
def forward(speed=70):
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed); pwmB.ChangeDutyCycle(speed)

def backward(speed=70):
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed); pwmB.ChangeDutyCycle(speed)

def turn_left(speed=70):
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed); pwmB.ChangeDutyCycle(speed)

def turn_right(speed=70):
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed); pwmB.ChangeDutyCycle(speed)

def stop():
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(0); pwmB.ChangeDutyCycle(0)

# -------- BlueDot --------
def move(pos):
    if fire_active: return
    x, y, speed = pos.x, pos.y, max(30, min(int(pos.distance * 100), 100))
    if y > 0.3:
        if abs(x) < 0.3: forward(speed)
        elif x > 0: turn_right(speed)
        else: turn_left(speed)
    elif y < -0.3: backward(speed)
    elif abs(x) > 0.3:
        if x > 0: turn_right(speed)
        else: turn_left(speed)
    else: stop()

def main():
    ser = setup_serial()
    if not ser: return

    # Start Threads
    threading.Thread(target=sensor_monitoring_thread, args=(ser,), daemon=True).start()
    threading.Thread(target=pump_speed_receiver_thread, daemon=True).start()
    threading.Thread(target=image_alert_receiver_thread, daemon=True).start()
    threading.Thread(target=mode_receiver_thread, daemon=True).start()
    threading.Thread(target=servo_auto_sweep_thread, daemon=True).start()

    bd = BlueDot()
    bd.when_moved = move
    bd.when_released = stop

    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        stop()
        set_pump(0)
        GPIO.cleanup()

if __name__ == "__main__":
    main()