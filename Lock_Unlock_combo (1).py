import RPi.GPIO as GPIO
import time
import random
import getpass
import MFRC522
import signal
import requests
import json
DOCK_Number='20161122'
flag=1
parentRootJSONObject=''
PINNum=''
PINNum1=''
otp1=''
tot_uid=''
Mob_Num=''
Name=''
flag=1
p=0
tot_uid1=''
continue_reading = True
GPIO_CLEANED_UP  = False

def Berry_Card():

 global  continue_reading
 sep='/dev/spidev0.1'
 MFRC522.__init__(sep,1000000)
 signal.signal(signal.SIGINT, end_read)
 MIFAREReader = MFRC522.MFRC522(sep,1000000)
 
 while continue_reading:

         

   
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    
    if status == MIFAREReader.MI_OK:

              lcd_string("   Connecting       ",LCD_LINE_1,2)
              lcd_string("       to server....",LCD_LINE_2,2)
              lcd_string(" Please wait....... ",LCD_LINE_3,2)
              lcd_string('                    ',LCD_LINE_4,2)
      
    
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    
    if status == MIFAREReader.MI_OK:

            global parentRootJSONObject
            global tot_uid1
            tot_uid1 =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print tot_uid
                
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(36, GPIO.OUT)


            GPIO.output(36,0)
            time.sleep(1)
            GPIO.output(36,1)
            responseReceived = requests.post('http://www.cykul.com/CYKULStations/Python/Activity/returnCycle.php?rcdidRefN=' + DOCK_Number + '&rccidRefN=' + tot_uid1)

            decodedJSONResponse = responseReceived.json()
                                   
            lcd_string("    Cycle Locked    ",LCD_LINE_1,2)
          
            lcd_string('        Hope        ',LCD_LINE_2,2)
            lcd_string('You Had a Great Ride',LCD_LINE_3,2)
            time.sleep(2)            
            main()
                     
    else:
            main()
            

def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    if(GPIO_CLEANED_UP==False):
                GPIO.cleanup()
def Rasp_Card():
    sep1='/dev/spidev0.0'

    MFRC522.__init__(sep1,1000000)
    global  continue_reading

    global flag
    global PINNum1
    global PINNum
    

    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522(sep1,1000000)
            

    while continue_reading:
        
        
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    
        if status == MIFAREReader.MI_OK:
            
          
            
            lcd_string("   Connecting       ",LCD_LINE_2,2)
            lcd_string("       to server....",LCD_LINE_3,2)
            lcd_string(" Please wait....... ",LCD_LINE_4,2)



    
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

    
  
        if status == MIFAREReader.MI_OK:

      
            global tot_uid
            tot_uid =  str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print tot_uid
            customURL= "http://www.cykul.com/CYKULStations/Python/Validation/getCardValidationStatus.php?cvsRefN=" + tot_uid
            global parentRootJSONObject
            responseReceived=requests.get(customURL)
            parentRootJSONObject = responseReceived.json()
            print parentRootJSONObject
            Condition_card()

        else:
          main()


                       
          
def Condition_card():
   global flag

   responseReceived = requests.post('http://www.cykul.com/CYKULStations/Python/Activity/issueCycle.php?icdidRefN=' + DOCK_Number + "&iccidRefN="  +tot_uid)

   decodedJSONResponse = responseReceived.json()

   print(decodedJSONResponse)



   if(decodedJSONResponse['result_status']=='true'):

            print'inside parentRootJSONObject==true',parentRootJSONObject['validation_status']

            if (  parentRootJSONObject['validation_status'] == "true" ):
                        global Name
                        Name=parentRootJSONObject['card_owner_name']


                        if( parentRootJSONObject['case_found']=="1" ):

                
                             lcd_string("       Welcome        ",LCD_LINE_1,2)
                             
                             lcd_string(parentRootJSONObject['card_owner_name'],LCD_LINE_2,2)
                             lcd_string('          ',LCD_LINE_3,2)
                             lcd_string('          ',LCD_LINE_4,2)
                          
                             time.sleep(2)
                             turn_sol()
                            # Berry_Card()

                        
                     
                        if( parentRootJSONObject['case_found']=="2" ):
                              
                              lcd_string("       Welcome        ",LCD_LINE_1,2)
                              
                              lcd_string(  parentRootJSONObject['card_owner_name']  ,LCD_LINE_2,2)
                              lcd_string('          ',LCD_LINE_3,2)
                              lcd_string('          ',LCD_LINE_4,2)
   
                              flag=2
                              global PINNum
                      
                              PINNum=parentRootJSONObject['generated_otp']
                              print PINNum
                              time.sleep(3)
                              callkeypadDisplay()
                              main()
                        
                            




                        if(parentRootJSONObject['case_found']=="3"):

                             lcd_string("     Welcome        ",LCD_LINE_1,2)
                             
                             lcd_string(  parentRootJSONObject['card_owner_name']  ,LCD_LINE_2,2)
                             lcd_string('          ',LCD_LINE_3,2)
                             lcd_string('          ',LCD_LINE_4,2)
                             time.sleep(3)
                             PINNum=parentRootJSONObject['secure_pin']
                             print PINNum

                             flag=1
                             
                             callkeypadDisplay()

                              
                         
                        if( parentRootJSONObject['case_found']=="4"):
                              
                              lcd_string("       Welcome        ",LCD_LINE_1,2)
                            
                              lcd_string(  parentRootJSONObject['card_owner_name'] ,LCD_LINE_2,2)
                              lcd_string('          ',LCD_LINE_3,2)
                              lcd_string('          ',LCD_LINE_4,2)
                              time.sleep(3)

             
                           
                              global   Mob_Num
                              Mob_Num=parentRootJSONObject['otp_mobile_number']

                              PINNum=parentRootJSONObject['secure_pin']
                              print "pin_case4",PINNum
                              flag=4
                              callkeypadDisplay()

            else:
                if(parentRootJSONObject['case_found']=='6'):
                             
                             Name=parentRootJSONObject['card_owner_name']


                             lcd_string("       Sorry!!!          ",LCD_LINE_1,2)
                             lcd_string("   Renew your card       ",LCD_LINE_2,2)
                             lcd_string(Name,LCD_LINE_3,2)
                            
                             lcd_string('          ',LCD_LINE_4,2)
                             time.sleep(3)
                             main()
                if(parentRootJSONObject['case_found']=='5'):
                             lcd_string("       Sorry!!!     ",LCD_LINE_1,2)
                             lcd_string("   Invalid Card     ",LCD_LINE_2,2)
                             lcd_string('                    ',LCD_LINE_3,2)
                             lcd_string('                    ',LCD_LINE_4,2)
                             time.sleep(3)
                             main()
                           
                if(parentRootJSONObject['case_found']==0) :
                             lcd_string("   User Invalid     ",LCD_LINE_1,2)
                             lcd_string("                       ",LCD_LINE_2,2)
                             lcd_string('                       ',LCD_LINE_3,2)
                             lcd_string('                       ',LCD_LINE_4,2)
                             time.sleep(3)
                             main()  

                if(parentRootJSONObject['case_found']=='7') :
                             lcd_string("   Cycle Not Present   ",LCD_LINE_1,2)
                             lcd_string("     At Station        ",LCD_LINE_2,2)
                             lcd_string('                       ',LCD_LINE_3,2)
                             lcd_string('                       ',LCD_LINE_4,2)
                             time.sleep(3)
                             main()

             
                
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


def main():
#  Approved_list('424162162','185163241100','153121243100','153217232100','48151162','194866038')
  flag=1
  lcd_init()
  s=0
  while (True):

     responseReceived = requests.post('http://www.cykul.com/CYKULStations/Python/Validation/getDockCurrentStatus.php?gdcsRefN=' +  DOCK_Number)

     decodedJSONResponse = responseReceived.json()
  

     responseStatus = decodedJSONResponse['result_status']     
     lcd_string("--------------------",LCD_LINE_1,2)
     lcd_string("     WELCOME TO     ",LCD_LINE_2,2)

     print'in main'     
   
     lcd_string("   CYKUL STATION    ",LCD_LINE_3,2)
     lcd_string("--------------------",LCD_LINE_4,2)
     
     time.sleep(2)
     lcd_string("--------------------",LCD_LINE_1,2)
     lcd_string("     PLEASE   ",LCD_LINE_2,2)
    
     lcd_string("   SCAN YOUR CARD    ",LCD_LINE_3,2)
     lcd_string("--------------------",LCD_LINE_4,2)
     time.sleep(4)
     print decodedJSONResponse['cycle_availability']

     if decodedJSONResponse['cycle_availability'] == "true":
#####  issue cycle  ####
             print 'take cycle '
             Rasp_Card()

     else:
             lcd_string('Cycle Not Available',LCD_LINE_1,2)
             lcd_string("       at          ",LCD_LINE_2,2)
             lcd_string("      Station      ",LCD_LINE_3,2)
             lcd_string("                   ",LCD_LINE_4,2)
             time.sleep(3)
             print 'return cycle'           
             Berry_Card()
     
               

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
      GPIO.setup(36,GPIO.OUT)
      x=0 
     
      while(x==0):
          GPIO.output(38,0)
          time.sleep(2)
          lcd_string("  Cycle Unlocked   ",LCD_LINE_1,2)
          lcd_string("                   ",LCD_LINE_2,2)
          time.sleep(1)
          GPIO.output(36,0)
          time.sleep(0.5)
          GPIO.output(36,1)
          time.sleep(0.5)
          
          GPIO.output(36,0)
          time.sleep(0.5)
          GPIO.output(36,1)
          time.sleep(0.5)

          GPIO.output(38, 1)
      
          x+=1
          lcd_string("      Thank You    ",LCD_LINE_1,2)
          lcd_string("Have a Great Ride!!",LCD_LINE_2,2)
          lcd_string(Name,LCD_LINE_3,2)
          time.sleep(5)
        
 
   
####sending status of cycle to server
          main()


def callkeypadDisplay():

   
     GPIO.setmode(GPIO.BOARD)
     GPIO.setwarnings(False)
   
     global flag
     if(flag==2):
        lcd_string("Enter OTP Number:    ",LCD_LINE_1,2)
        lcd_string("                     ",LCD_LINE_2,2)
        lcd_string("                     ",LCD_LINE_3,2)
        lcd_string("                     ",LCD_LINE_4,2)



     if(flag==1 or flag==4):
        lcd_string("Enter PIN Number:   ",LCD_LINE_1,2)
        lcd_string("                    ",LCD_LINE_2,2)
        lcd_string("                    ",LCD_LINE_3,2)
        lcd_string("                    ",LCD_LINE_4,2)






     MATRIX =[[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]
     k=0
     row=[37,11,13,15]
     col=[12,16,33]

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


                         if(MATRIX[i][j]=='#'):
                             h=h[:-1]
                             time.sleep(0.1)

                             lcd_string(h,LCD_LINE_2,2)
                             return h


                         lcd_string(h,LCD_LINE_2,2)
                         while(GPIO.input(row[i])==0):
                              pass

               GPIO.output(col[j],1)



     global cnt
     global PINNum1
     h=customBreakpoint()
     enteredOTP += h

     compareKey = str(h)
     PIN=str(PINNum)
     comp=cmp(PIN,compareKey)
     comp1=cmp(otp1,compareKey)
     
     if(flag==1):
       if(comp==0):
            lcd_string("    PIN  Matched    ",LCD_LINE_1,2)
            lcd_string("                    ",LCD_LINE_2,2)
            lcd_string("                    ",LCD_LINE_3,2)
            lcd_string("                    ",LCD_LINE_1,2)
     
            turn_sol()
       else:
            
               
               lcd_string("     Wrong Pin      ",LCD_LINE_1,2)
               lcd_string("  Plz try again...  ",LCD_LINE_2,2)
               lcd_string("                    ",LCD_LINE_3,2)
               lcd_string("                    ",LCD_LINE_4,2)               
               time.sleep(1)
               main()
               
      
      
    
     if(flag==2):
        if(comp==0):

           lcd_string("    otp  matched    ",LCD_LINE_1,2)
           lcd_string("                    ",LCD_LINE_2,2)
           lcd_string("                    ",LCD_LINE_3,2)
           lcd_string("                    ",LCD_LINE_4,2)               
           turn_sol()

          

        else:

           if(cnt<2):
               cnt+=1
               lcd_string("     Wrong OTP      ",LCD_LINE_1,2)
               lcd_string(" Please try again...",LCD_LINE_2,2)
               lcd_string("                    ",LCD_LINE_3,2)
               lcd_string("                    ",LCD_LINE_4,2)
                        
               time.sleep(1)
               
               callkeypadDisplay()
           else:
               main()


     if(flag==4):

        if(comp==0):

          lcd_string("   PIN Matched      ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
          lcd_string("                    ",LCD_LINE_4,2)
          print'in case 4'        
          time.sleep(3)
          CUSTOMURL= "http://www.cykul.com/CYKULStations/Python/Validation/sendGeneratedOTP.php?sgotpRefN=" + Mob_Num
          
          responseReceived=requests.get(CUSTOMURL)
          parentRootJSONObject1 = responseReceived.json()
          print   parentRootJSONObject1
         
          PINNum1 =parentRootJSONObject1['generated_otp']

          print PINNum1
          callKeypadDisplay1()
          flag=1
          
          

          
        else:
          
          lcd_string("  PIN not matched   ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
          lcd_string("                    ",LCD_LINE_3,2)
               
          lcd_string("                    ",LCD_LINE_4,2)
               
          time.sleep(2)
          main()






def callKeypadDisplay1():
     
     GPIO.setmode(GPIO.BOARD) 
     GPIO.setwarnings(False)
     lcd_string("Enter OTP:         ",LCD_LINE_1,2)
     lcd_string("                   ",LCD_LINE_2,2)


     MATRIX =[[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]
    
     row1=[37,11,13,15]
     col1=[12,16,33,31]
     for j in range(4):
          GPIO.setup(col1[j],GPIO.OUT)
          GPIO.output(col1[j],1)
     for i in range(4):
          GPIO.setup(row1[i],GPIO.IN,pull_up_down=GPIO.PUD_UP)
     
     enteredOTP1 = "Enter OTP:"
     def customBreakpoint1():
       k1=""
       while(True):

          for j in range(4):
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
                                       time.sleep(0.1)

                                       lcd_string(k1,LCD_LINE_2,2)
                         else:
                           
                            k1=k1+str(NEW_ARRAY1[i][j])
                            time.sleep(0.1)

                         
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
    
 
     PINNum5=str(PINNum1)
     compareKey5 = str(k1)
     
     
     comp5=cmp(PINNum5,compareKey5)
  

     
     if(comp5==0):
          
          lcd_string("    OTP Matched     ",LCD_LINE_1,2)
          lcd_string("                    ",LCD_LINE_2,2)
          time.sleep(2)
          turn_sol()
     else:

          lcd_string("  OTP didn't match  ",LCD_LINE_1,2)

          time.sleep(2)

          main()

       
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    
    lcd_byte(0x01,LCD_CMD)
    GPIO.cleanup()


