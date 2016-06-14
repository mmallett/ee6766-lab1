import mraa
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime
import pyupm_i2clcd as lcd
import math

def flash():
    buzz_pin_number=6

    buzz = mraa.Gpio(buzz_pin_number)

    buzz.dir(mraa.DIR_OUT)

    for i in range(1, 5):
        buzz.write(1)
        time.sleep(.2)
        buzz.write(0)
        time.sleep(.2)

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

def getip():
    arg='ip route list'  # Linux command to retrieve ip addresses.
    # Runs 'arg' in a 'hidden terminal'.
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()  # Get data from 'p terminal'.

    # Split IP text block into three, and divide the two containing IPs into words.
    ip_lines = data[0].splitlines()
    split_line_a = ip_lines[1].split()
    split_line_b = ip_lines[2].split()

    # con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
    ip_type_a = connect_type(split_line_a)
    ip_type_b = connect_type(split_line_b)

    """Because the text 'src' is always followed by an ip address,
    we can use the 'index' function to find 'src' and add one to
    get the index position of our ip.
    """
    ipaddr_a = split_line_a[split_line_a.index('src')+1]
    ipaddr_b = split_line_b[split_line_b.index('src')+1]

    return [(ip_type_a, ipaddr_a), (ip_type_b, ipaddr_b)]

def mail():
    # CHANGE TO YOUR ACCOUNT INFORMATION
    # Account Information
    to = 'mmallett91@gmail.com' # Email to send to.
    gmail_user = 'matt.mallett.iot@gmail.com' # Email to send from. (MUST BE GMAIL)
    gmail_password = 'monkeymonkey' # Gmail password.
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

    smtpserver.ehlo()  # Says 'hello' to the server
    smtpserver.starttls()  # Start TLS encryption
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)  # Log in to server
    today = datetime.date.today()  # Get current time/date

    ips = getip()

    # Creates a sentence for each ip address.
    my_ip_a = 'Your %s ip is %s' % ips[0]
    my_ip_b = 'Your %s ip is %s' % ips[1]

    # Creates the text, subject, 'from', and 'to' of the message.
    msg = MIMEText(my_ip_a + "\n\n" + my_ip_b)
    msg['Subject'] = 'IPs For Intel Edison on %s' % today.strftime('%b %d %Y')
    msg['From'] = gmail_user
    msg['To'] = to
    # Sends the message
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()

def readtemp():

    tempSensor = mraa.Aio(1)
    a = tempSensor.read()

    b=4275

    r = 1023.0/a-1.0;
    r = 100000.0*r;

    return 1.0/(math.log(r/100000.0)/b+1/298.15)-273.15;

def screen():
    ips = getip()

    temp = readtemp()

    # Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
    myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

    myLcd.setCursor(0,0)

    # RGB Red
    myLcd.setColor(255, 255, 0)

    myLcd.write(ips[0][1])
    myLcd.setCursor(1,0)
    myLcd.write(str(temp))

    while(1):
        pass


flash()
screen()
# mail()
