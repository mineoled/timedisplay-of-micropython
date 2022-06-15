#https://github.com/mineoled/timedisplay-of-micropython
#by @mineoled 2022
#感谢GitHub，gtee等平台对开源的支持
import network
from machine import RTC
import ntptime
import network
import dht
import machine
import time
from machine import Pin, I2C
from SSD1306 import SSD1306_I2C
from machine import Timer
import gc
gc.enable()

import machine
d = dht.DHT11(machine.Pin(16))
import DS1302
ds = DS1302.DS1302(Pin(14),Pin(13),Pin(12))
global online_status

# CLK 1
# DAT 2
# RST 3
print(ds.DateTime())

scl = Pin(5, Pin.OUT)  #OLED屏的SCL管脚接GPIO12管脚
sda = Pin(4, Pin.OUT)  #OLED屏的SCL管脚接GPIO14管脚
i2c = I2C(scl=scl, sda=sda)
oled = SSD1306_I2C(128, 64, i2c)
sta_if = network.WLAN(network.STA_IF)

#默认接线顺序：
#dht11数据引脚--->d0
#oled sda --->d2
#oled scl --->d1
#ds1302 clk ---d5
#ds1302 dat ---d7
#ds1302 cs ---d6

ssid=""
password=""
apisc=""
loacation="beijing"
#loacation填中文或拼音均可，用于天气预报

def do_connect(ssid,password):
    
    
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid,password)
        try_time=0
        while not sta_if.isconnected():
            if try_time > 10:
                
                break
            else:
                try_time += 1
                time.sleep(0.5)
                print("尝试时间"+str(try_time))
                pass
    print('network config:', sta_if.ifconfig())
    



def sync_ntp():
    ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
    ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
    try:
         ntptime.settime()  # 修改设备时间,到这就已经设置好了
    except:
         pass
    rtc = RTC()
    year=rtc.datetime()[0]
    month=rtc.datetime()[1]
    date=rtc.datetime()[2]
    weekday=rtc.datetime()[3]
    time=rtc.datetime()[4]
    minute=rtc.datetime()[5]
    second=rtc.datetime()[6]
    ds.start()
    ds.Year(year) #获取今天的年份
    ds.Month(month) #获取今天的月份
    ds.Day(date)
    #获取今天的日期
    ds.Weekday(weekday) #获取当前周几
    ds.Hour(time) #获取当前小时
    ds.Minute(minute) #获取当前分钟
    ds.Second(second) #获取当前的秒
    print("同步成功")
    return True

def get_time_string():
    
    rtc = RTC()
    year=rtc.datetime()[0]
    month=rtc.datetime()[1]
    date=rtc.datetime()[2]
    time=rtc.datetime()[4]
    minute=rtc.datetime()[5]
    second=rtc.datetime()[6]
    weekday=rtc.datetime()[3]
    xq="一"
    if weekday == 1:
        xq="天"
    elif weekday ==2:
        xq="一"
    elif weekday == 3:
        xq="二"
    elif weekday ==4:
        xq="三"
    elif weekday == 5:
        xq="四"
    elif weekday == 6:
        xq="五"
    elif weekday == 7:
        xq="六"
    totals=str(month)+"月"+str(date)+"日"+"星期"+xq+"\n"+str(time)+"时"+str(minute)+"分"+str(second)+"秒"
    return totals

def init_clock():
    
    year=ds.Year() #获取今天的年份
    month=ds.Month() #获取今天的月份
    date=ds.Day() #获取今天的日期
    weekday=ds.Weekday() #获取当前周几
    time=ds.Hour() #获取当前小时
    minute=ds.Minute() #获取当前分钟
    second=ds.Second()
    rtc = RTC()
    rtc.datetime((year, month, date,weekday, time, minute, second, 0))
do_connect(ssid,password)


    


now = 0
page=0
wait=0
i=0
def baoshi (get):
    rtc = RTC()
    second=rtc.datetime()[6]
    time=rtc.datetime()[4]
    minute=rtc.datetime()[5]
    if time >= 6 and time <= 23:
        if  minute == 0 and second == 0:
            musicon(1)
            print("整点报时"+str(rtc.datetime()[4])+"点")
        elif minute == 30 and second == 0 :
            musicon(2)
            print("半点报时"+str(rtc.datetime()[4])+"点")
def musicon(status):
    from machine import Pin,PWM
    import time
    import buzzer
    import uasyncio as asyncio
    zhengdian=[(1,"1"),(1/2,"2"),(1,"1"),(1/2,"5")]
    bandian=[(1/2,"1"),(1/4,"5"),(1/2,"1"),(1/4,"2")]
    buzzer=buzzer.Buzzer(PWM(Pin(2)))
    
    if status == 1:
        buzzer.play(zhengdian,tempo=74,freq_multiple=1,output=0)
    elif status == 2:
        buzzer.play(bandian,tempo=74,freq_multiple=1,output=0)
    return True
global firstday
global secondday
firstday =""
secondday =""
def get_weather():
    import urequests
    global firstday
    global secondday
    Url = 'https://api.seniverse.com/v3/weather/daily.json?key='+apisc+'&location='+loacation+'&language=zh-Hans&unit=c&start=1&days=3'
    r = urequests.get(Url)
    next1=r.json()['results'][0]['daily'][0]
    next2=r.json()['results'][0]['daily'][1]
    
    firstday=next1["date"]+"\n"+next1["text_day"]+"\n"+"最高温度"+next1["high"]+"\n"+"最低温度"+next1["low"]
    secondday=next2["date"]+"\n"+next2["text_day"]+"\n"+"最高温度"+next2["high"]+"\n"+"最低温度"+next2["low"]
    print(firstday)
if not sta_if.isconnected():
    print("检测无网")
    init_clock()
    online_status = False
else:
    online_status = True
    get_weather()
    sync_ntp()

tim = Timer(-1)
tim.init(period=300, mode=Timer.PERIODIC, callback=baoshi)
while True:
    global firstday
    global secondday
    if not sta_if.isconnected():
        online_status = False
        
    if sta_if.isconnected() and online_status == False:
        online_status = True
        get_weather()
        sync_ntp()
        
        
    if now == 360:
        if not sta_if.isconnected():
            print("检测无网")
            init_clock()
            do_connect()
        else:
            online_status = True
            get_weather()
            sync_ntp()
            now = 0
   
    def page1():
        
        oled.fill(0)
        print(get_time_string())
        if not sta_if.isconnected():
            oled.hz(get_time_string()+"\n"+str(360-now)+"秒后同步\n"+"当前未联网 "+str(i))
        elif sta_if.isconnected():
            oled.hz(get_time_string()+"\n"+str(360-now)+"秒后同步\n"+"当前已联网 "+str(i))

        print("当前"+str(i)+","+str(page))
    def page2():
        oled.fill(0)
        d.measure()
        temp="温度"+str(d.temperature())
        hum="湿度:"+str(d.humidity())
        oled.hz(temp+"\n"+hum+"\n\n"+str(i))
        print("当前"+str(i)+","+str(page))
    def page3():
        oled.fill(0)
        if firstday=="":
            page = 0
            i = 0
        else:
            oled.hz(firstday)
    def page4():
        oled.fill(0)
        if secondday=="":
            page = 0
            i = 0
        else:
            oled.hz(secondday)
      
        
    if page == 0 and i <= 10:
        page1()
        page = 1
    elif page == 1 and i <= 10:
        page1()
    elif page == 1 and i > 10:
        page2()
        page =2
    elif page == 2 and i <= 20:
        page2()    
    elif page == 2 and i > 20:
        page =3
        page3()
    elif page == 3 and i <= 30:
        page3()
   
        
        
    elif page == 3 and i > 30:
        page =4
        page4()
    elif page == 4 and i <= 40:
        page4()
    elif page == 4 and i > 40:
        i=0
        page = 0
    i=i+1
    now=now+1
    oled.show()
    gc.collect()
    time.sleep_ms(700)
