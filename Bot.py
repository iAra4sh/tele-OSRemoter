import telebot
from telebot import types
from termcolor import colored
import os
import random
from PIL import ImageGrab
from datetime import datetime
from winsound import Beep
from playsound import playsound
import pyttsx3
import requests
import webbrowser


class data:
    user_want_shutdown = 0
    user_want_restart = 0
    clock = datetime.now()
    script_time = clock.strftime('%H%M%S')


os.system('cls')
print()
print(colored('Bot is Online :D \n','green'))

#--------------------------#
TOKEN = 'your token'
bot = telebot.TeleBot(TOKEN)
#--------------------------#

def getfile(filename):
    f = open(filename,'r')
    return f.read()
    f.close

def putfile(filename,data):
    f = open(filename,'w+',encoding='utf-8')
    f.write(data)
    f.close()

def startcmd(user , check):
    user_text = user.text
    user_chatid = user.chat.id
    user_username = user.chat.username
    user_firstname = user.chat.first_name
    user_lastname = user.chat.last_name

    buttons = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Screen Shot 📸')
    button2 = types.KeyboardButton('Power Options 🔋')
    button3 = types.KeyboardButton('Play Sound 🔉')
    button4 = types.KeyboardButton('File Manager 📁')
    button5 = types.KeyboardButton('Save Text 💬')
    button6 = types.KeyboardButton('Web Browser 🌐')
    button7 = types.KeyboardButton('Open App 📱')
    buttons.add(button1,button2,button3,button4,button5,button6,button7)

    if(check == 1):
        print(f'user {user_chatid} : {user_firstname} Start The Bot.')
    else:
        print(f'user {user_chatid} : {user_firstname} Backed To Home.')    
    
    clock = datetime.now()
    start_time = clock.strftime('%H%M%S')
    runtime = int(start_time) - int(data.script_time)
    
    if(runtime >= 60):
        run = runtime / 60
        run  = round(run)
        runtime = str(run)+' Minute'  
    else:
        runtime = str(runtime)+ ' Second'      

    pc_username = os.getlogin()
    cpu_usage = os.popen('wmic cpu get Loadpercentage').read()
    cpu_usage = cpu_usage.replace('LoadPercentage','')
    
    user_ip = requests.get('http://ip.jsontest.com/').json()
    user_ip = user_ip['ip']
    

    bot.send_message(user_chatid,f'Hello {user_firstname} welcome To OS Remoter Bot \nCoded By sample 😎',reply_markup=buttons)
    bot.send_message(user_chatid,f'''
     🕐 Bot Runtime : {runtime} 

    👤 PC Username : {pc_username}

    📱 IP : {user_ip}

    ⚡️ CPU Usage : {eval(cpu_usage)} %
    ''')

    data.user_want_shutdown = 0
    data.user_want_restart = 0


def savetodb(user):
    user_text = user.text
    user_chatid = user.chat.id
    rand_number = str(random.randint(11111,99999))

    message = user_text.replace('/save ','')
    putfile('database/data_'+rand_number+'.txt',message)

    bot.send_message(user_chatid,'Your Data saved as data_'+rand_number+'.txt')

def savelist(user):
    user_chatid = user.chat.id
    listfiles =''

    for r,d,f in os.walk('database'):
        for files in f:
            listfiles = listfiles+'\n'+str(files)
    bot.send_message(user_chatid,'Your Data : \n'+listfiles)

def poweroptions_btn(user):
    user_chatid = user.chat.id

    buttons = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Shutdown 🚫')
    button2 = types.KeyboardButton('Restart ♻️')
    button3 = types.KeyboardButton('Home ↩️')
    buttons.add(button1,button2,button3)

    bot.send_message(user_chatid,'Power Options Menu 🤯',reply_markup=buttons)

def screenshot_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'OK , Taking Screen Shot... 📸')

    picture = ImageGrab.grab()
    photo = picture.save('screenshot.png')
    photo = open('screenshot.png','rb')
    bot.send_message(user_chatid,'Taked , Sending to you... 📤')

    date = datetime.now()
    bot.send_photo(user_chatid,photo,caption=date)
    photo.close()
    os.remove('screenshot.png')

def shutdown_btn(user):
    user_chatid = user.chat.id
    user_text = user.text

    data.user_want_shutdown = 1
    data.user_want_restart = 0

    bot.send_message(user_chatid,'Are you sure /yes or /no')


def restart_btn(user):
    user_chatid = user.chat.id
    user_text = user.text

    data.user_want_shutdown = 0
    data.user_want_restart = 1

    bot.send_message(user_chatid,'Are you sure /yes or /no')

def shutdown_or_restart(user):
    user_chatid = user.chat.id

    if(data.user_want_shutdown == 1 and data.user_want_restart == 0):
        bot.send_message(user_chatid,'your pc shutting Down...')
        #os.system('shutdown /s /t 1')
        data.user_want_shutdown = 0
        data.user_want_restart = 0

    elif(data.user_want_shutdown == 0 and data.user_want_restart == 1):
        bot.send_message(user_chatid,'your pc Restarting...')
        #os.system('shutdown /r /t 1')   
        data.user_want_shutdown = 0
        data.user_want_restart = 0 

    else:
        bot.send_message(user_chatid,'You Are Not Using Shutdown or Restart')    


def no_shutdow_or_restart(user):
    user_chatid = user.chat.id
    data.user_want_shutdown = 0
    data.user_want_restart = 0
    bot.send_message(user_chatid,'Ok Done !')

def playsound_btn(user,check=None):
    user_chatid = user.chat.id 

    buttons = types.ReplyKeyboardMarkup(row_width=3)   
    button1 = types.KeyboardButton('Beep 🔉')
    button2 = types.KeyboardButton('Music 🎧')
    button3 = types.KeyboardButton('TTS 🗣')
    button4 = types.KeyboardButton('Home ↩️')
    buttons.add(button1,button2,button3,button4)

    if(check == 1):

        bot.send_message(user_chatid,'Beep 🌀')
        for i in range(1,8):
            Beep(1000,200*2)

        bot.send_message(user_chatid,'Done ✅')    

    if(check == 2):
        bot.send_message(user_chatid,'Playing Music... ▶️')
        playsound('outro.mp3')
        bot.send_message(user_chatid,'Done ✅')

    if(check == 3):
        bot.send_message(user_chatid,'Text To Speech Usage : \n /tts [text]')

    if(check==None):
        bot.send_message(user_chatid,'🟡 Play Sound Menu ',reply_markup=buttons)

def tts(user):
    user_text = user.text
    user_chatid = user.chat.id
    text = user_text.replace('/tts ','')
    engine = pyttsx3.init()
    engine.setProperty('rate',125)
    engine.say(text)
    engine.runAndWait()
    bot.send_message(user_chatid,'Done 😀')

def filemanager_btn(user):
    user_chatid = user.chat.id

    buttons = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton('Download Notes 📥')
    button2 = types.KeyboardButton('Download File 📂')
    button3 = types.KeyboardButton('Files List 📩')
    button4 = types.KeyboardButton('Home ↩️')
    buttons.add(button1,button2,button3,button4)

    bot.send_message(user_chatid,'😁 Welcome to File Manager Menu.',reply_markup=buttons)


def downloadnotes_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'☢️ Sending your Notes...')

    for r,d,f in os.walk('database'):
        for files in f:
            thefile = open('database\\'+str(files),'rb')
            bot.send_document(user_chatid,thefile)

    bot.send_message(user_chatid,'Done ✅')        


def downloadfile_btn(user):
    user_chatid = user.chat.id
    user_text = user.text
    bot.send_message(user_chatid,'🤓 Usage : \n /download [file name] or [file address]')


def download_cmd(user):
    user_chatid = user.chat.id
    user_text = user.text
    filename_or_fileaddress = user_text.replace('/download ','')

    if(os.path.isdir(str(filename_or_fileaddress))):
        bot.send_message(user_chatid,'📍 This is a Folder.')

    else:
        if(os.path.isfile(str(filename_or_fileaddress))):

            thefile = open(filename_or_fileaddress,'rb')
            bot.send_document(user_chatid,thefile,caption='📎 Your file')   

        else:
            bot.send_message(user_chatid,'💢 File Not Found.')     


def savetext_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'Save text Help : \n \n/save [your text] For save any text \n \n/savelist For pritn your Notes List')


def fileslist_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'😌 Usage : \n /filelist [dir]')


def filelist_cmd(user):
    user_chatid = user.chat.id
    user_text = user.text
    directory = user_text.replace('/filelist ','')


    if(os.path.isdir(directory)):

        bot.send_message(user_chatid,'Scanning... 🔎')

        folder_count = 0
        folder_list = ''

        file_count = 0
        file_list = ''

        for r, d, f in os.walk(directory):

            for folder in d:

                if(folder_count > 30 or folder_count == 30):
                    break

                else:
                    if('\\' in r): #change
                        pass
                    else:
                        folder_count += 1
                        folder_list = folder_list+'\n\n'+'📁 '+r+'/'+folder

            for files in f:

                if(file_count > 30 or file_count == 30):
                    break

                else:
                    if('\\' in r):
                        pass
                    else:
                        file_count +=1
                        file_list = file_list+'\n\n'+'📝'+r+'/'+files            

        
        bot.send_message(user_chatid,'🗂 30 First Folders In '+directory+' : \n\n'+str(folder_list)) 
        bot.send_message(user_chatid,'📃 30 First File In '+directory+' : \n\n'+str(file_list)) 

    else:
        bot.send_message(user_chatid,'‼️ I Cant Find This Directory.')              


def webbrowser_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'😊 Usage :\n\n /web [address]')


def webbrowser_cmd(user):
    user_chatid = user.chat.id
    user_text = user.text
    web_address = user_text.replace('/web ','')

    bot.send_message(user_chatid,f'📍 Opening {web_address} ...')
    webbrowser.open(web_address, new=1)
    bot.send_message(user_chatid,'✅ Done !')


def openapp_btn(user):
    user_chatid = user.chat.id
    bot.send_message(user_chatid,'😀 Usage :\n\n /openapp [App name]')


def openapp_cmd(user):
    user_chatid = user.chat.id
    user_text = user.text
    app_name = user_text.replace('/openapp ','')

    bot.send_message(user_chatid,f'🚀 Opening {app_name} ...')
    result = os.system(f'start {app_name}')

    if(result == 0):
        bot.send_message(user_chatid,'✅ Done ! ')
    else:
        bot.send_message(user_chatid,f'📛 Error \n\n Cant Open {app_name}')    



@bot.message_handler(content_types=['text'])
def botmain(user):
    admins = ['your telegram id']
    user_text = user.text
    user_chatid = user.chat.id
    user_username = user.chat.username
    user_firstname = user.chat.first_name
    user_lastname = user.chat.last_name

    if(user_username in admins):

        if(user_text == '/start'):
            check = 1
            startcmd(user,check)

        if(user_text == 'Home ↩️'):
            check = 2
            startcmd(user,check)    
            

        if(user_text.startswith('/save ')):
            savetodb(user)

        if(user_text == '/savelist'):
            savelist(user)

        if(user_text == 'Power Options 🔋'):
            poweroptions_btn(user)    

        if(user_text == 'Screen Shot 📸'):
            screenshot_btn(user) 

        if(user_text == 'Play Sound 🔉'):
            playsound_btn(user,check=None) 

        if(user_text == 'Beep 🔉'):
            playsound_btn(user,check=1)

        if(user_text == 'Music 🎧'):
            playsound_btn(user,check=2) 

        if(user_text == 'TTS 🗣'):
            playsound_btn(user,check=3)  

        if(user_text.startswith('/tts ')):
            tts(user)           

        if(user_text == 'Shutdown 🚫'):
            shutdown_btn(user)

        if(user_text == 'Restart ♻️'):
            restart_btn(user) 

        if(user_text == '/yes'):
            shutdown_or_restart(user)      

        if(user_text == '/no'):
            no_shutdow_or_restart(user)

        if(user_text == 'File Manager 📁'):
            filemanager_btn(user)    

        if(user_text == 'Download Notes 📥'):
            downloadnotes_btn(user)

        if(user_text == 'Download File 📂'):
            downloadfile_btn(user)

        if(user_text == '/download'):
            downloadfile_btn(user) 

        if(user_text.startswith('/download ')):
            download_cmd(user)       

        if(user_text == 'Save Text 💬' or user_text == '/save'):
            savetext_btn(user)

        if(user_text == '/filelist'):
            fileslist_btn(user)

        if(user_text == 'Files List 📩'):
            fileslist_btn(user)    

        if(user_text.startswith('/filelist ')):
            filelist_cmd(user)

        if(user_text == 'Web Browser 🌐' or user_text == '/web'):
            webbrowser_btn(user)

        if(user_text.startswith('/web ')):
            webbrowser_cmd(user)

        if(user_text == 'Open App 📱' or user_text == '/openapp'):
            openapp_btn(user)

        if(user_text.startswith('/openapp ')):
            openapp_cmd(user)

    else:
        bot.send_message(user_chatid,f'[-] Dear {user_firstname} You Are Not Admin.')    

#--------------------------#
bot.polling(True)