# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 19:15:15 2022

@author: isalo
"""

""" TAKE VALUES FROM THE ETF DATABASE AND RENDER A TEMPLATE WITH A TABLE TO DISPLAY THEM"""

import sqlite3, flask
from flask import Flask, render_template

lista_siglas = []
lista_nombres = []
lista_apariciones = []
lista_links = []
title = "Table"
hoja = "tabla_etfs.css"

connection = sqlite3.connect('etf.db')
cursor = connection.cursor()

symbols = cursor.execute('select siglas from etf').fetchall()
names = cursor.execute('select nombre from etf').fetchall()
apparitions = cursor.execute('select apariciones from etf').fetchall()
links = cursor.execute('select link from etf').fetchall()

largo = len(symbols)

for i in range(0, largo):
    lista_siglas.append(symbols[i][0])
    lista_nombres.append(names[i][0])
    lista_apariciones.append(apparitions[i][0])
    lista_links.append(links[i][0])
        

cursor.close()
connection.close()

app = Flask(__name__, static_folder = 'static')

@app.route("/")
def pagina():
    return render_template("tabla_etfs.html", title = title, LARGO = largo, lista_siglas = lista_siglas, lista_nombres = lista_nombres, lista_apariciones = lista_apariciones ,lista_links = lista_links) 

if __name__ == '__main__':
    app.run(port = 8080)
