import wiringpi as wp
import time

LDR_PIN = 1  # GPIO-pin waarop de LDR is aangesloten
LED_PIN = 2  # GPIO-pin waarop de LED is aangesloten

wp.wiringPiSetup()
wp.pinMode(LDR_PIN, 0)  # Zet pin als input voor LDR
wp.pinMode(LED_PIN, 1)  # Zet pin als output voor LED

while True:
    # 1. Ontladen van de condensator
    wp.pinMode(LDR_PIN, 1)  # Output mode
    wp.digitalWrite(LDR_PIN, 0)  # Zet de pin laag (GND)
    time.sleep(0.1)  # Wacht 0.1s om de condensator te ontladen

    # 2. Start met opladen van de condensator
    wp.pinMode(LDR_PIN, 0)  # Zet de pin als input
    start_time = time.time()  # Starttijd vastleggen

    # 3. Wachten tot de condensator is opgeladen
    while wp.digitalRead(LDR_PIN) == 0:
        pass  # Blijf wachten

    stop_time = time.time()  # Stoptijd vastleggen
    interval = (stop_time - start_time) * 1000 * 1000

    print(f"Lichtwaarde: {interval:.2f}")

    # 4. Controleer de lichtwaarde en zet de LED aan of uit
    if interval > 1200:
        print("Geen licht")
    else:
        print("Licht gedetecteert")

    time.sleep(1)  # Wacht 1 seconde voor de volgende meting