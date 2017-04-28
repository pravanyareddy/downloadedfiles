import MFRC522
import signal
import time
import RPi.GPIO as GPIO

flag=0
tot_uid = ''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
continue_reading = True
continue_reading1 = True
GPIO_CLEANED_UP = False

def card_1():
   print 'kil'
   global continue_reading
   global flag
   dev='/dev/spidev0.1'
   MIFAREReader = MFRC522.MFRC522(dev,1000000)
   MFRC522.__init__(dev,1000000)
   signal.signal(signal.SIGINT, end_read)
   approved_list=("194866038")
   while continue_reading:     
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (tot_uid)
            if (tot_uid == approved_list):
                print ("Approved")
                turn_sol()              
            else:
		print "Not" 
                           

def end_read(signal,frame):
    global continue_reading
    global continue_reading1
    continue_reading = False
    continue_reading1 = False
    if(GPIO_CLEANED_UP==False):
                GPIO.cleanup()
def card_2():
    print 'pil'
    dev1='/dev/spidev0.0'    
    MFRC522.__init__(dev1,1000000)
    global  continue_reading1
    global flag
    signal.signal(signal.SIGINT, end_read)
    approved_list1=("194866038")
    MIFAREReader = MFRC522.MFRC522(dev1,1000000)
    while continue_reading1:        
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:            
		print 'Connecting to server'    
        (status,uid) = MIFAREReader.MFRC522_Anticoll()      
        if status == MIFAREReader.MI_OK:                
            tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print tot_uid
            if (tot_uid in approved_list1):
                print ("Approved1")
            else:
		print 'Not1'
#card_1()  
def turn_sol():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(35, GPIO.OUT)
  m=0
  while(m==0):
    GPIO.output(35, 1)
    time.sleep(2)
    print 'on'
    GPIO.output(35, 0)
    print'off'
    card_2()
def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    x=0
    while x==0:	    
	    GPIO.output(19, 1)
            GPIO.output(21, 1)
            print 'ab'
	    card_1()
	    time.sleep(2)
#            x+=1
	    GPIO.output(19, 0)
	    GPIO.output(21, 0)
            print 'cd'
            card_2()
            pass
if __name__ == '__main__':

  try:
     main()
  except KeyboardInterrupt:
    pass
  finally:
        GPIO.cleanup()

