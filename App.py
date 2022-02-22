

from cgi import test
from pydoc import text
from tkinter import Image
import kivy
from sklearn.feature_extraction import image
kivy.require("1.9.1")
import os
import subprocess


from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.uix.label import Label
from subprocess import PIPE, run
from kivy.uix.textinput import TextInput

from time import sleep
from ScannerRCP import ScannerRCP
from kivy.uix.image import Image
from threading import Thread


class FunctionalTestApp(App):
    
    def build(self):
        # use a (r, g, b, a) tuple
        title = Label(text ="                          RODE: RCPII Functional Test Application",font_size = 30,size=(150,10), pos=(10, 10))
        logo_image = Image(source='rode_250.jpg', size_hint=(None, None,), width=200, height=100)
        self.lbl = Label(text ="Ready to test",font_size = 30,size=(150,150), pos=(10, 10))

        self.button1 = Button(text="Flash",font_size = 30,size=(150,150), size_hint=(.25, 1), pos=(350, 300))
        # self.button1.bind(on_press=partial(self.com1, self.button1))

        self.button2 = Button(text="Check SD card",font_size = 30,size=(150,150), size_hint=(.25, 1), pos=(350, 300))
        # self.button3.bind(on_press=partial(self.com1, self.button3))

        self.button3 = Button(text="Assign Mac address",font_size = 30,size=(150,150), size_hint=(.25, 1), pos=(350, 300))
        # self.button2.bind(on_press=partial(self.com2, self.button2))

        self.button4 = Button(text="Assign Serial",font_size = 30, size=(150,150), size_hint=(.25, 1), pos=(350, 300))
        # self.button4.bind(on_press=partial(self.com2, self.button4))
        self.textinput = TextInput(text='',multiline=False)

        self.button5 = Button(text="Reset",font_size = 30, size=(150,150), size_hint=(.25, 1), pos=(350, 300), background_color= (0.0, 0.0, 1.0, 1.0))
        # self.button5.bind(on_press=partial(self.com2, self.button5))

        boxlayout_Title = BoxLayout(orientation='horizontal', size_hint_y = 0.15)
        self.boxlayout_label = BoxLayout(size_hint_y = 0.7)
        boxlayout = BoxLayout(orientation='horizontal',size_hint_y = 0.7)
        self.boxlayout_text = BoxLayout(size_hint_y = 0.1)
        
        boxlayout_Title.height = 10
        boxlayout_Title.add_widget(title)
        boxlayout_Title.add_widget(logo_image) 
        

        self.boxlayout_label.add_widget(self.lbl)
        boxlayout.add_widget(self.button1)
        boxlayout.add_widget(self.button2)
        boxlayout.add_widget(self.button4)
        boxlayout.add_widget(self.button3) 
        boxlayout.add_widget(self.button5)
        self.boxlayout_text.add_widget(self.textinput)
    
        #Button Press Call
        self.button1.bind(on_press = self.Flashcallback_parellel)
        self.button2.bind(on_press = self.SDcallbac_parallel)
        self.button3.bind(on_press = self.Macaddresscallback_parallel) 
        self.button4.bind(on_press = self.AssignSerialcallback_parallel)
        self.button5.bind(on_press = self.Resetcallback)


        # Screen layout
        Screen_layout = BoxLayout(orientation='vertical')
        Screen_layout.add_widget(boxlayout_Title)
        Screen_layout.add_widget(self.boxlayout_label)
        Screen_layout.add_widget(self.boxlayout_text)
        Screen_layout.add_widget(boxlayout)

        self.textinput.focus = True

        return Screen_layout
 
    
    
    #........................................................ Parallel Process for each button press..................................................

    def Flashcallback_parellel(self, event):

        ''' Parallel call '''

        self.lbl.text = 'Flashing: IN PROGRESS'
        self.button1.background_color = (1,1,0.2,1)

        self.fthread= Thread(name='Flashcallback', target=self.Flashcallback,daemon=True)
        self.fthread.start()
    
    def SDcallbac_parallel(self,event):

        ''' SD card call back '''

        self.lbl.text = 'SD Card validation: IN PROGRESS'
        self.button2.background_color = (1,1,0.2,1)

        self.fthread= Thread(name='SDcallbac_parallel', target=self.SDcallback,daemon=True)
        self.fthread.start()

    def Macaddresscallback_parallel(self,event):

        ''' Mac address call back '''

        self.lbl.text = 'MAC Address Assignment(BT): IN PROGRESS'
        self.button3.background_color = (1,1,0.2,1)

        self.fthread= Thread(name='Macaddresscallback', target=self.Macaddresscallback,daemon=True)
        self.fthread.start()

    def AssignSerialcallback_parallel(self,event):

        ''' AssignSerialback'''

        self.lbl.text = 'Serial Assignment : IN PROGRESS'
        self.button4.background_color = (1,1,0.2,1)

        self.fthread= Thread(name='AssignSerialcallback', target=self.AssignSerialcallback,daemon=True)
        self.fthread.start()

    
    
    
    
    
    
    
    
    
    ##..................................Call back function..................................................
    
    
    
    
    # callback function tells when button pressed
    
    def Flashcallback(self):

        ''' Flash the device '''
        try:
            sleep(1)
            os.system('sudo rm -rf /dev/sda')
            result = os.system('sudo python3 ~/pyamlboot/boot.py --image ~/rodecaster-pro-mini/Image --fdt ~/rodecaster-pro-mini/meson-axg-rodecaster.dtb --board-files ~/rodecaster-pro-mini/ --script ~/pyamlboot/boot.scr s400')
        
            print(result)

            if str(result)!='0':
                self.lbl.text = 'Flashing: FAILED'
                self.button1.background_color = (1,0,0.2,1)
            else:
                pass

            result = os.system("ls /dev/sda")
            if str(result)!='0':
                self.lbl.text = 'Flashing: FAILED'
                self.button1.background_color = (1,0,0.2,1)
            else:
                pass

            os.system("umount /media/rcp-ate/root")
            result = os.system("sudo dd if=~/rodecaster-pro-mini/rode-image-rt-eol-prod-rodecaster-pro-mini.wic of=/dev/sda status=progress")
        
            if str(result)!='0':
                self.lbl.text = 'Flashing: FAILED'
                self.button1.background_color = (1,0,0.2,1)
            else:
                self.lbl.text = 'Flashing: DONE'
                self.button1.background_color = (0,1,0.2,1)

            self.textinput.focus = True
        except:

            self.lbl.text = 'Flashing: No RCPII Found'
            self.button1.background_color = (1,0,0.2,1)
            self.textinput.focus = True

        

    def SDcallback(self):
        
        ''' Check SD card '''
        
        try:

            os.system('dd if=/dev/urandom of=/media/rcp-ate/1234-5678/test.file status=progress count=2000000')
            returnval = os.system('dd if=/media/rcp-ate/1234-5678/test.file of=test.file2 status=progress')

            if str(returnval)!='0':
                self.lbl.text = 'SD Card validation: FAILED'
                self.button2.background_color = (1,0,0.2,1)
            else:
                self.lbl.text = 'SD Card validation: DONE'
                self.button2.background_color = (0,1,0.2,1)


            self.textinput.focus = True
        except:

            self.lbl.text = 'SD Card validation: No RCPII Found'
            self.button2.background_color = (1,0,0.2,1)
            self.textinput.focus = True

    
    
    
    
    def Macaddresscallback(self):

        ''' Assign Mac Address '''

       
        try:

            #ETH
            os.system("rm ~/.ssh/known_hosts")
            with open('/home/rcp-ate/Documents/ethMacsList.txt') as f:
                line = f.readlines()
            f.close()
            
            os.system('sed -i \"1 d\" /home/rcp-ate/Documents/ethMacsList.txt')

            result = os.system("echo \""+ str(line) + "\"| sshpass -p Yojcakhev90 ssh -o \"StrictHostKeyChecking no\" root@192.168.1.150 -T \"cat > /Application/emmc-data/eth-mac.txt\"")

            if str(result)!='0':
                self.lbl.text = 'MAC Address Assignment (ETH): FAILED'
                self.button3.background_color = (1,0,0.2,1)
            else:
            
                pass

            
            #Blue TOOTH


            with open('/home/rcp-ate/Documents/wifiBtMacsList.txt') as f:
                line = f.readlines()
            # os.system('read -r line < "$wifiBtMacsFile"')
            os.system('sed -i \"1 d\" /home/rcp-ate/Documents/wifiBtMacsList.txt')
            result = os.system("echo \""+ str(line) + "\"| sshpass -p Yojcakhev90 ssh -o \"StrictHostKeyChecking no\" root@192.168.1.150 -T \"cat > /Application/emmc-data/wifi-mac.txt\"")

            if str(result)!='0':
                self.lbl.text = 'MAC Address Assignment(WIFI): FAILED'
                self.button3.background_color = (1,0,0.2,1)
            else:
            
                pass

    
            #WIFI
            
            with open('/home/rcp-ate/Documents/wifiBtMacsList.txt') as f:
                line = f.readlines()
        
            os.system('sed -i \"1 d\" /home/rcp-ate/Documents/wifiBtMacsList.txt')
            result = os.system("echo \""+ str(line) + "\"| sshpass -p Yojcakhev90 ssh -o \"StrictHostKeyChecking no\" root@192.168.1.150 -T \"cat > /Application/emmc-data/bt-mac.txt\"")



            if str(result)!='0':
                self.lbl.text = 'MAC Address Assignment(BT): FAILED'
                self.button3.background_color = (1,0,0.2,1)
            else:
            
                self.lbl.text = 'MAC Address Assignment: DONE'
                self.button3.background_color = (0,1,0.2,1)

            self.textinput.focus = True
        
        except:

            self.lbl.text = 'MAC Address Assignment(BT): FAILED \n No RCPII FOUND'
            self.button3.background_color = (1,0,0.2,1)
            self.textinput.focus = True
        
    def AssignSerialcallback(self):
        
        ''' Assign Serial number '''
        
        try:

             
            self.textinput.bind(text = self.on_text)
            if self.textinput.text == '' or self.textinput.text==None:
                self.lbl.text = 'No Serial Number scanned. Please scan a serial number'
                self.textinput.focus = True
                return
            
            print(self.textinput.text)
            
            result = os.system("echo \""+ str(self.textinput.text) + "\"| sshpass -p Yojcakhev90 ssh -o \"StrictHostKeyChecking no\" root@192.168.1.150 -T \"cat > /Application/emmc-data/unit-serial.txt\"")


            print(" Scan completed ")
            print("Scanner Program: Scan completed ")
            result ='Pass'

            if str(result).find('FAILED')> 0:
                self.lbl.text = 'Serial Assignment: FAILED'
                self.button4.background_color = (1,0,0.2,1)
            else:
                self.lbl.text = 'Serial Assignment: DONE, Serial Number = ' + str(self.textinput.text)
                self.button4.background_color = (0,1,0.2,1)
        
        except:

            self.lbl.text = 'Serial Assignment: No RCPII Found'
            self.button4.background_color = (1,0,0.2,1)
            raise Exception

        
        


    def Resetcallback(self,event):
        os.system('')

        self.lbl.text = 'Serial assignment: DONE'
        self.button1.background_color = 'silver'
        self.button2.background_color = 'silver'
        self.button3.background_color = 'silver'
        self.button4.background_color = 'silver'

    
         
 
# creating the object root for ButtonApp() class
root = FunctionalTestApp() 
root.run()
