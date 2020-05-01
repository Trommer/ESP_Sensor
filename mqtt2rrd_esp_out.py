#!/usr/bin/env python
import paho.mqtt.client as mqtt
import os

temperature = "0"
dewpoint = "0"
humidity_abs = "0"
humidity = "0"
pressure_rel = "0"
pressure = "0"
calls = 1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("/esp/out/#")

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    
    global temperature 
    global dewpoint
    global humidity_abs
    global humidity
    global pressure_rel
    global pressure
    global calls

    if (msg.topic.find("temperature") != -1): 
        temperature = str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (temperature)
    
    if (msg.topic.find("dewpoint") != -1): 
        dewpoint = str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (dewpoint)
    
    if (msg.topic.find("humidity_abs") != -1): 
        humidity_abs = str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (humidity_abs)
    elif (msg.topic.find("humidity") != -1): 
        humidity = str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (humidity)
    
    if (msg.topic.find("pressure_rel") != -1): 
        pressure_rel =str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (pressure_rel)
    elif (msg.topic.find("pressure") != -1): 
        pressure = str(msg.payload)[2:len(str(msg.payload)) -1]
        #print (pressure)
        #print (calls)

    if calls < 7:
        print ("Aufruf " + str(calls) + " - Topic " + str(msg.topic))
        calls = calls + 1
    if calls == 7:
        topics = ["temperature", "dewpoint", "humidity_abs", "humidity", "pressure_rel", "pressure"]
        meas = ["avg", "max", "min"]
        os.system('sudo rrdtool update /var/rrd/weather.rrd N:' + temperature + ':' + dewpoint + ':' + humidity_abs + ':' + humidity + ':' + pressure + ':' + pressure_rel + '')
        for topic in topics:
            os.system('sudo rrdtool graph /var/www/html/graph_' + topic +'_out_12h.png --title ' + topic + ' --width 600 --height 200 --start end-12h DEF:' + topic + '_avg=/var/rrd/weather.rrd:' + topic +':AVERAGE DEF:' + topic + '_min=/var/rrd/weather.rrd:'+ topic +':MIN DEF:' + topic +'_max=/var/rrd/weather.rrd:'+ topic +':MAX LINE1:'+ topic +'_avg#0000FF GPRINT:'+ topic +'_avg:LAST:" Aktuell\:%8.2lf %s" GPRINT:'+ topic +'_max:MAX:"Maimalwert\:%8.2lf %s" GPRINT:'+ topic +'_min:MIN:"Minimalwert\:%8.2lf %s"')
            os.system('sudo rrdtool graph /var/www/html/graph_' + topic +'_out_1d.png --title ' + topic + ' --width 600 --height 200 --start end-1d DEF:' + topic + '_avg=/var/rrd/weather.rrd:' + topic +':AVERAGE DEF:' + topic + '_min=/var/rrd/weather.rrd:'+ topic +':MIN DEF:' + topic +'_max=/var/rrd/weather.rrd:'+ topic +':MAX LINE1:'+ topic +'_avg#0000FF GPRINT:'+ topic +'_avg:LAST:" Aktuell\:%8.2lf %s" GPRINT:'+ topic +'_max:MAX:"Maimalwert\:%8.2lf %s" GPRINT:'+ topic +'_min:MIN:"Minimalwert\:%8.2lf %s"')
            os.system('sudo rrdtool graph /var/www/html/graph_' + topic +'_out_1w.png --title ' + topic + ' --width 600 --height 200 --start end-1w DEF:' + topic + '_avg=/var/rrd/weather.rrd:' + topic +':AVERAGE DEF:' + topic + '_min=/var/rrd/weather.rrd:'+ topic +':MIN DEF:' + topic +'_max=/var/rrd/weather.rrd:'+ topic +':MAX LINE1:'+ topic +'_avg#0000FF GPRINT:'+ topic +'_avg:LAST:" Aktuell\:%8.2lf %s" GPRINT:'+ topic +'_max:MAX:"Maimalwert\:%8.2lf %s" GPRINT:'+ topic +'_min:MIN:"Minimalwert\:%8.2lf %s"')
            os.system('sudo rrdtool graph /var/www/html/graph_' + topic +'_out_1m.png --title ' + topic + ' --width 600 --height 200 --start end-1m DEF:' + topic + '_avg=/var/rrd/weather.rrd:' + topic +':AVERAGE DEF:' + topic + '_min=/var/rrd/weather.rrd:'+ topic +':MIN DEF:' + topic +'_max=/var/rrd/weather.rrd:'+ topic +':MAX LINE1:'+ topic +'_avg#0000FF GPRINT:'+ topic +'_avg:LAST:" Aktuell\:%8.2lf %s" GPRINT:'+ topic +'_max:MAX:"Maimalwert\:%8.2lf %s" GPRINT:'+ topic +'_min:MIN:"Minimalwert\:%8.2lf %s"')
            os.system('sudo rrdtool graph /var/www/html/graph_' + topic +'_out_1y.png --title ' + topic + ' --width 600 --height 200 --start end-1y DEF:' + topic + '_avg=/var/rrd/weather.rrd:' + topic +':AVERAGE DEF:' + topic + '_min=/var/rrd/weather.rrd:'+ topic +':MIN DEF:' + topic +'_max=/var/rrd/weather.rrd:'+ topic +':MAX LINE1:'+ topic +'_avg#0000FF GPRINT:'+ topic +'_avg:LAST:" Aktuell\:%8.2lf %s" GPRINT:'+ topic +'_max:MAX:"Maimalwert\:%8.2lf %s" GPRINT:'+ topic +'_min:MIN:"Minimalwert\:%8.2lf %s"')
        #os.system('sudo rrdtool graph /var/www/html/graph_dewpoint_1d.png --title Taupunkt --width 600 --height 200 --start end-1d DEF:dewpoint_avg=/var/rrd/weather.rrd:dewpoint:AVERAGE DEF:dewpoint_min=/var/rrd/weather.rrd:dewpoint:MIN DEF:dewpoint_max=/var/rrd/weather.rrd:dewpoint:MAX LINE1:dewpoint_avg#000000 LINE1:dewpoint_min#0033CC LINE1:dewpoint_max#FF0000')
        print ("Update erfolgt")
        exit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqtt", "12345")
client.connect("localhost", 1883, 60)

client.loop_forever()
