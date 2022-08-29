# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 19:01:23 2022

@author: isalo
"""

""" THIS IS THE WEB SCRAPPER, IT SCRAPS THE SYMBOLS, THE FULL NAMES AND 
THE PRICES OF THE COMPANIES. THEN CALLS A FUNCTION THAT INSERTS 
THOSE VALUES IN A DATABASE"""
    
    
import webbrowser, sys, requests, time, datetime , sys, requests, bs4
from la_base import *


present_time = datetime.datetime.now()
adelanto = datetime.timedelta(hours = 12)
elementos_texto = []
tags = []
prices = []
nombres = []
links = {}
link = 'https://finviz.com/quote.ashx?t='

inicio = 0
final = 25

while present_time < datetime.datetime(2022, 9, 9, 12, 40, 0):
    
        adress = 'https://finance.yahoo.com/etfs'
        #site = webbrowser.open(adress)
        request = requests.get(adress)
        request.raise_for_status()

        file = open('Prueba.txt', 'wb')
        for byte in request.iter_content(100000):
            file.write(byte)
        file.close()    
        
        file = open('Prueba.txt','rb')
        sopa = bs4.BeautifulSoup(file, 'html.parser')
        prueba = sopa.find_all('a')
        elementos = sopa.find_all('a', class_ = "Fw(600) C($linkColor)")
        
        #THESE ARE THE SYMBOLS OF THE COMPANIES (ELEMENTOS TEXTO) 
        #AND THE FULL NAMES (NOMBRES)
        for i in range(0, 25):
            texto = elementos[i]
            elementos_texto.append(texto.get_text())
            nombre = texto['title']
            nombres.append(nombre)
            
        
        #LOOK FOR THE TAGS THAT CONTAIN THE ETF PRICE
        #CLICK ON THE PRICE TO FIND THE ATTRIBUTES
        for i in range(inicio, final):
            siglas = elementos_texto[i]
            set_1 = sopa.find_all(attrs = {'data-symbol' : siglas})
            set_2 = sopa.find_all(attrs = {'data-field' : 'regularMarketPrice'})
        
        #SAME AS ABOVE
            for uno in set_1:
                for dos in set_2:
                    if uno == dos:
                        tag = uno
                        tags.append(tag)
 
            #GETTING THE ETF PRICE AND INSERTING IT ON A LIST
            precio = tag['value']
            prices.append(precio)
            prices = prices

        # LINKS DICTIONARY
        for i in range(inicio, final):
            nombre = nombres[i]
            links[nombre] = link + elementos_texto[i]
               
        
        file.close()        
        
        """INSERT THE DATA INTO THE DATABASE, IF SUCCESSFUL UPDATE 
        VARIABLES AND SLEEP FOR 12 HOURS"""
        
        permiso_1 = segundo_paso(inicio, final, elementos_texto, nombres, links)
        if permiso_1 == True:
            inicio += 25
            final += 25
            present_time += adelanto
                
        time.sleep(43200)





