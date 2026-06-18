#This file is going to be used to connect to fubo and generate an account



import requests
import playwright
import os
import json


from playwright.sync_api import sync_playwright

#URL used to sign up. 
main_url = 'https://www.fubo.tv/signup'

account_path = 'emails.json'
credit_path = 'credit_card.json'
discord_path = 'discord.json'


def fubo_action():

    print('We are live connected ')
    #Before We Do this we are goinng to want extract a email and going to want to extract the password with it.
    user_name, password, zipcode,first_name,last_name,cc_number,cvv_number,exp_month, exp_year = get_account() 


    with sync_playwright() as p:

        #going to generate a browser. 
        #user_data_dir = "./chromeInformation" 

        # browswer = p.chromium.launch_persistent_context(
        #     user_data_dir,
        #     headless=False,
        #     #will use the default installed google chrome path
        #     channel="chrome",
        #     args=["--disable-blink-features=AutomationControlled"],
        #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # Set custom user-agent  # Use the dynamically found Chrome path
        # )

        # browswer.add_init_script("""
        #     Object.defineProperty(navigator, 'webdriver', {
        #         get: () => undefined
        #     });
        # """)

        browswer = p.chromium.launch(
            headless=False,
            #will use the default installed google chrome path
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )

       


        # browswer = p.chromium.launch_persistent_context(
        #     user_data_dir,
        #     headless=False,
        #     #will use the default installed google chrome path
        #     channel="chrome",
        #     args=["--disable-blink-features=AutomationControlled"],
        #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # Set custom user-agent  # Use the dynamically found Chrome path
        # )

        # browswer.add_init_script("""
        #     Object.defineProperty(navigator, 'webdriver', {
        #         get: () => undefined
        #     });
        # """)


        new_page = browswer.new_page()

        #Send the page to our new_page. 
        new_page.goto(main_url)


        #Going to want to click on this button. 
        new_page.get_by_role("button", name='Next').click()

       

        new_page.get_by_test_id("sign-up-email-fld").fill(user_name)

        new_page.get_by_test_id("sign-up-password-fld").fill(password)

        new_page.get_by_test_id("sign-up-zip-fld").fill(zipcode)

        new_page.get_by_test_id("sign-up-zip-confirm-btn").click()

        new_page.get_by_test_id("sign-up-continue-btn").click()

        #want to debug this in order to make it work properly. 



        #---------------------------------------SOLVE ISSUE OF ALREADY HAVING EMAIL ----------------------------------------------------------------------------
        

        #new_page.pause()

        #Potential error -> user already has an account with associated email. 
        error = new_page.get_by_text("You already have an account.")

        #The try and except in python (Used to handle errors. )
        #Will try to run the code in the try -> if it runs perfect then
        #Will skip the except.
        #If it can't run it without error -> then runn except. 
        try:
            
            error.wait_for(state="visible",timeout=5000)
            #We are going to want to close this browswer -> update the information asscociated with the email and make sure it's good.
            print('This accout already has been made. ')
            #Browswer close. 

            #Update information as marked as used. 
            update_account(user_name)
            #Close the page and return. 
            new_page.close()
            return

        except:
            print('We are fine. ')

        
        error = new_page.get_by_role("heading", name="Please start over with a")

        try:
            error.wait_for(state='visible', timeout=5000)

            print('The email is not valid / was flagged. Please try another one. ')
            #Going to want to update this account to make sure we do not use it again. 
            update_account(user_name)

            new_page.close()
            return

        except:
            print('We are fine')



        #Potential error. -> whenever our email is flagged to be different / not correct.  
        error = new_page.locator("a").filter(has_text="Continue with")
        #new_page.locator("a").filter(has_text="Continue with")

        try:
            #want to see if the error is located on the screen. 
            error.wait_for(state='visible', timeout=5000)
            #We are going to want to click it. 
            new_page.locator("a").filter(has_text='Continue with').click()

            #Now we are going to have to verify with the code -> have the user enter the code. 
            #THE code from email....
            #Can eventually put in logic / code in here to make it work better. 

            #This is going to refresh / reload the page, the timeout here is used for ?...

            new_page.wait_for_timeout(5000)
            
            new_page.reload(timeout=4000)

            #SEEMS WE WANT TO REFRESH THE BROWSWER HERE.... SEEMS IT GETS STUCK. 
            error = new_page.get_by_role("heading", name="Please verify your email")

            try:
                #We have to have the people enter the code here....
                error.wait_for(state='visible',timeout=5000)

            except:
                print('We are fine. ')

            

        except:
            print('We are fine. ')

        #new_page.pause()


        #This popped up as an error -> idk anything about it 
        #get_by_role("heading", name="Please start over with a")


        #Wait for this too load. 
        new_page.get_by_test_id("plan_selection_interstitial_btn").wait_for(timeout=0)


        
        new_page.get_by_test_id("plan_selection_interstitial_btn").click()

        #We are going to want to get the days of the free trial to know when to cancel it.  
        days_text = new_page.get_by_text("days").first.text_content()
        print(days_text)


        new_page.get_by_test_id("package-page-continue-button").click()


        new_page.get_by_test_id("switch-quarterly-btn-update").click()

        new_page.get_by_test_id("payment_interstitial_btn").click()


        new_page.get_by_test_id("cc-first-name-fld").fill(first_name)

        new_page.get_by_test_id("cc-last-name-fld").fill(last_name)


        #going to want to puase here because something is wrong with the frames suggested by the extension. 
        #We are going to want to first 

        #Here we are going find the ifram (The frame that is going to be used to place the credit/card info)

        # <iframe allowtransparency="true" frameborder="0" scrolling="no" name="recurly-element--jsdFd2rGhVoZ6Fjg" allowpaymentrequest="true" style="background: none; width: 100%; height: 100%;"
        # title="Billing information" src="https://api.recurly.com/js/v1/field.html#config=%7B%22style%22%3A%7B%22placeholder%22%3A%7B%22content" \
        # "%22%3A%7B%22number%22%3A%22___%20___%20___%20___%22%2C%22expiry%22%3A%22MM%20%2F%20YY%22%7D%7D%2C%22title%22%3A%22Card%20Details%22%2C%22fontFamily" \
        # "%22%3A%22Helvetica%2CArial%2Csans-serif%22%2C%22fontWeight%22%3A%22normal%22%2C%22fontSize%22%3A%220.875rem%22%2C%22lineHeight%22%3A%221.5%22%2C%22fontColor" \
        # "%22%3A%22%23000000%22%7D%2C%22busGroupId%22%3A%22VFBHNXzi3eydZSQU%22%2C%22deviceId%22%3A%22bQOyfCOrGcLj7NmA%22%2C%22elementId%22%3A%22jsdFd2rGhVoZ6Fjg%22%2C" \
        # "%22recurly%22%3A%7B%22currency%22%3A%22USD%22%2C%22timeout%22%3A60000%2C%22publicKey%22%3A%22sjc-uR3SmPHcQnBYE5yBXVEcIH%22%2C%22parent%22%3Atrue%2C%22parentVersion" \
        # "%22%3A%224.43.0%22%2C%22cors%22%3Atrue%2C%22engage%22%3A%7B%22enabled%22%3Atrue%7D%2C%22fraud%22%3A%7B%22kount%22%3A%7B%22dataCollector%22%3Atrue%7D%2C%22litle%22%" \
        # "3A%7B%7D%2C%22braintree%22%3A%7B%7D%7D%2C%22report%22%3Afalse%2C%22risk%22%3A%7B%22threeDSecure%22%3A%7B%22preflightDeviceDataCollector%22%3A%7B%22enabled%22%3Atrue%" \
        # "7D%2C%22proactive%22%3A%7B%22enabled%22%3Afalse%2C%22gatewayCode%22%3A%22%22%7D%7D%7D%2C%22api%22%3A%22https%3A%2F%2Fapi.recurly.com%2Fjs%2Fv1%22%2C%22required%22%3" \
        # "A%5B%22number%22%2C%22month%22%2C%22year%22%2C%22first_name%22%2C%22last_name%22%5D%2C%22fields%22%3A%7B%22all%22%3A%7B%22style%22%3A%7B%7D%7D%2C%22number%22%3A%7B" \
        # "%22selector%22%3A%22%5Bdata-recurly%3Dnumber%5D%22%2C%22style%22%3A%7B%7D%7D%2C%22month%22%3A%7B%22selector%22%3A%22%5Bdata-recurly%3Dmonth%5D%22%2C%22style%22%3A%7" \
        # "B%7D%7D%2C%22year%22%3A%7B%22selector%22%3A%22%5Bdata-recurly%3Dyear%5D%22%2C%22style%22%3A%7B%7D%7D%2C%22cvv%22%3A%7B%22selector%22%3A%22%5Bdata-recurly%3Dcvv%5D%2" \
        # "2%2C%22style%22%3A%7B%7D%7D%2C%22card%22%3A%7B%22selector%22%3A%22%5Bdata-recurly%3Dcard%5D%22%2C%22style%22%3A%7B%7D%7D%7D%7D%2C%22sessionId%22%3A%22eoXK6bTjT0kXX" \
        # "sar%22%2C%22type%22%3A%22card%22%7D" data-airgap-id="122" tabindex="0" aria-label="Card info"></iframe>

        #Locates the frame with name Card info.
        credit_frame = new_page.frame_locator('iframe[aria-label="Card info"]')


        #Input one for the program we are dealing with. 

        # <input id="recurly-hosted-field-input" type="text" pattern="[0-9\/\s]*" spellcheck="false" autocapitalize="none" autocorrect="off" class="recurly-hosted-field-input recurly-hosted-field-input-number"
        # autocomplete="cc-number" inputmode="numeric" placeholder="___ ___ ___ ___" title="___ ___ ___ ___" 
        # aria-label="___ ___ ___ ___" aria-required="true" style="visibility: visible; color: rgb(0, 0, 0); " \
        # "font-family: Helvetica, Arial, sans-serif; font-feature-settings: normal; font-kerning: auto; font-size: " \
        # "0.875rem; font-stretch: normal; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: " \
        # "normal; line-height: 1.5; text-rendering: auto; text-shadow: none; text-transform: none;">

        credit_frame.get_by_label('___ ___ ___ ___').fill(cc_number)


        #Input for the month / year


        # <input type="text" inputmode="numeric" pattern="[0-9\/\s]*" spellcheck="false" autocapitalize="none" autocorrect="off" 
        # class="recurly-hosted-field-input recurly-hosted-field-input-expiry" placeholder="MM / YY" title="MM / YY" aria-label="MM / YY" 
        # autocomplete="cc-exp" aria-required="true" style="color: rgb(0, 0, 0); font-family: Helvetica, Arial, sans-serif; font-feature-settings:" \
        # " normal; font-kerning: auto; font-size: 0.875rem; font-stretch: normal; font-style: normal; font-variant: normal; font-weight: normal; "
        # "letter-spacing: normal; line-height: 1.5; text-rendering: auto; text-shadow: none; text-transform: none; visibility: visible;">

        #We are going to get both of the numbers and combine them. 
        month_and_year = exp_month + exp_year

        credit_frame.get_by_label("MM / YY").type(month_and_year,delay=1000)

        #Input for the cvv. 

        # <input type="text" inputmode="numeric" pattern="[0-9\/\s]*" spellcheck="false" autocapitalize="none" autocorrect="off" class="recurly-hosted-field-input recurly-hosted-field-input-cvv" placeholder="CVV" title="CVV" aria-label="CVV" 
        # autocomplete="cc-csc" aria-required="true" style="color: rgb(0, 0, 0); " \
        # "font-family: Helvetica, Arial, sans-serif; font-feature-settings: normal;" \
        # " font-kerning: auto; font-size: 0.875rem; font-stretch: normal; font-style: normal;" \
        # " font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: 1.5; " \
        # "text-rendering: auto; text-shadow: none; text-transform: none; visibility: visible;">

        credit_frame.get_by_label("CVV").type(cvv_number)
     
        # new_page.locator("iframe[name=\"recurly-element--xL4bpV34Qgahg2h0\"]").content_frame.get_by_role("textbox", name="___ ___ ___ ___").fill(cc_number)

        # new_page.locator("iframe[name=\"recurly-element--xL4bpV34Qgahg2h0\"]").content_frame.get_by_role("textbox", name="MM / YY").fill(exp_month)

        new_page.get_by_test_id("cc-zip-fld").type(zipcode)

        #This is going to be the last we select.....
        #new_page.pause()
        new_page.get_by_test_id("sign-up-payment-btn").click()

        #Want to pause after clicking and verify everything works good. 
        success = new_page.get_by_role("heading", name="You are subscribed!")


        try:
            success.wait_for(state='visible',timeout=5000)

            #Now update the profile. -> showing that we succesuffly signed up. 
            update_account(user_name)

            #Now we are going to want to send webhook to notify that we have offically completed the task. 
            send_webhook(user_name,password,days_text)
            
        
        except:
            print('Error and we did not succesfully sign up')
        
        new_page.pause()

        #From this page we are going to want to wait for some dumb sh.

def send_webhook(user_name, pw, length_until_expire = "?"):

    #Now we need to get the users discord. 
    if os.path.exists(discord_path):
        with open (discord_path, 'r') as file:
            discord_info = json.load(file)
    else:
        print('Error, no file exist for the discord webhook, please save one.')
        return

    #Now that we got the webhook we are going to want to send it. 

    discord_url = discord_info['webhook']

    #Build the webhook before we send it. 
    webhook = {

        "username" : "FuboBot",

        'embeds' : [
            {
                'title' : "Succesfully Generated!🥳",
                
                "fields" : [
                    {
                        "name" : 'Email Associated',
                        "value" : user_name
                    },
                    {
                        'name' : 'Password',
                        'value' : f"||{pw}||"
                        
                    },
                    {
                        'name' : 'length of trial',
                        'value' : length_until_expire
                    }

                ]       
            }               
        ]
    }


    #Now we are going to want to send the request. 
    request_info = requests.post(discord_url,json = webhook)

    if request_info.status_code != 204:
        print('Error sending discord webhook, please make sure correct discord webhook is saved. ')
    else:
        print('Succesfully sent the discord webhook. ')

    


def get_account():

    print('We are going to get an account that hasn''t been used' )
    #Json file already sort of returns a dictonarie of such. 
    json_file = {}

    #Get all the accounts.
    with open(account_path, "r") as file:
        json_file = json.load(file)

    with open(credit_path,'r') as file:
        credit_json = json.load(file)


    #Now this is going to return an object of information.... 

    for email in json_file:
        #Going to want to go through an return the first one that hasn't been used. 
        if email['has_been_used'] == False:
            return email['email'], email['password'], credit_json['zipcode'],credit_json['first_name'],credit_json['last_name'],credit_json['credit_number'],credit_json['cvv'],credit_json['exp_month'],credit_json['exp_year']


def update_account(user_email):

    #Going to want to open the file -> mark it as updated and return it. 

    #We are going to want to read and open the file. 
    account_info = {}

    with open(account_path, 'r') as file:
        account_info = json.load(file)
    
    file.close()
    #Going to want to open the file now to write too
    with open(account_path, 'w') as file:
        #Now going to go through all the accounts in here. 
        for email in account_info:
            if email['email'] == user_email:
                email['has_been_used'] = True
                break
        #Reset the offset of the reading back to the start of the file. 
        file.seek(0)
        json.dump(account_info,file,indent=2)

    
    





    

    


    