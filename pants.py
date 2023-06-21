from sense_emu import SenseHat
import signal
import time
import requests

sense = SenseHat()

def send_signal():
  sense.set_pixel(7, 7, [255, 0, 0])
  
def clear_signal():
  sense.set_pixel(7, 7, [125, 125, 125])

def pants_signal():
  sense.set_pixel(7, 7, [0, 255, 0])

clear_signal()

def end_read(signal, frame):
  print("Ctrl+C captured, ending read.")
  sense.clear()

signal.signal(signal.SIGINT, end_read)

while True:
  temperature = sense.get_temperature()
  humidity = sense.get_humidity()
  
  if temperature > 30 and temperature < 40 and humidity > 30 and humidity < 40:
    clear_signal()
    time.sleep(5)
    tag_id_input = input("Enter the ID of the RFID tag on the protective pants: ")
    tag_id = [x for x in tag_id_input.split(",")]
    
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    url = 'http://localhost:5000/incident'

    data = {
        "worn": False,
        "time": current_time
    }

    if tag_id == ["0xAD22"]:
      pants_signal()
      data["worn"] = True
      with open("signals.txt", "a") as f:
        f.write("Protective pants worn at {}\n".format(current_time))

    else:
      send_signal()
      data["worn"] = False
      with open("signals.txt", "a") as f:
        f.write("Pants not worn at {}\n".format(current_time))
    
    response = requests.post(url, json=data)

    if response.status_code == 201:
        print("Incident added successfully!")
    else:
        print("Failed to add incident.")
  else:
    continue
    
  time.sleep(5)

