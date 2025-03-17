import wiringpi as wp 
import time

TRIG_PIN = 5  
ECHO_PIN = 6  

wp.wiringPiSetup()  
wp.pinMode(TRIG_PIN, 1)  
wp.pinMode(ECHO_PIN, 0)  

def read_distance():
    
    wp.digitalWrite(TRIG_PIN, 1)
    time.sleep(0.00001)
    wp.digitalWrite(TRIG_PIN, 0)
    
    while wp.digitalRead(ECHO_PIN) == 0:
        start_time = time.time()
    while wp.digitalRead(ECHO_PIN) == 1:
        end_time = time.time()
    
    elapsed_time = end_time - start_time
    distance = (elapsed_time * 34300) / 2  
    return distance

while True:
    desk_to_ceiling = read_distance()
    if desk_to_ceiling is not None:
        print(f"Afstand bureau tot plafond: {desk_to_ceiling:.2f} cm")
    time.sleep(1)
