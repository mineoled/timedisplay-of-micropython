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
buzzer库来自https://github.com/Wind-stormger/micropython-uasycio-buzzer

默认接线顺序：


#dht11数据引脚--->d0


#oled sda --->d2


#oled scl --->d1


#ds1302 clk ---d5


#ds1302 dat ---d7


#ds1302 cs ---d6


（可能有误，以代码为准）

# 如何使用
首先
```
git clone https://github.com/mineoled/timedisplay-of-micropython
```

1.在esp8266/esp32/pyboard板中烧录micropython固件

2.打开项目文件，修改main.py

ssid="" #wifi名称

password="" #wifi密码

apisc="" #api密钥

loacation="" #天气预报用，地点

3.使用项目中的upload.sh(未验证可用性)或upload.bat进行上传代码，

或自行上传
