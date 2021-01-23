from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import time, smtplib, sys

# Web scraping function
def scrapeSite():
    my_url = 'https://www.ruhealth.org/covid-19-vaccine' #web URL
    uClient = uReq(my_url) #open URL
    page_html = uClient.read() #read URL contents
    uClient.close() #close URL

    page_soup = soup(page_html, 'html.parser') #parse URL data

    containers = page_soup.find('table',{'class':'table'}).findAll('tr') #look for all the elements within the table

    return containers #return elements within the table

def sendEmail():
    # set the 'from' address,
    fromaddr = senderEmail
    # set the 'to' addresses,
    #toaddrs  = ['AN_EMAIL_ADDRESS','A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']
    toaddrs = receiverEmail
    
    # setup the email server,
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # add my account login name and password,
    server.login(senderEmail, senderEmailPass)
    
    # Print the email's contents
    print('From: ' + fromaddr)
    print('To: ' + str(toaddrs))
    print('Message: ' + msg)
    
    # send the email
    server.sendmail(fromaddr, toaddrs, msg)
    # disconnect from the server
    server.quit()

#--- END FUNCTIONS ---#

print('''\n\
Welcome to the (Unofficial) Riverside County COVID-19 Vaccine Clinic alert program!  
This is an imperfect, yet functional program. 
(Sure beats having to check the website every 30 minutes though!)
Please make sure the information you input is correct or else you will not receive an update!\n''')

senderEmail = input('What is your email address?\n\
(Please make sure your Gmail\'s "Less Secure App Access" setting is turned ON.)\n').strip()

senderEmailPass = input('''\nWhat is your password?\n\
(The program needs it to create the alert and send it to you via your own email.)\n''').strip() 

receiverEmail = senderEmail
print('\nThank you! I\'ll be continously checking the website every 20 minutes for you! You\'ll get an email once something changes.')

# continuously run function
while True:
    #try to scrape webpage
    try: 
        check1 = scrapeSite() # extract table data
        time.sleep(1200) # wait 20mins
        check2 = scrapeSite() # extract table data again to a diff variable

        # if vaccination table has not changed
        if len(check1) == len(check2):
            # continue with the script,
            continue

        # if vaccination table has changed,
        elif len(check1) != len(check2):
            # Try to send email about update
            try:
                # create an email message with just a subject line,
                msg = """\
                Subject: COVID-19 Vaccine Clinic Update!

                The website registration website has been updated! Either more sites have been added, or sites have been removed. 

                I'm not that advanced, so I don't know which one is the case, but you should go check it out! 

                Here's the link: https://www.ruhealth.org/covid-19-vaccine 

                Make sure to stop running the program (and turn Gmail\'s "Less Secure App Access" setting back OFF) if you got the result you expected. If not, I'll keep checking for more updates.

                Best, 
                RH-Check """

                sendEmail()
                
                continue #continue with script
            # Update could not be emailed
            except:
                print('\nThere was an update! However, you didn\'t get an alert because your email and/or password were incorrect.')
                print('Please try running the script again with the correct information to receive updates.')
                sys.exit()
        
        #check for script error
        else:
            # try to send email of script error
            try:
                # create an email message with just a subject line,
                msg = """\
                Subject: SCRIPT ERROR!

                Something went wrong! Please try re-running the script to continue staying updated.

                Best, 
                RH-Check """
                
                sendEmail()
                
                sys.exit() #end script
            # Script error could not be emailed
            except:
                print('\nSeems like I\'ve encountered an error! Sorry about that! \nHowever, you didn\'t get an alert because your email and/or password were incorrect.')
                print('Please try running the script again with the correct information to receive email updates.')
                sys.exit()
    #Exit script if any user/script eroors
    except SystemExit:
        sys.exit()
    #Exit script if user exits
    except KeyboardInterrupt:
        print('')
        sys.exit()
    # Webscrape error
    except:
        # try to send email of webscrape error
        try:
            # create an email message with just a subject line,
            msg = """\
            Subject: UNKNOWN ERROR!

            There might be an error with the website. Try running the script again later to keep receiving updates.
            
            If the website is up and running, I might need to be updated. 

            Best, 
            RH-Check """
            
            sendEmail()
            
            sys.exit() #end script
        # Webscrape error could not be emailed
        except:
            print('\nERROR! There might be an error with the website. If the website is up and running, I might need to be updated. \nHowever, you didn\'t get an alert because your email and/or password were incorrect.')
            print('Please try running the script again with the correct information to receive email updates.')
            sys.exit()
