import RPi.GPIO as GPIO
import time
import threading


MEASUREMENTS = [{
    #forward
    "trigger": 7,
    "echo": 11,
    "output": 37,
    "distance": False,
    "alertDistance": 50,
},{
    #left
    "trigger": 12,
    "echo": 16,
    "output": 40,
    "distance": False,
    "alertDistance": 25,
}]

GPIO.setmode(GPIO.BOARD)

for setup in MEASUREMENTS:
    GPIO.setup(setup["trigger"], GPIO.OUT)
    GPIO.setup(setup["echo"], GPIO.IN)
    GPIO.setup(setup["output"], GPIO.OUT)

def get_distance(trigger, echo, num_readings):
    distances = []
    for i in range(num_readings):
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
        distances.append(distance)
        time.sleep(0.01)
    return sum(distances) / num_readings

def get_buzz_frequency(distance):
    frequency = distance / 60
    if frequency < 0.25:
        frequency = 0.25
    return frequency

def alert_user(sensor):
    while True:
        current_distance = sensor["distance"]
        if current_distance and current_distance < sensor['alertDistance']:
            buzz_frequency = get_buzz_frequency(current_distance)
            GPIO.output(sensor["output"], True)
            time.sleep(buzz_frequency)
            GPIO.output(sensor["output"], False)
            time.sleep(buzz_frequency)

def output_distance():
    while True:
        for sensor in MEASUREMENTS:
            sensor["distance"] = get_distance(sensor["trigger"], sensor["echo"], 4)
            print("Sensor:", sensor['trigger'], "Distance:", sensor["distance"])
        time.sleep(0.25)

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