#We are going to want to have a generator for fubo.tv -> this will allow us to create / gen accounts and store them.
#We are going to want to create not a UI -> but it just being regular first.


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QComboBox
from PyQt6.QtWidgets import *
#We are going to need to have this to validate.
from PyQt6.QtGui import QIntValidator

import os
import json
import requests

#Used for passwords. 

import secrets
import string

import generate


email_path = 'emails.json'
credit_card_path = 'credit_card.json'
discord_path = 'discord.json'


#Used to get only the emails and send them back. 
def decompileInformation():
    print('We are decompiling information.')
    text = ''
    for email in json_info:
        text = text + email['email'] + '\n'

    return text
    # for email in 


#Function used for whenever the user clicks on the discord webhook information and saves it. 
def save_discord():

    #Extract information we are going to want to send the discord webhook too.
    line_edit_text = LineEdit_discord.text()
    webhook_info = {
        "webhook" : line_edit_text
    }

    #So we are going to want to open the file first to write too it. 
    with open(discord_path, "w") as file:
        json.dump(webhook_info,file)

    
def test_webhook():

    discord_info = {
        "username" : "Fubo Generator",
        "content" : ".",

        "embeds" : [
            {
                "title" : "Hello , This is a Test for Fubo Generator! ",
        
                'fields' : [
                    {
                        "name" : "Test",
                        "value" : "This is a test. "
                    }


                ]
            }

        ]
    }

    #Get the actual link for the discord. 
    discord_link = LineEdit_discord.text()

    status = requests.post(discord_link,json = discord_info)

    if(status.status_code != 204):
        print('Error has occured -> error is ', status, status.text)
    else: 
        print("We tested Succesfully! ")

    



def warning(users_emails):
    print("Warning.... if you click on this you will overwrite all emails history stored and are going to rewrite overemails. Are you sure? ")
    if True:
        get_emails(users_emails)


#used for credit card. 
def LoadProfiles():

    #Only if the name exist. 
    if os.path.exists(credit_card_path):
        information = {}
        with open(credit_card_path,"r") as file:
            information = json.load(file)
    else:
        return
    
    #Now that if we have this information we are going to want to display it....

    
    LineEdit_First_name.setText(information["first_name"])
    LinEdit_Last_name.setText(information["last_name"])
    LineEdit_credit_card.setText(information["credit_number"])
    LineEdit_CVV.setText(information['cvv'])
    Combo_Month.setCurrentText(information['exp_month'])
    Combo_Year.setCurrentText(information['exp_year'])
    LineEdit_ZipCode.setText(information['zipcode'])





def save_credit_card():

    #Do not care about if they already exist we are just going to want to write to it. (Want to write to it as json tho.)
    #Stored all the information in a proper json format. 

    credit_card = {
        "first_name" : LineEdit_First_name.text(),
        "last_name" :  LinEdit_Last_name.text(),
        "credit_number" : LineEdit_credit_card.text(),
        "cvv" : LineEdit_CVV.text(),
        "exp_month" : Combo_Month.currentText(),
        "exp_year" : Combo_Year.currentText(),
        "zipcode" : LineEdit_ZipCode.text()
    }

    #going to want to write to the file the inforamtion we have gathered. 
    with open(credit_card_path, "w") as file:
        #Want to write something to a file must use json dump. 
        json.dump(credit_card,file)
    


    


#This function objective is to write all the emails from the 
def get_emails(users_emails):
    #From this we are going to want to want to save the user_emails to persistant storage. 
    #First want to see if the file is already created-> if so open it. If not do not open it and create one. 


    #This is going to return text/string of all the information that was in the users inbox. 
    text = textBox_emails.toPlainText()

    print(text, "This is the text")

    print('We are actually saving the emails')

    #Want to verify now that the format was correct and emails are proccessed 
    print(text)

    #We are using a delimited 
    list_split = text.split('\n')

    #Going to want to verify that every email is a correct email.
    #This is going to have to deal with containing a @ symbol and also going to contain .com. 
    valid_list = True

    print(valid_list , "This is our valid list!")

    for email in list_split:
        
        #Makes sure email ends with .com , makes sure it's alphabatic.Also want to make sure it contains @ symbol. 
        if not email.endswith('.com' ) or not '@' in email:
            valid_list = False

        #If the user is trying to delete it.
        if len(text) == 0:
            valid_list = True

    #Return if list is not valid. 
    if valid_list == False:
        print('List is not valid. ')
        return

    #Want to go through the list again and make them each a json and add it to a list. 


    list_of_emails = []

    #Used to generate passwords.
    alphabet = string.ascii_letters + string.digits + "!@#$%^"



    #For each emmail going to want to do this. 
    for email in list_split:

        #Each email generate a new unique password. With a range of 12. 
        generated_password = ''.join(secrets.choice(alphabet) for _ in range(12))

        current_email = {
            "email" : email,
            "has_been_used" : False,
            "password" : generated_password
        }

        #Going to want to add it to our list. 
        list_of_emails.append(current_email)




    #We now have a valid list and can properly store it.

    print(valid_list)
    if valid_list == True:
        print("Saved Information! ")

        #If the path already exist in our file.
        if os.path.exists(email_path):
            with open(email_path,"w") as file:
                json.dump(list_of_emails,file,indent=2)
                #file.write(text)
        else:
            with open(email_path,"w") as file:
                json.dump(list_of_emails,file,indent=2)
        


    


app = QApplication(sys.argv)


#Going to create the tabs to allow us to move from one point to another. 
tabs = QTabWidget()

#Going to want to add tabs to this
emails = QWidget()
settings = QWidget()
main = QWidget()
credit_card = QWidget()

#layout = QVBoxLayout()
layout = QFormLayout()

credit_card.setLayout(layout)

#-------------------------------------------------------- Setting the MAIN (Start Task) -------------------------------------------------------

start_task_button = QPushButton('Generate an account',main)


start_task_button.clicked.connect(generate.fubo_action)





#-------------------------------------------------------- Setting the TABS -------------------------------------------------------
tabs.addTab(main, "Main Menu")
tabs.addTab(emails, "Emails")
tabs.addTab(credit_card, "Credit Card")
tabs.addTab(settings,"Settings")


window = QMainWindow()
window.setWindowTitle("Fubo Account Generator")
window.resize(800, 800)
window.setCentralWidget(tabs)


#Now we are going to want to allow a user to enter a bunch of emails -> and passwords. 
#This is going to return a string. We are from this string going to want to parse it and sepearte each.


#If the path already exist in our file we are going to want to display the emails already into the information. 

json_info = {}

if os.path.exists(email_path):
    with open(email_path,"r") as file:
        json_info = json.load(file)
else:
    with open(email_path,"w") as file:
        json_info = "Enter Emails, Make Sure each email is seperate by a : "


print("This is the information \n" , json_info)



#-------------------------------------------------------INFORMATION FOR EMAILS-------------------------------------------------------
textBox_emails = QTextEdit(emails)
textBox_emails.setPlaceholderText("Please Add Emails. ")
#Want to sent the information of textBox_emails to the information we got from the path. -> everytime we view it the list will be displayed. 

corrected_list = decompileInformation()

textBox_emails.setPlainText(corrected_list)
textBox_emails.move(150,150)
textBox_emails.setFixedSize(350,350)

button_save_emails = QPushButton('Save Emails',emails)
button_save_emails.move(250,450)

#What is lambda in python? It says to use lambda. 
button_save_emails.clicked.connect(warning)

#--------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------INFORMATION FOR CREDIT CARD -------------------------------------------------------

#We are going to want to have a layout? 


#Have Information For First and Last name.


LineEdit_First_name = QLineEdit()
LinEdit_Last_name = QLineEdit()

LineEdit_First_name.setPlaceholderText('John')
LineEdit_First_name.setMaxLength(15)

LinEdit_Last_name.setPlaceholderText('Doe')
LinEdit_Last_name.setMaxLength(20)



#Credit Card Information. 
LineEdit_credit_card = QLineEdit(credit_card)
LineEdit_credit_card.setMaxLength(20)
LineEdit_credit_card.setPlaceholderText("1234-5678-9999-9999")

#do not allow the below code, includes a bug / error that doesn't allow us to enter 16 digits and instead only 10. Need another way to verify. 
#LineEdit_credit_card.setValidator(QIntValidator())

#CVV Time
LineEdit_CVV = QLineEdit()
LineEdit_CVV.setMaxLength(4)

#Validates only intergers are added. 
LineEdit_CVV.setValidator(QIntValidator())


#ZipCode Time
LineEdit_ZipCode = QLineEdit()
LineEdit_ZipCode.setPlaceholderText('12345')
#Most US zipcodes are only 5 in length...
LineEdit_ZipCode.setMaxLength(5)
#Validate only intergers are being added
LineEdit_ZipCode.setValidator(QIntValidator())



Combo_Month = QComboBox()

Combo_Month.addItems([
   "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12"

])

Combo_Year = QComboBox()

Combo_Year.addItems([
    "2026",
    "2027",
    "2028",
    "2029",
    "2030",
    "2031",
    "2032",
    "2032"
])


button_credit_card = QPushButton("Save Profile")


LoadProfiles()

layout.addRow("First Name: ", LineEdit_First_name)
layout.addRow("Last Name: ", LinEdit_Last_name)
layout.addRow("Credit Card: ", LineEdit_credit_card)
layout.addRow("CVV: ", LineEdit_CVV)
layout.addRow("Exp. Month: ", Combo_Month)
layout.addRow("Exp. Year:", Combo_Year)
layout.addRow("ZipCode: ",  LineEdit_ZipCode)
layout.addRow(button_credit_card)

button_credit_card.clicked.connect(save_credit_card)




#-------------------------------------------------------WEBHOOK INFORMATION --------------------------------------------------------------------------------------------------------------

#Going to add the discord webhook -> going to be used to send the information for whenever it is done generating.

#Going to want to read if there is already a discord webhook document. 

if os.path.exists(discord_path):
    with open(discord_path, "r") as file:
        discord_url = json.load(file)
else:
    discord_url = {
        "webhook" : "N/A"
    }


#We are going to want to make a layout....
#Create the line edit for the settings.
layout_for_settings = QFormLayout()

#We need this in order for the layout and the widget page to match / link to each other. 
settings.setLayout(layout_for_settings)

LineEdit_discord = QLineEdit()
#Now going to want to fill it in with information. 
LineEdit_discord.setText(discord_url['webhook'])


button_discord = QPushButton("Save Discord URL")
button_discord.clicked.connect(save_discord)

button_test_webhook = QPushButton("Test Webhook!")
button_test_webhook.clicked.connect(test_webhook)


layout_for_settings.addWidget(LineEdit_discord)
layout_for_settings.addWidget(button_discord)
layout_for_settings.addWidget(button_test_webhook)






window.show()

sys.exit(app.exec())