#Import libraries
import os, threading, time, datetime
import RPi.GPIO as GPIO
from recorder import Recorder

#Initialize GPIO
GPIO.setmode(GPIO.BOARD)
startstop_switch=16
fault_switch=18
led_out=22
GPIO.setup(startstop_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fault_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.setup(led_out, GPIO.OUT)
GPIO.output(led_out,0)

#Initialize Recorder
rec = Recorder(channels=2)
recfile = None
recordStatus = False
interval=300 #5 minutes

#Function write to text file
def writeLog(message):
    print(message)
    with open("recording_log.txt", "a") as f:
        f.write(message+'\n')
    
#Function to determen the filename
def getFilename():
    i=1
    filename = 'qcontrole_'+str(i).zfill(3)+'.wav'
    while(os.path.isfile('/home/pi/'+filename)):
        i += 1
        filename = 'qcontrole_'+str(i).zfill(3)+'.wav'        
    return filename

#Function to start recording
def startRecording():
    global recfile, t
    filename = getFilename()
    recfile = rec.open(filename, 'wb')
    writeLog('Start recording to '+filename+' - '+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    recfile.start_recording()
    GPIO.output(led_out,1)
    
#Function to stop recording an write the file
def stopRecording():
    global recfile, t
    recfile.stop_recording()
    recfile.close()
    GPIO.output(led_out,0)
    
#Timer callback function
def nextFile():
    if(recordStatus):
        stopRecording()
        time.sleep(1)
        startRecording()
        t = threading.Timer(interval, nextFile)
        t.start()
    
#Callback function for start/stop recording switch
def startstop_callback(channel):
    global recordStatus, t
    if(GPIO.input(startstop_switch)):
            recordStatus = not recordStatus
            if(recordStatus):
                startRecording()
                t = threading.Timer(interval, nextFile)
                t.start()
            else:
                stopRecording()
                writeLog("Stop recording")
                t.cancel()
                
#Callback function for fault switch
def fault_callback(channel):
    writeLog('Fault registered - '+datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

#Add callback function to gpio event
GPIO.add_event_detect(startstop_switch, GPIO.RISING, callback=startstop_callback, bouncetime=500)
GPIO.add_event_detect(fault_switch, GPIO.RISING, callback=fault_callback, bouncetime=500)

#Set threading
t = threading.Timer(interval, nextFile)

#Loop until exit with keyboard
while(True):
    pass 
    
GPIO.cleanup()
t.cancel()
