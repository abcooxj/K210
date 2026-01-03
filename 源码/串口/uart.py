#调用需要使用到的库文件
from machine import UART
from Maix import GPIO
from fpioa_manager import fm
import utime

#映射UART2的两个引脚
fm.register(GPIO.GPIOHS9, fm.fpioa.UART2_TX)
fm.register(GPIO.GPIOHS10, fm.fpioa.UART2_RX)

#初始化串口，返回调用句柄 (8个数据位，无校验，1个停止位)
uart_A = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

#定义一个要发送的字符串 (注意：UART write需要的是bytes类型)
write_data = 'get dat\r\n'.encode('utf-8')

#主循环
while(True):
    # 尝试读取最多 10 个字节的数据
    read_data = uart_A.read(10)

    # 判断是否成功接收到数据 (read() 未读到数据时返回 None)
    if read_data is not None:
        try:
            # 将接收到的 bytes 数据解码成字符串进行打印
            read_str = read_data.decode('utf-8')
            print("Received Data:", read_str.strip())

            # 接收到数据后返回信息
            uart_A.write(write_data)
            print("Sent Reply:", write_data.decode('utf-8').strip())

        except UnicodeError:
            # 捕获解码错误，打印原始 bytes
            print("Received unknown bytes (Decode Error):", read_data)

    # 统一延时，减少 CPU 占用
    utime.sleep_ms(200)
