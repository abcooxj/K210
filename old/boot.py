import utime
from machine import Timer,UART
from fpioa_manager import fm
from Maix import GPIO
io_led_greed = 12
io_led_red   = 13
io_led_blue  = 14
io_boot_key  = 16
io_uart1_tx  = 24
io_uart1_rx  = 25
fm.register(io_led_greed,fm.fpioa.GPIO0)
fm.register(io_led_red,  fm.fpioa.GPIO1)
fm.register(io_led_blue, fm.fpioa.GPIO2)
fm.register (io_boot_key,fm.fpioa.GPIOHS0)
fm.register (io_uart1_tx, fm.fpioa.UART1_TX,force=True)
fm.register (io_uart1_rx, fm.fpioa.UART1_RX, force=True)
led_g=GPIO(GPIO.GPIO0,GPIO.OUT)
led_r=GPIO(GPIO.GPIO1,GPIO.OUT)
led_b=GPIO(GPIO.GPIO2,GPIO.OUT)
key = GPIO(GPIO.GPIOHS0,GPIO.IN,GPIO.PULL_UP)
uart_A = UART(UART.UART1, 9600,timeout = 1000,read_buf_len = 4096)
led_g.value (1)
led_r.value (1)
led_b.value (1)
uart_send_str = 'hello world'
led_state = False
key_state = False
def test_irq(key):
	global key_state
	key_state = True
while(1):
	key.irq(test_irq,GPIO.IRQ_FALLING )
	read_data = uart_A.read()
	if read_data:
		read_str = read_data.decode('utf-8')
		uart_A.write(read_str)
		if read_str == "led_turn":
			 print("led_turn")
			 led_state = not led_state
			 led_b.value(led_state)
	if key_state:
		key_state = False
		uart_A.write("@LED_ON\r\n")
