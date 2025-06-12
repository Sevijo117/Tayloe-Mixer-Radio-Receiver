from machine import Pin
from radio import Radio
import si5351

synth = si5351.SI5351( data=Pin(3), clock=Pin(2), addr=0x60 )

r = Radio( synth, 7000000 )
r.run()
