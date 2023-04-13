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

for sensor in MEASUREMENTS:
    GPIO.setup(sensor["trigger"], GPIO.OUT)
    GPIO.setup(sensor["echo"], GPIO.IN)
    GPIO.setup(sensor["output"], GPIO.OUT)

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

def alert_user():
    print("IN ALERT USER")
    while True:
        for sensor in MEASUREMENTS:
            distance = sensor['distance']
            print("distance is ", distance)
            if distance and distance < sensor['alertDistance']:
                buzz_frequency = get_buzz_frequency(distance)
                print('buzz frequency', buzz_frequency)
                GPIO.output(sensor['output'], True)
                time.sleep(buzz_frequency)
                GPIO.output(sensor['output'], False)
                time.sleep(buzz_frequency)
            else:
                time.sleep(0.25)

def print_distance():
    for sensor in MEASUREMENTS:
        print("Sensor ", sensor['name'] , " Distance: ", sensor['distance'])

# def output_distance(sensor):
#     distance = {
#         "output": sensor['output'],
#         "distance": get_distance(sensor["trigger"], sensor["echo"], 2),
#         "alertDistance": sensor['alertDistance']
#     }
#     return distance

try:
    thread = threading.Thread(target=alert_user)
    thread.start()

    while True:
        for sensor in MEASUREMENTS:
            distance = get_distance(sensor["trigger"], sensor["echo"], 2)
            sensor['distance'] = distance
            buzz_frequency = get_buzz_frequency(distance)

        print_distance()

        time.sleep(0.01) # Wait for a short period to avoid excessive CPU usage

except KeyboardInterrupt:
    print("Measurement stopped by User")

finally:
    print("Clean up")
    GPIO.cleanup()
