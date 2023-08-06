from rpithingamajigs.chardisplay import Display
import logging
import smbus
import time

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

class I2C1602Display(Display):
    """I2C1602Display implements a driver for 16x2 LCD displays connected via the I2C bus."""
    def __init__(self, name):
        super().__init__(name)
        lcd_init()

    def configure(self, settings):
        i2c_address_string = settings.get('i2c_bus_address', '0x27')
        i2c_address = int(i2c_address_string, 16)
        
        global I2C_ADDR
        I2C_ADDR = i2c_address
        logging.info('Display I2C bus address: {}'.format(i2c_address))

    def dimensions(self):
        return (16, 2)

    def message(self, lines):
        columns, _ = self.dimensions()
        for lcd_line in [ LCD_LINE_1, LCD_LINE_2 ]:
            line = lines.pop(0) if lines else ""
            lcd_string(line[:columns], lcd_line)

    def clear(self):
        lcd_byte(0x01, LCD_CMD)

class I2C2004Display(Display):
    """I2C1602Display implements a driver for 16x2 LCD displays connected via the I2C bus."""
    def __init__(self, name):
        super().__init__(name)
        global LCD_WIDTH
        LCD_WIDTH=20
        lcd_init()

    def configure(self, settings):
        i2c_address_string = settings.get('i2c_bus_address', '0x27')
        i2c_address = int(i2c_address_string, 16)

        global I2C_ADDR
        I2C_ADDR = i2c_address
        logging.info('Display I2C bus address: {}'.format(i2c_address))

    def dimensions(self):
        return (20,4)

    def message(self, lines):
        columns, _ = self.dimensions()
        for lcd_line in [ LCD_LINE_1, LCD_LINE_2, LCD_LINE_3, LCD_LINE_4 ]:
            line = lines.pop(0) if lines else ""
            lcd_string(line[:columns], lcd_line)

    def clear(self):
        lcd_byte(0x01, LCD_CMD)
