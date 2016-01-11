#Authors: Edwin van Tuijl & Glenn Scholten

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
import sys,subprocess

# ---------------------------------------------------------

def get_value(number):
    "return the result of one of the pre-define numbers"
    print "get_value, of of item with number=",number

    #Voor diagnostische doeleinden. Niet te benaderen door de eindgebruiker.
    if number == 0:
        output = "De verbinding is tot stand gebracht."
        return output
    
    # Opvragen OS versie
    if number == 1:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\1.ps1'], 
        stdout=subprocess.PIPE)                 
        output = p.stdout.read()                 
        return output

    # Opvragen Username
    if number == 2:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\2.ps1'],  
        stdout=subprocess.PIPE)                  
        output = p.stdout.read()                 
        return output

    # Opvragen RAM
    if number == 3:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\3.ps1'],  
        stdout=subprocess.PIPE)                  
        output = p.stdout.read()                 
        return output

    # Opvragen Vrije Ruimte C:
    if number == 4:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\4.ps1'],  
        stdout=subprocess.PIPE)                  
        output = p.stdout.read()                 
        return output

    # Opvragen IP adres
    if number == 5:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\5.ps1'],  
        stdout=subprocess.PIPE)                  
        output = p.stdout.read()                 
        return output

    # Opvragen Uptime
    if number == 6:
        p=subprocess.Popen(['powershell.exe',    
            '-ExecutionPolicy', 'Unrestricted',  
            'c:\\scripts\\6.ps1'],  
        stdout=subprocess.PIPE)                  
        output = p.stdout.read()                 
        return output

    
    # Last value
    return None


# ---------------------------------------------------------

# Soap instellingen
port=8008
dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# Soap variabelen
dispatcher.register_function('get_value', get_value,
    returns={'resultaat': str},   # return data type
    args={'number': int}         # it seems that an argument is mandatory, although not needed as input for this function: therefore a dummy argument is supplied but not used.
    )

# Soap listening settings
print "Starting server on port",port,"..."
httpd = HTTPServer(("", port), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()

