import os
import sys
from os import listdir
import sqlite3
from os.path import isfile, isdir, join

def listdir_recurd(files_list, root, folder, checked_folders):

    if (folder != root):
        checked_folders.append(folder)

    for f in listdir(folder):
        d = join(folder, f)       

        if isdir(d) and d not in checked_folders:
            listdir_recurd(files_list, root, d, checked_folders)
        else:
            if isfile(d):  # si no hago esto, inserta en la lista el nombre de las carpetas ignoradas
                files_list.append(join(f))

    return files_list

def listdir_recurd(files_list, root, folder, checked_folders):

    if (folder != root):
        checked_folders.append(folder)

    for f in listdir(folder):
        d = join(folder, f)       

        if isdir(d) and d not in checked_folders:
            listdir_recurd(files_list, root, d, checked_folders)
        else:
            if isfile(d):  # si no hago esto, inserta en la lista el nombre de las carpetas ignoradas
                files_list.append(join(f))

    return files_list

def total_arch(folder,k):
    n=0
    for f in listdir(folder):   
        if f[2:11]==k:
            n=n+1
    return n




def borraraux():
    if(os.path.exists("a.jpg")):
        try: 
            os.remove("a.jpg")          
        except ValueError:    
            pass
    if(os.path.exists("0.jpg")):
        try:
            os.remove("0.jpg") 
        except ValueError:    
            pass
    if(os.path.exists("1.jpg")):
        try:
            os.remove("1.jpg")
        except ValueError:    
            pass  
    if(os.path.exists("2.jpg")):
        try:
            os.remove("2.jpg") 
        except ValueError:    
            pass
    if(os.path.exists("3.jpg")):
        try:
            os.remove("3.jpg")
        except ValueError:    
            pass
    if(os.path.exists("3.jpg")):
        try:
            os.remove("3.jpg")
        except ValueError:    
            pass
    if(os.path.exists("4.jpg")):
        try:
            os.remove("4.jpg")
        except ValueError:    
            pass
    if(os.path.exists("5.jpg")):
        try:
            os.remove("5.jpg")
        except ValueError:    
            pass     

def borraraux2():
    if(os.path.exists("0.jpg")):
        try:
            os.remove("0.jpg") 
        except ValueError:    
            pass
    if(os.path.exists("1.jpg")):
        try:
            os.remove("1.jpg")
        except ValueError:    
            pass  
    if(os.path.exists("2.jpg")):
        try:
            os.remove("2.jpg") 
        except ValueError:    
            pass
    if(os.path.exists("3.jpg")):
        try:
            os.remove("3.jpg")
        except ValueError:    
            pass
    if(os.path.exists("3.jpg")):
        try:
            os.remove("3.jpg")
        except ValueError:    
            pass
    if(os.path.exists("4.jpg")):
        try:
            os.remove("4.jpg")
        except ValueError:    
            pass
    if(os.path.exists("5.jpg")):
        try:
            os.remove("5.jpg")
        except ValueError:    
            pass        


def borrarauxexp(path):
    if(os.path.exists(path)):
        print(path)
        try: 
            os.remove(path)        
        except ValueError:    
            pass


conn = sqlite3.connect('SIAF.db')
c = conn.cursor()

c.execute('SELECT * FROM EXPEDIENTE_ADMIN')
print( c.fetchone())
print("/n")