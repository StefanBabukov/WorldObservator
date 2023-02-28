import RPi.GPIO as GPIO
import time
import threading


# TRIGGERS = [7, 8, 12]
# ECHOS = [11, 10, 16]
# OUTPUTS = [37, 38, 40]

MEASUREMENTS = [{
    "trigger": 7,
    "echo": 11,
    "output": 37
},{
    "trigger": 8,
    "echo": 10,
    "output": 38,
},{
    "trigger": 12,
    "echo": 16,
    "output": 40,
},]
# following the board pin numbering 
GPIO.setmode(GPIO.BOARD)

#set GPIO direction (IN / OUT)
for setup in MEASUREMENTS:
    GPIO.setup(setup["trigger"], GPIO.OUT)
    GPIO.setup(setup["echo"], GPIO.IN)
    GPIO.setup(setup["output"], GPIO.OUT)

distances = []

def get_distance(trigger, echo):
     
    #GPIO pins
    GPIO.output(trigger, True)

    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    distance = (stop_time - start_time) * 34300 / 2
    return distance

def alert_user(sensor):
    global distances
    while True and len(distances)==3:
        if sensor["distance"] and sensor["distance"] > 70:
            continue
        blink_frequency = distances[sensor] / 100
        GPIO.output(sensor["output"], True)
        time.sleep(blink_frequency)
        GPIO.output(sensor["output"], False)
        time.sleep(blink_frequency)

def output_distance():
    global distances
    while True:
        for sensor in MEASUREMENTS:
            sensor["distance"] = get_distance(sensor["trigger"], sensor["echo"])
            print("Distance ", sensor["distance"])

try:
    measuring_thread = threading.Thread(target=output_distance)
    measuring_thread.start()

    for sensor in MEASUREMENTS:
        thread = threading.Thread(target=alert_user, args=(sensor, ))
        thread.start()

    measuring_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    print("Clean up")
    GPIO.cleanup()