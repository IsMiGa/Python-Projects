# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:50:06 2022

@author: isalo
"""

import sqlite3


""" THIS DATABASE KEEPS THE FOLLOWING VALUES OF THE ETFS: SYMBOL, COMPLETE
NAME, NUMBER OF TIMES THE ETF HAS APPEARED ON THE TOP 25 OF THE YAHOO 
FINANCE LIST AND THE LINK TO SEE THE GRAPHIC THAT SHOWS ITS PRICE. 
THIS DATABASE RECIEVES THE NUMBER OF APPARITIONS OF AN ETF
FROM THE SECOND DATABASE. IT IS MEANT TO KEEP RECORDS EVEN WHEN THE
MAIN LOOP STOPS RUNNING. """


def segundo_paso(inicio, final, elementos_texto, nombres, links):
   
    permiso = False
    
    connection = sqlite3.connect('etf.db')
    cursor = connection.cursor()


    cursor.execute('create table if not exists etf(siglas text, nombre text, apariciones integer, link text)')
    connection.commit()

    for i in range(inicio, final):
        siglas = elementos_texto[i]
        nombre = nombres[i]
        link = links[nombre]
    
        #CHECK IF THE ETF EXISTS IN THE DATABASE
        existencia = cursor.execute('select siglas, apariciones from etf where siglas = ?', (siglas,))
        connection.commit()
        existencia = cursor.fetchone()
        
        # CHECK IF THE ETF ALREADY EXISTS IN THE DATABASE, IF IT DOES
        # THE NUMBER OF APPARITIONS IS UPDATED, IF NOT IT IS INTRODUCED IN THE
        # DATABASE
        # fetchone() RETURNS A TUPLE
    
        if existencia != None:
            aparicion = existencia[1] + 1
            valores = (aparicion, siglas)
            cursor.execute('update etf set apariciones = ? where siglas = ?', valores)
            connection.commit()
           
        else:
            aparicion = 1
            cursor.execute('insert into etf (siglas, nombre, apariciones, link) values (?,?,?,?)', (siglas, nombre, aparicion, link))
            connection.commit()    
     
    cursor.close()
    connection.close()
    
    permiso = True
    return(permiso)





"""
con = sqlite3.connect('file:etf.db?mode=rw', uri=True)
chequear si la database existe
"""