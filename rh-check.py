from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import time
import smtplib

# Web scraping function
def scrapeSite():
    my_url = 'https://www.ruhealth.org/covid-19-vaccine' #web URL
    uClient = uReq(my_url) #open URL
    page_html = uClient.read() #read URL contents
    uClient.close() #close URL

    page_soup = soup(page_html, 'html.parser') #parse URL data

    containers = page_soup.find('table',{'class':'table'}).findAll('tr') #look for all the elements within the table

    return containers #return elements within the table

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
    check1 = scrapeSite() # extract table data
    time.sleep(10) # wait 20mins
    check2 = scrapeSite() # extract table data again to a diff variable

    # if vaccination table has not changed
    if len(check1) != len(check2):
        # continue with the script,
        continue

    # if vaccination table has changed,
    elif len(check1) == len(check2):
        # create an email message with just a subject line,
        msg = """\
        Subject: COVID-19 Vaccine Clinic Update!

        The website registration website has been updated! Either more sites have been added, or sites have been removed. 

        I'm not that advanced, so I don't know which one is the case, but you should go check it out! 

        Here's the link: https://www.ruhealth.org/covid-19-vaccine 

        Make sure to stop running the program (and turn Gmail\'s "Less Secure App Access" setting back OFF) if you got the result you expected. \
        If not, I'll keep checking for more updates.

        Best, 
        RH-Check """

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
        
        continue #continue with script
    
    #check for error
    else:
        # create an email message with just a subject line,
        msg = """\
        Subject: SCRIPT ERROR!

        Something went wrong! Please try re-running the script to continue staying updated.

        Best, 
        RH-Check """
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
        
        break #break out of script
