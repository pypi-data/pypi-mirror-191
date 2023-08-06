#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:13:52 2023

@author: marcio
"""

import numpy as np
import re
def Metal(entrada):
    linhas = []
    lista_up = []
    lista_down = []
    klines = []
    k2 = []
    with open(entrada, 'r') as nscf:
        for lines in nscf:
            linhas.append(lines)
            if "SPIN UP" in lines:
                up = lines
            elif "SPIN DOWN" in lines:
                down = lines
            elif "Fermi" in lines:
                Fermi = lines
                E_Fermi = lines[25:40].split()
            elif "k" in lines[10:12]:
                klines.append(lines)
    for i in linhas[linhas.index(up)+3:linhas.index(down)-1]:
        if i != "\n":
            lista_up.append(i.rstrip())
    for j in linhas[linhas.index(down)+3:linhas.index(Fermi)-1]:
        if j != "\n":
            lista_down.append(j.rstrip())
    for l in klines:
        if l in linhas:
            k2.append(l.rstrip())
    linhas.clear(), klines.clear() ###redefine as listas linhas e klines
    for x in k2:
        if x in lista_up:
            lista_up[lista_up.index(x)] = "\n"
            #pass
        if x in lista_down:
            lista_down[lista_down.index(x)] = "\n"
    ###################        SPIN  UP       ################################
    str_up = "".join(map(str,lista_up))
    #print(string)
    spin_up = []
    spin_up.append(str_up.split('\n'))
    spin_up[0].pop(0)
    lista_final_up = []
    for i in spin_up[0]:
        lista_final_up.append(list(map(float, i.split())))
    matriz_up = np.array(lista_final_up)
    matriz_up = matriz_up - float(E_Fermi[0])
    ###################        SPIN  DOWN     ################################
    str_down = "".join(map(str,lista_up))
    #print(string)
    spin_down = []
    spin_down.append(str_down.split('\n'))
    spin_down[0].pop(0)
    lista_final_down = []
    for j in spin_down[0]:
        lista_final_down.append(list(map(float, j.split())))
    matriz_down = np.array(lista_final_down)
    matriz_down = matriz_down - float(E_Fermi[0])
    return matriz_up, matriz_down
def AMetal(entrada):
    linhas = [] #salva todas as linhas do arquivo .out
    klines = [] #salva os k's que indica o início e fim das bandas
    #k2 = [] #lista de controle
    with open(entrada, 'r') as nscf:
        for lines in nscf:
            linhas.append(lines)
            if "End of band structure calculation" in lines:
                start = lines
            elif "highest" in lines:
                highest = lines
                high = re.sub('[^-.0-9]+', ' ', str('%s' %(highest)))
                energy = high.split()
            elif "k" in lines[10:12]:
                klines.append(lines)
    lista = [ a.rstrip() for a in linhas[linhas.index(start)+4:linhas.index(highest)-1]]
    lista1 = [b.rstrip() for b in klines if b in linhas]
    for c in lista1:
        if c in lista:
            lista[lista.index(c)] = "\n"
    lista3 = [i for i in lista if i != '']
    string = "".join(map(str,lista3))
    spin_up = []
    spin_up.append(string.split('\n'))
    spin_up[0].pop(0)
    lista_final = []
    for i in spin_up[0]:
        lista_final.append(list(map(float, i.split())))
    matriz = np.array(lista_final)
    matriz = matriz - float(energy[0])
    return matriz
    
