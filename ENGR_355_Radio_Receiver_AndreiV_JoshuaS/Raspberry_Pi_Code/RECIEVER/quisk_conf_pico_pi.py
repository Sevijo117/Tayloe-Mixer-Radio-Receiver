# OpenRadio v1.1 Quisk Configuration File
# 
# IMPORTANT: To be able to control the OpenRadio board from within Quisk,
# you will need to compile and upload the 'openradio_quisk' firmware, which
# is available from: https://github.com/darksidelemm/open_radio_miniconf_2015
#
# You will also need to install the pyserial package for python.
#

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


# SOUND CARD SETTINGS
#
# Uncomment these if you wish to use PortAudio directly
#name_of_sound_capt = "portaudio:(hw:2,0)"
#name_of_sound_play = "portaudio:(hw:1,0)"

# Uncomment these lines if you wish to use Pulseaudio
name_of_sound_capt = "pulse"
name_of_sound_play = "pulse"


# OpenRadio Frequency limits.
# These are just within the limits set in the openradio_quisk firmware.
openradio_lower = 3800000
openradio_upper = 30000000

# OpenRadio Hardware Control Class
#
import serial,time
from quisk_hardware_model import Hardware as BaseHardware

class Hardware(BaseHardware):
  def open(self):
    # SERIAL PORT SETTINGS
    # Set this as appropriate for your OS.
    openradio_serial_port = "/dev/ttyUSB0"
    openradio_serial_rate = 57600
    # Called once to open the Hardware
    # Open the serial port.
    try:
    	self.or_serial = serial.Serial(openradio_serial_port,openradio_serial_rate,timeout=3)
    except serial.serialutil.SerialException:
       openradio_serial_port = "/dev/ttyDummy" # Set to the port for interceptty.
       # To run interceptty: $ interceptty /dev/ttyACM0 /dev/ttyDummy
    try:
    	self.or_serial = serial.Serial(openradio_serial_port,openradio_serial_rate,timeout=3)
    except serial.serialutil.SerialException:
    	openradio_serial_port = "/dev/ttyUSB1" # Set to the second serial port for your OS.
    try:
    	self.or_serial = serial.Serial(openradio_serial_port,openradio_serial_rate,timeout=3)
    except serial.serialutil.SerialException:
       openradio_serial_port = "/dev/ttyACM0" # Set to the third serial port for your OS.
    try:
    	self.or_serial = serial.Serial(openradio_serial_port,openradio_serial_rate,timeout=3)
    except serial.serialutil.SerialException:
       openradio_serial_port = "/dev/ttyACM1" # Set to the third serial port for your OS.
    try:
    	self.or_serial = serial.Serial(openradio_serial_port,openradio_serial_rate,timeout=3)
    except serial.serialutil.SerialException:
    	print ("Radio not connected")
    	raise
    print("Opened Serial Port.")
    # Wait for the Arduino Nano to restart and boot.
    time.sleep(2)
    # Poll for version. Should probably confirm the response on this.
    version = str(self.get_parameter("VER"))
    print("This should be the version printed next.")
    print(version)
    # Return an informative message for the config screen
    t = version + ". Capture from sound card %s." % self.conf.name_of_sound_capt
    return t

  def close(self):      
    # Called once to close the Hardware
    self.or_serial.close()

  def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
    # Called whenever quisk requests a frequency change.
    # This sends the FREQ command to set the centre frequency of the OpenRadio,
    # and will also move the 'tune' frequency (the section within the RX passband
    # which is to be demodulated) if it falls outside the passband (+/- sample_rate/2).
    print("Setting VFO to %d." % vfo)
    if(vfo<openradio_lower):
      vfo = openradio_lower
      print("Outside range! Setting to %d" % openradio_lower)

    if(vfo>openradio_upper):
      vfo = openradio_upper
      print("Outside range! Setting to %d" % openradio_upper)

    # success = self.set_parameter("FREQ",str(vfo))
    self.set_parameter("FREQ",str(vfo))

    print("sample_rate =")
    print(sample_rate)
    # If the tune frequency is outside the RX bandwidth, set it to somewhere within that bandwidth.
    if(tune>(vfo + sample_rate/2) or tune<(vfo - sample_rate/2)):
      tune = vfo + 10000
      print("Bringing tune frequency back into the RX bandwidth.")

    # if success:
    #   print("Frequency change succeeded!")
    # else:
    #   print("Frequency change failed.")

    return tune, vfo

#
# Serial comms functions, to communicate with the Pi Pico board
#

  def get_parameter(self,string):
    string = string + "\n"
    self.or_serial.write(string.encode())
    return self.get_argument()
    #return string.encode()
        
  def set_parameter(self,string,arg):
    string = string+","+arg+"\r"+"\n"
    self.or_serial.write(string.encode())
    print('arg is: ', arg)
    temp_arg = self.get_argument()
    print('temp_arg is: ', temp_arg)
    return True
    # if temp_arg == arg:
    #   return True
    # else:
    #   return False
    
  def get_argument(self):
    data1 = self.or_serial.readline()
    # Do a couple of quick checks to see if there is useful data here
    if len(data1) == 0:
       return -1
        
    # Maybe we didn't catch an OK line?
    if data1.startswith(b'OK'):
       data1 = self.or_serial.readline()
       print('Received: ', data1)
        
    # Check to see if we have a comma in the string. If not, there is no argument.
    if data1.find(b',') == -1:
       return -1
    
    data1 = data1.split(b',')[1].rstrip(b'\r\n')
    print("data1 =")
    print(data1)
    
    # Check for the OK string
    data2 = self.or_serial.readline()
    if data2.startswith(b'OK'):
       return data1
