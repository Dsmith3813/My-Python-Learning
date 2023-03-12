#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

# This is my first python program. It is an electronic barista severing coffee.
# Basiclly it is the first program guild from Nertwork Chuck on youtube
# Author: Dennis J Smith
# Date:   04-05-2022

#The imports
from pickle import TRUE
import PySimpleGUI as sg
import random
import datetime
import os
from tabulate import tabulate
import io
from PIL import Image
import base64
import botton as bt

tabulate.PRESERVE_WHITESPACE = True     #This isn't working as discribed

#init program stuff
step = 0                                 #What step of the process
msg = ''                                 #Message from the robot
err = ''                                 #error msg
error = False                            #Error flag
DEF_BUTTON_COLOR = ('#0F1f00 on #0F1f00')
sg.theme('DefaultNoMoreNagging')
sg.theme('darkgray10')                   #PySimpleGUI theme
sg.set_options(font='PTMono 18')         #set font
sg.set_options(text_color='lightgreen')  #set text color 
font = ('PT Mono', 18)                   #output msg text


#Set up menu and cost list
#TODO Make is an input file
menu = [
        ["1", "Regular Octain Black Coffee", 2.25],
        ["2", "Cupachino", 7.45],
        ["3", "Cafe Americana", 3.25],
        ["4", "Mocca Grande with 2 shots", 8.59],
        ["5", "High Octane Coffee", 9.00],
        ["6", "Espresso", 3.50],
        ["7", "Green Tea", 3.25],
        ["8", "Black Leaf Tea", 3.00],
        ["9", "Premium Oolong Tea", 3.50],
        ["10", "The Pickard", 3.75]]

#List of persons that have been banned from the store.
#TODO make this an input file
#Misspelling on purpose
bandedlist = ['ben', 'benjamin', 'trevena']

def resize_base64_image(image64, size):
    image_file = io.BytesIO(base64.b64decode(image64))
    img = Image.open(image_file)
    img.thumbnail(size, Image.Resampling.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()
    return imgbytes


def GraphicButton(text, key, image_data, color=DEF_BUTTON_COLOR,
                  size=(100, 50)):
    
    return sg.Button(text, image_data=resize_base64_image(image_data, size),
                     button_color=color, font='Any 15', pad=(0, 0), key=key, border_width=0)


#Build the notification command to set a notifcation (Mac os)
def notify(message,title,subtitle,sound):
    m = 'display notification "{}"'.format(message)
    t = 'with title "{}"'.format(title)
    st ='subtitle "{}"'.format(subtitle)
    s = 'sound name "{}"'.format(sound)
    AppleNotify = ' {} {} {} {}'.format(m,t,st,s)
    command = f'''
    osascript -e '{AppleNotify}'
    '''
    os.system(command)

#Function: Determine what part of the day we are in
def set_day_type():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        greatings = 'Good morning'
        day_type = 'morning'
    elif hour < 18:
        greatings = 'Good afternoon'
        day_type = 'afternoon'
    else:
        greatings = "Good evening"
        day_type = 'evening'
    return greatings, day_type

#Function: Robots need consiant maintenace, so get a new one.
def new_robot():
    robot_num = random.randint(1,100)
    robot_name = 'Barista#'+str(robot_num)
    return robot_name

#Function: Deadbeat customers
def check_baned(name):
    msg = ' '
    if name.casefold() in bandedlist:
        error = True
        l1 = f"\nSo you're {name}!"
        l2 = "\nYou have been banned from this establishment!"
        l3 = "\nPlease leave now!\nOr I will be forced to call the police!"
        l4 = "\n\nAssHat!\n\n"
        l5 = '\nPress "NEXT" button for the next customer.'
        l6 = f'\nOr press "EXIT" to leave the coffee shop. Recomended for {name}.'
        msg = f"{l1} {l2} {l3} {l4} {l5} {l6}"
        err = '>>>>>> !! Banned Notice !! <<<<<<'
    else:
        error = False
        msg = str(f"Hello, {name}, hope you are having a nice {day_type}.\n\nHere is our menu for this {day_type}:\n\n")
        msg = msg + str((tabulate(menu, headers=['No','Item','Price'], floatfmt=".2f", numalign='left', stralign='left')))
        msg = msg + str('\n\nPlease enter the menu item number:')
        err = ' '
    return (error, msg, err)

#Function: Make sure we have a correct item number
def check_item(item):
    if item not in range(1,11):
        error = True
        err = 'Item out of range; Enter 1 through 10'
        msg = ' '
    else: 
        error = False
        prod = menu[item - 1][1] 
        msg = f'How meny "{prod}" would you like {name}?'
        err = ' '
    return (error, msg, prod, err)
#
#  Start of program main line.
#

greatings, day_type = set_day_type()
robot_name = new_robot()

#All the stuff inside the window using pySimpleGUI
layout = [  [sg.Text(f'{greatings}, Welcome to Gitta High Coffee Shop',
                     s=(50,1), justification='center')],
            [sg.Text('Where your coffee high is only a sip away', s=(50,1),
                      justification='center')],
            [sg.Text(f'Server {robot_name} has joined', s=(50,1),
                     key='-rob-',justification='center')],
            [sg.Text(' ')],
            [sg.Text('Please enter requested information:'), 
             sg.InputText(s=(15,1), key='-in-'), 
             sg.Button('Enter', bind_return_key='Enter')],
            [sg.Text(s=(50,1), k='-err-', text_color='Red', 
                     font=('PT Mono', 22, 'bold'), 
                     justification='center')],
            [sg.Text(s=(50,20), key='-out-', font=font)],
            [sg.Text(' ')],
            # [sg.Button('Next'), sg.Button('Exit')],
            [GraphicButton('Next', '-Next-', bt.green_pill64),
             GraphicButton('Exit', '-Exit-', bt.green_pill64)]]

#Create the Window
window = sg.Window('Gitta High Coffee Shop', layout, size=[600,700],
                    # no_titlebar=True, 
                    finalize=True, 
                    use_default_focus=True, 
                    location=(300,125),
                    keep_on_top=False)

#Event Loop to process "events" and get the "values" of the inputs
while True:
    #Note that first window create will have a null event returned

    #Determine what step of the process we are in.
    #STEP = 0 customer came into the shop populate the window
    #STEP = 1 we have the customer name see if they are baned and check the menu
    #STEP = 2 Ask the customer to pick an item
    #STEP = 3 Ask how meny they would like, and give them the cost
    
    if step == 0: 
        msg = f'Hello, my name is {robot_name}. May I have your first name please?'
        window['-out-'].update(msg)                     
        step = 1
        error = False
        event, values = window.read()
    elif error:                  #error somewhere; reset and start again
        step = 0
        error = False
        event, values = window.read()
    else:                               #normal pass
        error = False
        step += 1
        window['-err-'].update(' ')
        event, values = window.read()

    #Check what event occured and what step   
    if event == sg.WIN_CLOSED or event == '-Exit-': 
        break
    elif event == '-Next-':
        step = 0
        window['-err-'].update(' ')
        window['-in-'].update(' ')
        error = False
        window.Refresh()
    elif event == 'Enter':                 #customer input; determin what step
                                            #of the process we are in
        if step == 1:
            name = values['-in-']
            window['-in-'].update(' ')
            error, msg, err = check_baned(name)
            if error:
                window['-out-'].update(msg)
                window['-err-'].update(err)
            else:
                window['-err-'].update(' ')
                window['-out-'].update(msg)

        if step == 2:
            item = ''
            item = int(values['-in-'])
            error, msg, err, prod = check_item(item)
            if error:
                step = 1
                window['-err-'].update('err')
                window['-out-'].update(msg)
                window['-in-'].update(' ')
            else:
                window['-out-'].update(msg)
                window['-err-'].update(' ')
                window['-in-'].update(' ')
            
        if step == 3:
            qty = int(values['-in-'])
            x = item - 1
            prod = menu[x][1]
            price = menu[x][2]
            total = "{:.2f}".format((price * qty))
            a = f'Ok, {name}; your {qty} "{prod}" will be ready in a few moments.'
            b = '\nYour total will be $' + str(total) + '.'
            c = '\nYou may pickup your order from the human at the next window.'
            d = f'\nHave a wonderful {day_type} {name}!'
            e = f'\n\nPlease standby as {robot_name} needs an oil change.'
            f = '\nPress "NEXT" for the next customer.'
            g = '\nOr press "EXIT" to leave the coffee shop.'
            msg = f'{a} {b} {c} {d} {e} {f} {g}'
            window['-out-'].update(msg)
            window['-err-'].update(' ')
            window['-in-'].update(' ')
            window['-rob-'].update(f'Please stand by: {robot_name} needs an oil change...')
            robot_name = new_robot()
            window['-rob-'].update(f'Server {robot_name} will be here shortly.')
            n1 = f'Thank you {name}, your ${total} purchase was successful'
            n2 = f'Charging ${total} on your card'
            n3 = f'Your ${total} purchase Was Approved!'
            notify(n1,n2,n3,'payment_success')
            
window.close()