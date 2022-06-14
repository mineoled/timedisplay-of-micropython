# timedisplay-of-micropython
使用esp8266作为开发底板

micropython初学成品

功能：
1.天气预报（心知天气api）
2.温湿度传感（dht11）
3.整点/半点报时（22-6点不报）
4.不联网使用（ds1302）
5.oled屏显示（ssd1306）
字体文件来自 https://gitee.com/walkline/micropython-new-fontlib#https://gitee.com/walkline/fontmaker-client

默认接线顺序：
#dht11数据引脚--->d0
#oled sda --->d2
#oled scl --->d1
#ds1302 clk ---d5
#ds1302 dat ---d7
#ds1302 cs ---d6

