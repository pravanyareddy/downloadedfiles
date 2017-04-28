import MFRC522
import signal
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
continue_reading = True
#MIFAREReader = MFRC522.MFRC522()
dev='/dev/spidev0.0'
MIFAREReader = MFRC522.MFRC522(dev,1000000)
MFRC522.__init__(dev,1000000)

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
#MIFAREReader = MFRC522.MFRC522()
approved_list=("136418657")
# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."
while continue_reading:

    # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
           # lcd_string("Card Detected",LCD_LINE_1)


    # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            print uid
            print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print (tot_uid)
            if (tot_uid in approved_list):
                print ("Approved")
                exit(1)
	    else:
		print "Not"
	        pass
#        else:
#            print ("Not Approved")
#            time.sleep(2)
GPIO.cleanup()                


