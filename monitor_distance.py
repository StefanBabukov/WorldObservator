import RPi.GPIO as GPIO
import time
import threading


MEASUREMENTS = [{
    "name": "forward",
    "distance": False,
    "trigger": 7,
    "echo": 11,
    "output": 37, # corresponding pin for vibration output
    "alertDistance": 100, #how far (cm) an object needs to be to start alerting the user
},
{   
    "name": "right",
    "distance": False,
    "trigger": 8,
    "echo": 10,
    "output": 38,
    "alertDistance" : 45,
    },
{
    "name": "left",
    "distance": False,
    "trigger": 12,
    "echo": 16,
    "output": 40,
    "alertDistance": 45, 
}]

GPIO.setmode(GPIO.BOARD)

for sensor in MEASUREMENTS:
    GPIO.setup(sensor["trigger"], GPIO.OUT)
    GPIO.setup(sensor["echo"], GPIO.IN)
    GPIO.setup(sensor["output"], GPIO.OUT)

def get_distance(trigger, echo, num_readings):
    distances = []
    # getting a number of readings at a time and averaging them, to eliminate innacuracies
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
            # if the echo waits for the trigger signal too long, assume its too far away and stop waiting
            # this gives more frequent readings
            if stop_time - pulse_start > 0.01: 
                distance = 100
                break
            else:
                distance = (stop_time - start_time) * 34300 / 2

        distances.append(round(distance,2))
        time.sleep(0.01)
    return sum(distances) / num_readings

def get_buzz_frequency(distance):
    # the closer the object is, the more frequent the vibrations are
    frequency = distance / 60
    if frequency < 0.25:
        frequency = 0.25
    return frequency

def alert_user():
    while True:
        for sensor in MEASUREMENTS:
            distance = sensor['distance']
            if distance and distance < sensor['alertDistance']:
                buzz_frequency = get_buzz_frequency(distance)
                GPIO.output(sensor['output'], True)
                time.sleep(0.5)
                GPIO.output(sensor['output'], False)
                time.sleep(buzz_frequency)

def print_distance():
    for sensor in MEASUREMENTS:
        distance = sensor['distance']
        if distance == 100:
            distance = 'clear'
        print("Sensor ", sensor['name'] , " Object at: ", "{:.2f} ".format(distance), ' cm')

try:
    thread = threading.Thread(target=alert_user)
    thread.start()

    while True:
        for sensor in MEASUREMENTS:
            distance = get_distance(sensor["trigger"], sensor["echo"], 3)
            sensor['distance'] = distance
            buzz_frequency = get_buzz_frequency(distance)

        print_distance()

        time.sleep(0.01) # Wait for a short period to avoid excessive CPU usage

except KeyboardInterrupt:
    print("Measurement stopped by User")

finally:
    print("Clean up")
    GPIO.cleanup()
