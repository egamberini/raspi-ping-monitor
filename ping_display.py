from pythonping import ping
from collections import deque
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

q60 = deque(maxlen=60)
q300 = deque(maxlen=300)

while True:
  try:
    response_list = ping('sfr.fr', count=3, verbose=False, size=52)
    t = int(round(response_list.rtt_avg_ms, 0))
    q60.append(t)
    q300.append(t)
    max60 = max(list(q60))
    max300 = max(list(q300))

    lcd.clear()
    msg = '{:>4} {:>5} {:>5}'.format('Now', 'Max1', 'Max5')
    msg = msg+'\n{:>4} {:>5} {:>5}'.format(str(t), str(max60), str(max300))
    lcd.message = msg #'Now: ' + str(t) + '\nMax: ' + str(max60) + '  ' + str(max300)
  except Exception as e:
    print(e)
  time.sleep(1)
