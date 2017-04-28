import RPi.GPIO as GPIO
import time
import random
import getpass
import MFRC522
import signal
flag=0
tot_uid = ''
continue_reading = True
GPIO_CLEANED_UP  = False
PINNum=1234
PINNum1=9876
print "Manju's Pin:",PINNum
print "Puja's Pin:",PINNum1
OTP= random.randint(1000,2000)
print "OTP:",OTP    
def end_read(signal,frame):

    global continue_reading
    continue_reading = False
    if(GPIO_CLEANED_UP==False):
                GPIO.cleanup()
def Rasp_Card():
    sep1='/dev/spidev0.1'
    MFRC522.__init__(sep1,1000000)
    global  continue_reading
    global flag
    cycle_list=("8620524048","1344723848", "8620524048", "21414324948", "86924748", "198424648", "3816924448")
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522(sep1,1000000)    
    while continue_reading:                
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
        if status == MIFAREReader.MI_OK:                            
  		print "Card Detected"

        else:
		Berry_Card()
        (status,uid) = MIFAREReader.MFRC522_Anticoll()      
        if status == MIFAREReader.MI_OK:      
              tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
              print tot_uid

	      if (tot_uid in cycle_list):
                print ("Approved")
                lcd_string("   CYCLE LOCKED     ",LCD_LINE_1,2)
                lcd_string("                    ",LCD_LINE_2,2)
                lcd_string("                    ",LCD_LINE_3,2)
                lcd_string("                    ",LCD_LINE_4,2)
                time.sleep(2)
#		GPIO.output(35, 1)
#		time.sleep(0.2)                     
#		GPIO.output(35, 0)                                        
                lcd_string("    THANK  YOU      ",LCD_LINE_1,2)
		lcd_string("   Hope you had a   ",LCD_LINE_2,2)
                lcd_string("     Great ride!!   ",LCD_LINE_3,2)
                lcd_string("                    ",LCD_LINE_4,2)
		print 'Cycle got locked'
		time.sleep(1)
		main1()
		pass
#	    else:
	      main1()
#                lcd_string("                    ",LCD_LINE_1,2)
#                lcd_string("   Cycle  is  Not   ",LCD_LINE_2,2)
#                lcd_string("  Locked  Properly  ",LCD_LINE_3,2)
#                lcd_string("   Please  Check    ",LCD_LINE_4,2)
#		print 'not locked'
#                pass       
                                                                                                                                                                             
def Condition_card():
	    PINNum=''
            global  continue_reading
            global flag                    
            sep='/dev/spidev0.0'
            MFRC522.__init__(sep,1000000)
            signal.signal(signal.SIGINT, end_read)
            MIFAREReader = MFRC522.MFRC522(sep,1000000)
            approved_list1=("424162162")
            approved_list2=("185163241100")
            approved_list3=("153121243100") 
            approved_list4=("153217232100")
            approved_list5=("48151162")
            approved_list6=("194866038")
#	    GPIO.setmode(GPIO.BOARD)
#	    GPIO.setwarnings(False)
#	    GPIO.setup(35, GPIO.OUT)
            while continue_reading:        
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)    
 	        (status,uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:     
                        tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                        print tot_uid
#			GPIO.output(35, 1)
#			time.sleep(0.2)                     
#			GPIO.output(35, 0)
                                        
                        if (tot_uid in approved_list1):		             
                             lcd_string("      WELCOME      ",LCD_LINE_1,2)                             
                             lcd_string("      Anitha       ",LCD_LINE_2,2)
                             lcd_string("                   ",LCD_LINE_3,2)
                             lcd_string("                   ",LCD_LINE_4,2)                          
                             print "Welcome Anitha"
			     time.sleep(2)
                             turn_sol()
                                             
                        if (tot_uid in approved_list2):			      
                              lcd_string("      WELCOME     ",LCD_LINE_1,2)                              
                              lcd_string("         Z        ",LCD_LINE_2,2)
                              lcd_string("                  ",LCD_LINE_3,2)
                              lcd_string("                  ",LCD_LINE_4,2)   
			      print "Welcome Z"
                              flag=2                                               
                              time.sleep(2)
                              callkeypadDisplay()
                                                                           
                        if (tot_uid in approved_list3):     			     
                             lcd_string("      WELCOME      ",LCD_LINE_1,2)                             
                             lcd_string("      Manjunath    ",LCD_LINE_2,2)
                             lcd_string("                   ",LCD_LINE_3,2)
                             lcd_string("                   ",LCD_LINE_4,2)
			     print "Welcome Manjunath" 
                             time.sleep(2)                                                     			
                             flag=1                             			     
                             callkeypadDisplay()
                                                       
                        if (tot_uid in approved_list4):                             			     			      
                              lcd_string("      WELCOME     ",LCD_LINE_1,2)                            
                              lcd_string("       Puja       ",LCD_LINE_2,2)
                              lcd_string("                  ",LCD_LINE_3,2)
                              lcd_string("                  ",LCD_LINE_4,2)
			      print "Welcome Puja"
                              time.sleep(2)                    			  
                              flag=4
                              callkeypadDisplay()
            
                        if (tot_uid in approved_list5):                                                         
                             lcd_string("      SORRY!      ",LCD_LINE_1,2)
                             lcd_string(" Your card expired",LCD_LINE_2,2)
                             lcd_string("          Y       ",LCD_LINE_3,2)                            
                             lcd_string("                  ",LCD_LINE_4,2)
			     print 'expired'
                             time.sleep(2)
                             main1()
                        if (tot_uid in approved_list6):
                           lcd_string("       SORRY!       ",LCD_LINE_1,2)
                           lcd_string("    INVALID CARD    ",LCD_LINE_2,2)
                           lcd_string("                    ",LCD_LINE_3,2)
                           lcd_string("                    ",LCD_LINE_4,2)
			   print 'invalid card'
                           time.sleep(3)
                           main1()                           
                        else:
                           lcd_string("    USER INVALID    ",LCD_LINE_1,2)                     
                     	   lcd_string("                    ",LCD_LINE_2,2)
                     	   lcd_string("                    ",LCD_LINE_3,2)
                     	   lcd_string("                    ",LCD_LINE_4,2)
			   print 'user invalid'
                           time.sleep(3)
                           main1()  
                else:
   		     #main()
		     Rasp_Card()
             
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 40
LCD_D5 = 32
LCD_D6 = 29
LCD_D7 = 18

LCD_WIDTH = 20    
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

E_PULSE = 0.0005
E_DELAY = 0.0005

def Berry_Card(): 
     Condition_card() 

def main():
   
  lcd_init()
  s=0
  while (True):   
     lcd_string("--------------------",LCD_LINE_1,2)
     lcd_string("     WELCOME TO     ",LCD_LINE_2,2)        
     lcd_string("   CYKUL STATION    ",LCD_LINE_3,2)
     lcd_string("--------------------",LCD_LINE_4,2)     
     print 'welcome'
     time.sleep(2)
     lcd_string("--------------------",LCD_LINE_1,2)
     lcd_string("  PLEASE SCAN YOUR  ",LCD_LINE_2,2)    
     lcd_string("         CARD       ",LCD_LINE_3,2)
     lcd_string("--------------------",LCD_LINE_4,2)
     print 'cycle scan'
     time.sleep(3) 
     Rasp_Card()                          
#     main()                    
def main1():
     
     while True:
	lcd_string("--------------------",LCD_LINE_1,2)
        lcd_string("     WELCOME TO     ",LCD_LINE_2,2)        
        lcd_string("   CYKUL STATION    ",LCD_LINE_3,2)
        lcd_string("--------------------",LCD_LINE_4,2)     
        print 'welcome'
        time.sleep(2)
        lcd_string("--------------------",LCD_LINE_1,2)
        lcd_string("  PLEASE SCAN YOUR  ",LCD_LINE_2,2)    
        lcd_string("         CARD       ",LCD_LINE_3,2)
        lcd_string("--------------------",LCD_LINE_4,2)
        print 'scan'
        time.sleep(2) 	   
	Condition_card()

def lcd_init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(LCD_RS, GPIO.OUT) 
  GPIO.setup(LCD_E, GPIO.OUT) 
  GPIO.setup(LCD_D4, GPIO.OUT) 
  GPIO.setup(LCD_D5, GPIO.OUT) 
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)  
  
  lcd_byte(0x33,LCD_CMD) 
  lcd_byte(0x32,LCD_CMD) 
  lcd_byte(0x06,LCD_CMD) 
  lcd_byte(0x0C,LCD_CMD) 
  lcd_byte(0x28,LCD_CMD) 
  lcd_byte(0x01,LCD_CMD) 

  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
 
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(LCD_RS, GPIO.OUT)  
  GPIO.setup(LCD_E, GPIO.OUT)   
  GPIO.setup(LCD_D4, GPIO.OUT)  
  GPIO.setup(LCD_D5, GPIO.OUT)  
  GPIO.setup(LCD_D6, GPIO.OUT)  
  GPIO.setup(LCD_D7, GPIO.OUT)  
  
  GPIO.output(LCD_RS, mode) 
  
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, 1)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, 1)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, 1)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, 1)
 
  lcd_toggle_enable()
  
  GPIO.output(LCD_D4, 0)
  GPIO.output(LCD_D5, 0)
  GPIO.output(LCD_D6, 0)
  GPIO.output(LCD_D7, 0)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, 1)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, 1)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, 1)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, 1)
 
  lcd_toggle_enable()

def lcd_toggle_enable():
 
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line,style):
  
  if style == 1:
     message = message.ljust(LCD_WIDTH," ")
  elif style == 2:
      message = message.center(LCD_WIDTH," ")
  elif style == 3:
      message = message.rjust(LCD_WIDTH," ")      
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def turn_sol():
      
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(38, GPIO.OUT)
      GPIO.setup(35,GPIO.OUT)
      x=0
      while(x==0):
          GPIO.output(38, 0)
          lcd_string("  CYCLE  UNLOCKED   ",LCD_LINE_1,2)
	  print "Cycle Unlocked"
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  time.sleep(2)
          GPIO.output(35, 1)
	  print "on1"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off1"
          time.sleep(0.5)
          GPIO.output(35, 1)
	  print "on2"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off2"
          GPIO.output(38, 1)
          x+=1
   	  lcd_string("     THANK YOU      ",LCD_LINE_1,2)
          lcd_string("Have a great ride!! ",LCD_LINE_2,2)
          lcd_string("       Anitha       ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  print " Thank You Anitha" 
          time.sleep(5)          
          main1()
def turn_sol1():
      
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(38, GPIO.OUT)
      GPIO.setup(35,GPIO.OUT)
      x=0
      while(x==0):
          GPIO.output(38, 0)
          lcd_string("  CYCLE  UNLOCKED   ",LCD_LINE_1,2)
	  print "Cycle Unlocked"
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  time.sleep(2)
          GPIO.output(35, 1)
	  print "on1"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off1"
          time.sleep(0.5)
          GPIO.output(35, 1)
	  print "on2"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off2"
          GPIO.output(38, 1)
          x+=1
   	  lcd_string("     THANK YOU      ",LCD_LINE_1,2)
          lcd_string("Have a great ride!! ",LCD_LINE_2,2)
          lcd_string("         Z          ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  print " Thank You Z" 
          time.sleep(5)          
          main1()
def turn_sol2():
      
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(38, GPIO.OUT)
      GPIO.setup(35,GPIO.OUT)
      x=0
      while(x==0):
          GPIO.output(38, 0)
          lcd_string("  CYCLE  UNLOCKED   ",LCD_LINE_1,2)
	  print "Cycle Unlocked"
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  time.sleep(2)
          GPIO.output(35, 1)
	  print "on1"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off1"
          time.sleep(0.5)
          GPIO.output(35, 1)
	  print "on2"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off2"
          GPIO.output(38, 1)
          x+=1
   	  lcd_string("     THANK YOU      ",LCD_LINE_1,2)
          lcd_string("Have a great ride!! ",LCD_LINE_2,2)
          lcd_string("      Manjunath     ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  print " Thank You Manju" 
          time.sleep(5)          
          main1()
def turn_sol3():
      
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(38, GPIO.OUT)
      GPIO.setup(35,GPIO.OUT)
      x=0
      while(x==0):
          GPIO.output(38, 0)
          lcd_string("  CYCLE  UNLOCKED   ",LCD_LINE_1,2)
	  print "Cycle Unlocked"
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  time.sleep(2)
          GPIO.output(35, 1)
	  print "on1"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off1"
          time.sleep(0.5)
          GPIO.output(35, 1)
	  print "on2"
          time.sleep(0.5)
          GPIO.output(35, 0)
	  print "off2"
          GPIO.output(38, 1)
          x+=1
   	  lcd_string("     THANK YOU      ",LCD_LINE_1,2)
          lcd_string("Have a great ride!! ",LCD_LINE_2,2)
          lcd_string("       Puja         ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
	  print " Thank You Puja" 
          time.sleep(5)          
          main1()

def callkeypadDisplay():
   
     GPIO.setmode(GPIO.BOARD)
     GPIO.setwarnings(False)   
     global flag
     if(flag==2):
        lcd_string("Enter OTP            ",LCD_LINE_1,2)
        lcd_string("                     ",LCD_LINE_2,2)
        lcd_string("                     ",LCD_LINE_3,2)
        lcd_string("                     ",LCD_LINE_4,2)
	print 'Enter OTP'
     if(flag==1 or flag==4):
        lcd_string("Enter PIN            ",LCD_LINE_1,2)
        lcd_string("                     ",LCD_LINE_2,2)
        lcd_string("                     ",LCD_LINE_3,2)
        lcd_string("                     ",LCD_LINE_4,2)
	print 'Enter PIN'
     MATRIX =[[1,2,3],[4,5,6],[7,8,9],['*',0,'#']]
     k=0
     row=[11,33,16,15]
     col=[13,37,12]
     for j in range(3):
          GPIO.setup(col[j],GPIO.OUT)
          GPIO.output(col[j],1)
     for i in range(4):
          GPIO.setup(row[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
     enteredOTP = "Enter OTP:"
     def customBreakpoint():
       h=""
       while(True):
          for j in range(3):
               GPIO.output(col[j],0)
               for i in range(4):
                    if (GPIO.input(row[i])==0):
                         MATRIX[i][j]
                         NEW_ARRAY = map(list,MATRIX)
                         MATRIX[i][j]
			 time.sleep(0.1)
                         if(MATRIX[i][j]=='*'):
                                  tempLength = len(h)
                                  if(tempLength>=0):
                                       h= h[:-1]
				       time.sleep(0.1)	
                                       lcd_string(h,LCD_LINE_2,2)
                         else:
                            h=h+str(NEW_ARRAY[i][j])
			    time.sleep(0.1)
			    print h
                         if(MATRIX[i][j]=='#'):
                             h=h[:-1]
			     time.sleep(0.1)
                             lcd_string(h,LCD_LINE_2,2)
                             return h
                         lcd_string(h,LCD_LINE_2,2)
                         while(GPIO.input(row[i])==0):
                              pass

               GPIO.output(col[j],1)
     h=customBreakpoint()
     enteredOTP += h
     compareKey = str(h)
     PIN=str(PINNum)
     PIN1=str(PINNum1)
     otp=str(OTP)
     comp=cmp(PIN,compareKey)
     comp2=cmp(PIN1,compareKey)
     comp1=cmp(otp,compareKey)
     
     if(flag==2):
       if(comp1==0):
            lcd_string("    OTP  MATCHED    ",LCD_LINE_1,2)
            lcd_string("                    ",LCD_LINE_2,2)
            lcd_string("                    ",LCD_LINE_3,2)
            lcd_string("                    ",LCD_LINE_1,2)     
	    print 'OTP Matched'
            turn_sol1()
       else:                           
               lcd_string("     WRONG OTP      ",LCD_LINE_1,2)
               lcd_string("  Please try again...  ",LCD_LINE_2,2)
               lcd_string("                    ",LCD_LINE_3,2)
               lcd_string("                    ",LCD_LINE_4,2)               
	       print 'Wrong OTP'
               time.sleep(1)
               main1()                               
     if(flag==1):
       if(comp==0):
           lcd_string("    PIN  MATCHED    ",LCD_LINE_1,2)
           lcd_string("                    ",LCD_LINE_2,2)
           lcd_string("                    ",LCD_LINE_3,2)
           lcd_string("                    ",LCD_LINE_4,2)
	   print 'PIN Matched'               
           turn_sol2()          
       else:                  
               lcd_string("     WRONG PIN      ",LCD_LINE_1,2)
               lcd_string(" Please try again...",LCD_LINE_2,2)
               lcd_string("                    ",LCD_LINE_3,2)
               lcd_string("                    ",LCD_LINE_4,2)                        
	       print 'Wrong PIN'
               time.sleep(2)                     
               main1()
     if(flag==4):
       if(comp2==0):
          lcd_string("   PIN MATCHED      ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)                                                        
	  print 'PIN Matched'
          time.sleep(3)	         
          callKeypadDisplay1()
          flag=2                              
       else:          
          lcd_string("  PIN NOT MATCHED   ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)               
          lcd_string("                    ",LCD_LINE_4,2)               
	  print 'PIN not Matched'
          time.sleep(2)
          main1()
       
      
def callKeypadDisplay1():
     
     GPIO.setmode(GPIO.BOARD) 
     GPIO.setwarnings(False)
     lcd_string("Enter OTP          ",LCD_LINE_1,2)
     lcd_string("                   ",LCD_LINE_2,2)
     print 'Enter OTP'
     MATRIX =[[1,2,3],[4,5,6],[7,8,9],['*',0,'#']]   
     row1=[11,33,16,15]
     col1=[13,37,12]
     for j in range(3):
          GPIO.setup(col1[j],GPIO.OUT)
          GPIO.output(col1[j],1)
     for i in range(4):
          GPIO.setup(row1[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
    
     enteredOTP1 = "Enter OTP"
     def customBreakpoint1():
       k1=""
       while(True):
          for j in range(3):
	       GPIO.output(col1[j],0)
	       for i in range(4):
	            if (GPIO.input(row1[i])==0):		                                  
			 MATRIX[i][j]
			 NEW_ARRAY1 = map(list,MATRIX)
			 MATRIX[i][j]
			 time.sleep(0.1)			 
			 if(MATRIX[i][j]=='*'):                                                                   
                                  tempLength1 = len(k1)                                 
                                  if(tempLength1>=0):    
                                       k1= k1[:-1]                                      
                                       lcd_string(k1,LCD_LINE_2,2)
                         else:                           
                            k1=k1+str(NEW_ARRAY1[i][j])                                                    
			    time.sleep(0.1)
			    print k1
                         if(MATRIX[i][j]=='#'):
                             k1=k1[:-1]
			     time.sleep(0.1)
                             lcd_string(k1,LCD_LINE_2,2)
                             return k1
                         lcd_string(k1,LCD_LINE_2,2)
			 while(GPIO.input(row1[i])==0):
			      pass						
	       GPIO.output(col1[j],1)
     k1=customBreakpoint1()
     enteredOTP1 += k1     
     otp1=str(OTP)
     compareKey1 = str(k1)            
     comp5=cmp(otp1,compareKey1)
     if(comp5==0):          
          lcd_string("    OTP MATCHED     ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
	  print 'OTP Matched'
          time.sleep(2)
          turn_sol3()
     else:
          lcd_string("  OTP DID NOT MATCH  ",LCD_LINE_1,2)
	  print 'OTP didnot Match'
          time.sleep(3)
          main1()
       
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    
    lcd_byte(0x01,LCD_CMD)
    GPIO.cleanup()




