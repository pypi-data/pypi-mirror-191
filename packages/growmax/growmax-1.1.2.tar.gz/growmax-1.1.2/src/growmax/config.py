import machine

# Wi-Fi SSID and password
WIFI_ENABLED = False
WIFI_SSID = "SSID"
WIFI_PASSWORD = ""


# Threshold value for moisture sensor (range 0-28)
# Note: you may set value per plant by assigning an array length 8, Ex: [7, 7, 10, 8, 9, 12, 13, 10]
SOIL_WET_THRESHOLD = 10

# Water Sensor Pins
# (GP21 and GP22 ports have voltage dividers 4V -> ~3.3V to pair with Optomax Digital Liquid Level Sensors)
WATER_SENSOR_LOW_ENABLED = True
WATER_SENSOR_LOW = 22
WATER_SENSOR_HIGH_ENABLED = False  # Not yet implemented
WATER_SENSOR_HIGH = 21  # Not yet implemented

# Pump settings
PUMP_WHEN_DRY = True
PUMP_CYCLE_DURATION = 30  # seconds -- avoid long pump times as it does not check if reservoir is low while pumping!


# Auxiliary Sensors settings
ADAFRUIT_SCD4X_ENABLED = False
ADAFRUIT_SCD4X_I2C_CHANNEL = 0  # 0 for QWIIC_I2C0 or 1 for QWIIC_I2C1

# I2C Displays
DISPLAY = None   # To enable a display, define an import from growmax.displays, Ex: "SSD1327_I2C"
DISPLAY_I2C_CHANNEL = 0  # 0 for QWIIC_I2C0 or 1 for QWIIC_I2C1
DISPLAY_I2C_ADDRESS = None  # The address of the display
DISPLAY_SWITCH = None  # Set GPIO Pin number of the input switch
DISPLAY_SWITCH_PULL = None  # Set to be None, machine.Pin.PULL_UP or machine.Pin.PULL_DOOWN
DISPLAY_SWITCH_TRIGGER = machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING

# Data collection w/ api.opensensor.io (early alpha testing)
OPEN_SENSOR_COLLECT_DATA = False  # Please don't enable this for now
OPEN_SENSOR_API_KEY = None  # Not yet supported
DEVICE_NAME = ""
