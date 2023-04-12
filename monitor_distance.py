import RPi.GPIO as GPIO
import time
import threading


MEASUREMENTS = [{
    "name": "forward",
    "trigger": 7,
    "echo": 11,
    "output": 37,
    "distance": False,
    "alertDistance": 65,
},
{   
    "name": "left",
    "alertDistance" : 40,
    "distance": False,
    "trigger": 8,
    "echo": 10,
    "output": 38,
    },
{
    "name": "right",
    "trigger": 12,
    "echo": 16,
    "output": 40,
    "distance": False,
    "alertDistance": 40,
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
        pulse_start = time.time()
        while GPIO.input(echo) == 1:
            stop_time = time.time()
            if stop_time - pulse_start > 0.01: # break if echo remains high for too long
                distance = 100
                print('breaking from here')
                break
            else:
                distance = (stop_time - start_time) * 34300 / 2

        distances.append(distance)
        time.sleep(0.01)
    return sum(distances) / num_readings

def get_buzz_frequency(distance):
    frequency = distance / 60
    if frequency < 0.25:
        frequency = 0.25
    return frequency

def alert_user(distance):
    while True:
        current_distance = distance[1]
        output_pin = distance[0]
        if current_distance and current_distance < sensor['alertDistance']:
            buzz_frequency = get_buzz_frequency(current_distance)
            GPIO.output(output_pin, True)
            time.sleep(buzz_frequency)
            GPIO.output(output_pin, False)
            time.sleep(buzz_frequency)

def print_distance():
    for sensor in MEASUREMENTS:
        print("Sensor ", sensor['name'] , " Distance: ", sensor['distance'])

def output_distance():
    #holding data in the format [outputpin, distance]
    distances = []
    for sensor in MEASUREMENTS:
        distances.append[[sensor['output'], get_distance(sensor["trigger"], sensor["echo"], 2)]]
    print_distance()
    return distances

try:
    distances = output_distance()
    for distance in distances:
        alert_user(distance)
    
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    print("Clean up")
    GPIO.cleanup()
