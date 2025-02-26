import time
from w1thermsensor import W1ThermSensor, Sensor

# Initialize the sensor
sensor = W1ThermSensor(sensor_type=Sensor.DS18B20)

while True:
    try:
        # Read temperature
        temperature_celsius = sensor.get_temperature()
        temperature_fahrenheit = temperature_celsius * 9.0 / 5.0 + 32.0

        # Print the temperature
        print(f"\tTemperature: {temperature_celsius:.2f} °C / {temperature_fahrenheit:.2f} °F", end = '\r')
    except Exception as e:
        print(e, end = '\r')
    # Wait for 1 second before reading again
    time.sleep(1)
