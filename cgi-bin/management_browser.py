#Het importeren van de benodigde modules.
from pysimplesoap.client import SoapClient, SoapFault
import re
import cgi, cgitb 
cgitb.enable()
from lxml import etree
import time
import logging
import ConfigParser
import sqlite3
import csv

#Variable Tijd van Uitvoeren
now = time.strftime("%c")

# XML importeren
xml = 'config.xml'
tree = etree.parse(xml)

#Het inladen van de invoervelden.
form = cgi.FieldStorage()
agentinput = (form.getvalue('agentnumber'))
input = (form.getvalue('command'))

#Het controleren van de input in het agent veld. 
if not re.match("[1-2]{1}",agentinput):
    print "Content-Type: text/html"
    print
    print '''\
    <html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body>De invoer in het agent veld is onjuist.</body>
    </html>
    '''
    quit()

#Het controleren van de input in het input veld. 
if not re.match("[1-6]{1}",input):
    print "Content-Type: text/html"
    print
    print '''\
    <html>
    <head><title>Management Console</title></head>
    <body>De invoer in het input veld is onjuist.</body>
    </html>
    '''
    quit()
    
#Variabelen agent
location1 = tree.xpath('/config/agent[1]/location/text()')
action1 = tree.xpath('/config/agent[1]/action/text()')
namespace1 = tree.xpath('/config/agent[1]/namespace/text()')
soap_ns1 = tree.xpath('/config/agent[1]/soap_ns/text()')
ns1 = tree.xpath('/config/agent[1]/ns/text()')

#Variabelen agent2
location2 = tree.xpath('/config/agent[2]/location/text()')
action2 = tree.xpath('/config/agent[2]/action/text()')
namespace2 = tree.xpath('/config/agent[2]/namespace/text()')
soap_ns2 = tree.xpath('/config/agent[2]/soap_ns/text()')
ns2 = tree.xpath('/config/agent[2]/ns/text()')

#Het vergelijken van de input (agent).
if agentinput == "1":
    client = SoapClient(
        location = location1[0],
        action = action1[0],
        namespace = namespace1[0],
        soap_ns = soap_ns1[0],
        ns = False)

elif agentinput == "2":
    client = SoapClient(
        location = location2[0],
        action = action2[0],
        namespace = namespace2[0],
        soap_ns = soap_ns2[0],
        ns = False)

#Logging
logging.basicConfig(filename='log.log',level='INFO',
    format='%(asctime)s : %(levelname)s : %(message)s')
logging.info('Het script is gestart op agent %s', agentinput)

#Connection database
datab = sqlite3.connect("""C:\inetpub\python\cgi-bin\Database\logDB.sqlite""")
c=datab.cursor()

#Hier wordt er een testwaarde opgevraagd. Dit is ter controle van de verbinding.
try:
    print "Content-Type: text/html"
    print
    print '''\
    <html>
    <head><title>Management Console</title></head>
    <body></body>
    </html>
    '''
    r0=str(client.get_value(number=0).resultaat)

except:
    print '''\
    <html>
    <head><title>Management Console</title></head>
    <body>Er is iets misgegaan met verbinden.</body>
    </html>
    '''
    logging.info('Er kan geen verbinding gemaakt worden met agent %s', agentinput)
    quit()

#De usernaam wordt altijd opgehaald ter behoeve van registratie in de database
r2=str(client.get_value(number=2).resultaat)

#Hier worden de Powershell scripts op de agent aangeroepen.
if (input) == "1":
    r1=str(client.get_value(number=1).resultaat)
    print """<html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> OS: %s </h1></body>
    </html>""" % r1
    #Logging
    logging.info('Het OS is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r1,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r1))
    f.close()

elif (input) == "2":
    r2=str(client.get_value(number=2).resultaat)
    print""" <html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> Ingelogde User: %s </h1></body>
    </html>""" % r2
    #Logging
    logging.info('De ingelogde user is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r2,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r2))
    f.close()

elif (input) == "3":
    r3=str(client.get_value(number=3).resultaat)
    print """<html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> Beschikbare RAM: %s </h1></body>
    </html>""" % r3
    #Logging
    logging.info('Het beschikbare RAM geheugen is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r3,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r3))
    f.close()

elif (input) == "4":
    r4=str(client.get_value(number=4).resultaat)
    print """<html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> Beschikbare ruimte op C: %s </h1></body>
    </html>""" % r4.rstrip()
    #Logging
    logging.info('De beschikbare opslag op C: is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r4,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r4))
    f.close()

elif (input) == "5":
    r5=str(client.get_value(number=5).resultaat)
    print  """<html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> IP adres: %s </h1></body>
    </html>""" % r5.rstrip()
    #Logging
    logging.info('Het IP adres is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r5,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r5))
    f.close()
    
elif (input) == "6":
    r6=str(client.get_value(number=6).resultaat)
    print  """<html>
    <head><title>Management Console</title></head>
    <link rel="stylesheet" type="text/css" href="stylesheet.css" />
    <body><h1> De Uptime is: %s </h1></body>
    </html>""" % r6.rstrip()
    #Logging
    logging.info('de Uptime is opgevraagd op agent %s', agentinput)
    #Database
    c.execute("insert into Request values(?,?,?,?)",(agentinput,input,r6,r2,))
    datab.commit()
    #Export CSV
    f = open("csvlog.csv", 'a')
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    writer.writerow((now,agentinput,input,r6))
    f.close()

#Het beeindigen van de aanvraag wordt gelogd.    
logging.info("Aanvraag uitgevoerd")

#Het script wordt opnieuw ingeladen, zodat er een nieuwe waarde kan worden opgevraagd.
print """<form action="/cgi-bin/management_browser.py" method="post">
Agentnr: <input type="text" name="agentnumber"><br />
Command: <input type="text" name="command"><br />
<input type="submit" value="Submit" /></center>
</form>
<h3>Toelichting Agentnr:</h3>
1: Agent 1 <br/>
2: Agent 2 <br/>

<h3>Toelichting Command:</h3>
1: OS versie opvragen <br/>
2: Gebruikersnaam ingelogde gebruiker opvragen <br/>
3: Hoeveelheid beschikbaar RAM opvragen <br/>
4: Hoeveelheid beschikbare ruimte C: opvragen <br/>
5: IP adres opvragen <br/>
6: Uptime opvragen <br/>
"""


