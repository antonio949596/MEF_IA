import selenium 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import  sqlite3
from PIL import Image,ImageChops
import time
import os.path 
import argparse
from os import listdir



import numpy as np
import cv2

import matplotlib.pyplot as plt
import operator
import os
import time
import leer

def binarizacion(imagen, umbral):
    ancho, alto = imagen.size
    pix = imagen.load() 
    output = Image.new("L", (ancho, alto))
    out_pix = output.load()
    for i in range(ancho):
        for j in range(alto):
            if pix[i, j] >umbral: out_pix[i, j] = 255
            else: out_pix[i, j] = 0
    return output

def dilation(n):
    imagen = cv2.imread("a.jpg",0)
    #Crear un kernel de '1' de nxn
    kernel = np.ones((n,n),np.uint8) 
    #Se aplica la transformacion: Erode
    transformacion = cv2.dilate(imagen,kernel,iterations = 1)
    cv2.imwrite("a.jpg" ,transformacion)


def pixels_total_horizontal(imagen):
    w, h = imagen.size
    pix = imagen.load() 
    histog=w*[0]
    for i in range(w):
        c=0
        for j in range(h):
            if pix[i,j]==255:
                c=c+1
        histog[i]=c
    return histog


def pixels_total_vertical(imagen):
    w, h = imagen.size
    pix = imagen.load() 
    histog=h*[0]
    for j in range(h):
        c=0
        for i in range(w):
            if pix[i,j]==255:
                c=c+1
        histog[j]=c
    return histog

def corte(imagen,m,n):
    w1, h1 = imagen.size
    c1=pixels_total_horizontal(imagen)
    for i1 in range(w1):
        if c1[i1]>m:
            T=imagen.crop((i1-1,0,w1,h1))
            break
    w2, h2 = T.size
    c2=pixels_total_horizontal(T)
    for i2 in range(w2):
        if c2[w2-i2-1]>m:
            P=T.crop((0,0,w2-i2,h2))
            break       
    w3, h3 = P.size
    c3=pixels_total_vertical(P)
    for i3 in range(h3):
        if c3[i3]>n:
            Q=P.crop((0,i3-1,w3,h3))
            break
    w4, h4 = Q.size
    c4=pixels_total_vertical(Q)
    for i4 in range(h4):
        if c4[h4-i4-1]>n:
            R=Q.crop((0,0,w4,h4-i4))
            break
    return R

def conteo_pixels_blanco(imagen):
    cantidad=0
    ancho, alto = imagen.size
    pix = imagen.load()     
    for i in range(ancho):
        for j in range(alto):
            if pix[i,j]==255:
                cantidad=cantidad+1
    return cantidad

def seg_minimo_pixel(imagen):
    r=minimo_pixel(imagen)
    c=pixels_total_horizontal(imagen)
    smenor=200
    for i in range(len(c)):
        if(c[i]<smenor and c[i]!=0 and c[i]!=r):
            smenor=c[i]
    return smenor

def thinning():
    imagen = cv2.imread("a.jpg",0)   
    size = np.size(imagen)
    skel = np.zeros(imagen.shape,np.uint8)
    ret,imagen = cv2.threshold(imagen,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    while( not done):
        eroded = cv2.erode(imagen,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(imagen,temp)
        skel = cv2.bitwise_or(skel,temp)
        imagen = eroded.copy()
        zeros = size - cv2.countNonZero(imagen)
        if zeros==size:
            done = True
    cv2.imwrite("a.jpg" ,skel)

def segmentacion(imagen,separador,nsegmentos,lseg,mintotpix):
    his=pixels_total_horizontal(imagen)
    w, h = imagen.size
    letter=False
    foundletter=False
    u=0
    t=0
    p=0
    for i in range(w):
        if letter==True:
            if his[i]<=separador or i==w-1:
                if i== w-1: print (t)
                if t>lseg: 
                    n2=i
                    foundletter=True
                    print("e")
                else:
                    t=t+1
            else:
                t=t+1
        else:
            if his[i]>separador or i==0:
                letter=True
                n1=i
                t=1
        if foundletter==True:
            im = imagen.crop((n1, 0, n2, h))
            if conteo_pixels_blanco(im)>mintotpix:
                u=u+1
                if u==nsegmentos:
                    im = imagen.crop((n1, 0, w, h))
                    im.save(str(nsegmentos)+".jpg")
                    im.close()
                    break
                elif u<nsegmentos:
                    leer.borrarauxexp(str(u)+"jpg")
                    im.save(str(u)+".jpg")
                    im.close()
                    p=n1
            foundletter=False
            letter=False
    if u<nsegmentos:
        im1 = imagen.crop((p, 0, w, h))
        im1.save(str(u)+".jpg")
        im1.close()      
    return u


def segmentacion_thin(imagen1,imagen2,separador,nsegmentos,lseg):
    leer.borraraux2()
    his=pixels_total_horizontal(imagen2)
    w, h = imagen2.size
    letter=False
    foundletter=False
    u=0
    t=0
    p=0
    for i in range(w):
        if letter==True:
            if his[i]<=separador or i==w-1:
                if t>lseg: 
                    n2=i
                    foundletter=True
                else:
                    t=t+1
            else:
                t=t+1
        else:
            if his[i]>separador or i==0:
                letter=True
                n1=i
                t=1

        if foundletter==True:
            im = imagen1.crop((n1, 0, n2, h))
            if conteo_pixels_blanco(im)>9:
                u=u+1
                if  u==nsegmentos:
                    im1 = imagen1.crop((n1, 0, w, h))
                    im1.save(str(u)+".jpg")
                    im1.close()
                    break
                elif u<nsegmentos:
                    im.save(str(u)+".jpg")
                    p=n1
                    im.close()
            foundletter=False
            letter=False
    if u<nsegmentos:
        im1 = imagen1.crop((p, 0, w, h))
        im1.save(str(u)+".jpg")
        im1.close()
    print(u)
    return u

def quitar_mancha(imagen):
    ancho, alto = imagen.size
    pix = imagen.load() 
    output = Image.new("L", (ancho, alto))
    out_pix = output.load()
    for i in range(ancho):
        fin=1
        for j in range(alto):
            if pix[i,j]==0 and fin:
                out_pix[i,j]=255
            else:
                fin=0
                out_pix[i,j]=pix[i,j]
    return output
    
def quitar_linea(imagen,L):
    anchu, altu = imagen.size
    out = imagen.load()
    outps = Image.new("L", (anchu, altu))
    out_ps = outps.load()
    pix = L.load() 
    for n in range(anchu):
        for m in range(altu):            
            if(out[n, m]==0):
                if (pix[n, m] == 0):
                        out_ps[n, m]=255
                        if m != altu-1:
                            out_ps[n,m+1]=255
                        if m !=  0:
                            out_ps[n,m-1]=255
                else:
                    if out_ps[n, m]!=255:
                        out_ps[n, m]=out[n, m]
            else:
                if out_ps[n, m]!=255:
                    out_ps[n, m]=out[n, m]
    return outps


def segmentar(minpix,nseg,Lminseg,k,mintotpix):
    leer.borraraux()
    c=leer.total_arch("C:/Users/Antonio/Desktop/CAPTCHAS/MEF_IA/segmentada",k)
    print(c)
    if c<5:
        for i in range(c):     
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            m=segmentacion(im1,minpix,nseg,Lminseg,mintotpix)
            im1.close()
            print(m,n,c)
            if m>1  :            
                for r in range(c,i+1,-1):
                    print(r)
                    os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))
                    
                os.remove("segmentada/"+str(i+1)+"."+str(k))
                for s in range(m): 
                    os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
                break
    leer.borraraux()

def segmentarforzado(k):
    c=leer.total_arch("C:/Users/Antonio/Desktop/CAPTCHAS/MEF_IA/segmentada",k)
    print(c)
    Lmax=0
    p=0
    if c<5:
        for i in range(c):
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            ancho, alt=im1.size
            im1.close()
            if ancho>Lmax:
                Lmax=ancho
                p=i+1
        im1=Image.open("segmentada/"+str(p)+"."+str(k))
        his=pixels_total_horizontal(im1)
        minpix=100
        for i in range(int(round(Lmax/3.0,0))+1,int(2.0*round(Lmax/3.0,0))):
            if his[i]<minpix:
                minpix=his[i]
        print(minpix,Lmax,p,"sd")
        im1.close()
        im1=Image.open("segmentada/"+str(p)+"."+str(k))
        m=segmentacion(im1,minpix,2,round(Lmax/3),0)
        im1.close()
        print(m,n,c)
        if m==2  :            
            for r in range(c,p,-1):
                print(r)
                os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+1)+"."+str(k))
            os.remove("segmentada/"+str(p)+"."+str(k))
            for s in range(m): 
                os.rename(str(s+1)+".jpg", "segmentada/"+str(p+s)+"."+str(k))
    leer.borraraux()        

def segmentarthin(minpix,nseg,Lminseg,k):
    c=leer.total_arch("segmentada/",k)
    print(c)
    if c<5:
        for i in range(c):
            leer.borraraux()
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            im1.save("a.jpg")
            dilation(2)
            M=Image.open("a.jpg")
            N=binarizacion(M, 90)
            M.close()
            leer.borrarauxexp("a.jpg")
            N.save("a.jpg")
            thinning()
            dilation(2)
            N.close()
            P=Image.open("a.jpg")
            Q=binarizacion(P, 90)
            m=segmentacion_thin(im1,Q,minpix,nseg,Lminseg)
            P.close()
            Q.close()
            im1.close()
            if m>1:            
                for r in range(c,i+1,-1):
                    print(r)
                    os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))
                    
                os.remove("segmentada/"+str(i+1)+"."+str(k))
                for s in range(m): 
                     os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
                break 
    leer.borraraux2()

#################################################################################################################################################################
################################ CODIGO PRINCIPAL ###############################################################################################################
#################################################################################################################################################################
#Entrenamiento del modelo
try:
    npaClassifications = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
except:
    print ("error, unable to open classifications.txt, exiting program\n")
    os.system("pause")
    # end try

try:
    npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
except:
    print ("error, unable to open flattened_images.txt, exiting program\n")
    os.system("pause")


print(npaClassifications.shape,npaFlattenedImages.shape)

kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object
kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

print("modelo entrenado")

#SQLITE CONACION
conn = sqlite3.connect('SIAF.db')
c = conn.cursor()
"""
# Create table solo si no estan creadas previamente
c.execute('''CREATE TABLE EXPEDIENTE_ADMIN
             (Entidad INTEGER,  año text, expediente int, nom_entidad text, tipo_operacio text, nom_operacion text, tipo_mod_compra text, nom_mod_compra text, tipo_prc_selecc text, nom_prc_selecc)''')
c.execute('''CREATE TABLE DATOS_EXPEDIENTE
             (Entidad INTEGER,  año text, expediente int, num_registro int, ciclo char, fase char, sec int, corr int, doc INTEGER, numero text, fecha date, ff int, moneda text,  monto real, estado char, fecha_proceso datetime,  id_trx INTEGER )''')
"""
driver= webdriver.Chrome()
driver.get('http://apps2.mef.gob.pe/consulta-vfp-webapp/consultaExpediente.jspx')
total_consultas=6
for i in range(total_consultas):
    k=str(i)+".jpg"
    driver.save_screenshot('screenshot.png')
    screenshot=Image.open('screenshot.png')
    captcha= screenshot.crop((149,518,349,576))
    captcha.save("img/"+k)  
    leer.borraraux()
    I = Image.open("img/"+k)
    #convertir a gris
    G = I.convert("L")
    G.save("gris/"+k)
    #binarizar imagen para que se vea solo la linea
    LN=binarizacion(G, 40) 
    LN.save("linea/"+k)
    #binarizar imagen para quitar el color de fondo de la imagen
    w, h = G.size
    pix = G.load() 
    output = Image.new("L", (w, h))
    out_pix = output.load()
    for i in range(w):
        sum=0
        for a in range(h):
            sum=sum+pix[i,a]
        p=sum/h
        p=int(p)
        for j in range(h):
            if pix[i, j] >= p: out_pix[i, j] = 255
            else: out_pix[i, j] = 0 
    output.save("binarizada/"+k)
     #quitar mancha
    A=quitar_mancha(output)
    A.save("sinmancha/"+k)

    #quitar linea
    C=quitar_linea(A,LN)
    C.save("sinlinea/"+k)
    #invertir colores de la imagen
    out = ImageChops.invert(C)
    out.save("invertida/"+k)
    #corte
    Ct=corte(out,7,7)
    Ct.save("cortada/"+k)
    Ct.save("a.jpg")
    dilation(2)
    M=Image.open("a.jpg")
    N=binarizacion(M, 90)
    N.save("a.jpg")
    thinning()
    dilation(2)
    N.close()
    M.close()
    P=Image.open("a.jpg")
    Q=binarizacion(P, 90)
    n=segmentacion_thin(Ct,Q,0,5,30)
    P.close()    
    print(n)
    for i in range(n):
        if os.path.exists(str(i+1)+".jpg"):
            L=Image.open(str(i+1)+".jpg")
            L.save("segmentada/"+str(i+1)+"."+str(k))
            L.close()
    n=0
    m=0
    for i in range(5):
        if os.path.exists("segmentada/"+str(i+1)+"."+str(k)):
            R=Image.open("segmentada/"+str(i+1)+"."+str(k))
            w, h = R.size
            R.close()  
            if w>m:
                m=w
                c=i+1
            n=n+1
        else:
            break
    if n<5 and n>0:
        print(m,n,c)        
        for i in range(n):
            leer.borraraux()
            im1=Image.open("segmentada/"+str(i+1)+"."+str(k))
            m=segmentacion(im1,0,6-n,27,90)
            im1.close()
            print(m,n,c)
        if m>1:            
            for r in range(c,i+1,-1):
                print(r)
                os.rename("segmentada/"+str(r)+"."+str(k), "segmentada/"+str(r+m-1)+"."+str(k))
            os.remove("segmentada/"+str(i+1)+"."+str(k))
            for s in range(m): 
                os.rename(str(s+1)+".jpg", "segmentada/"+str(i+1+s)+"."+str(k))
    segmentar(0,6-n,23,k,80)
    segmentarthin(0,6-c,24,k)
    segmentar(1,6-c,23,k,85)
    segmentar(0,6-n,20,k,85)
    segmentarthin(0,6-c,20,k)
    segmentar(1,6-c,22,k,85)
    segmentar(2,6-c,25,k,85)
    segmentarthin(2,6-c,20,k)
    segmentar(2,6-c,20,k,70)
    segmentar(3,6-c,20,k,80)  
    segmentarthin(3,6-c,20,k)
    segmentarthin(4,6-c,20,k)  
    segmentar(3,6-c,20,k,70)
    segmentar(5,6-c,20,k,70)    
    segmentar(6,6-c,20,k,70)
    segmentarforzado(k)
    segmentarforzado(k)

    finalstr=''
        for n in leer.listdir_recurd([],"C:/Users/Antonio/Desktop/CAPTCHAS/MEF_IA/segmentada/","C:/Users/Antonio/Desktop/CAPTCHAS/MEF_IA/segmentada/",[]): 
            test=Image.open("segmentada/"+str(n))
            test.save("a.jpg")
            ancho,alto=test.size
            mitad_ancho=int(ancho/2.0)
            mitad_alto=int(alto/2.0)
            pix=test.load()
            im2=Image.new("L",(52,52))
            im2_pix = im2.load() 
            for i in range(26-mitad_ancho,26+mitad_ancho):
                for j in range(26-mitad_alto,26+mitad_alto):
                    if pix[i+mitad_ancho-26,j+mitad_alto-26]>180:
                        try:
                            im2_pix[i,j]=255
                        except:
                            pass
            im2.save("a.jpg")
            im2.close()
            imgTestNumbers = cv2.imread("a.jpg")
            testflt= imgTestNumbers.reshape(1,np.prod(8112))   
            testflt = np.float32(testflt)   
            retval, npaResults, neigh_resp, dists = kNearest.findNearest(testflt, k = 1)
            predicchar = str(chr(int(npaResults[0][0])))
            finalstr= finalstr + predicchar
            print(finalstr)

    captcha_entrada= driver.find_element_by_id("j_captcha")
    captcha_entrada.send_keys(finalstr)
    unidad_ejec= driver.find_element_by_id("secEjec")
    unidad_ejec.send_keys("300001")
    expediente= driver.find_element_by_id("expediente")
    exp=i+100
    expediente.send_keys(str(exp))
    buscar=driver.find_element_by_xpath("//*[@id='command']/input").click()
    time.sleep(3)

#leer data
    try:
        entidadnom = driver.find_element_by_id("secEjecNombre")


        año= driver.find_element_by_id("anoEje")
        dato_año= año.get_attribute("value")
        entidadid = driver.find_element_by_id("secEjec")
        id_entidad= entidadid.get_attribute("value")
        
        nom_entidad= entidadnom.get_attribute("value")
        expedid = driver.find_element_by_id("expediente")
        id_expediente= expedid.get_attribute("value")
        t_ope= driver.find_element_by_id("tipoOperacion")
        tipo_ope= t_ope.get_attribute("value")
        nom_ope= driver.find_element_by_id("tipoOperacionNombre")
        nombre_ope= nom_ope.get_attribute("value")
        t_modcom= driver.find_element_by_id("modalidadCompra")
        tipo_modo_compra= t_modcom.get_attribute("value")
        nom_modcom= driver.find_element_by_id("modalidadCompraNombre")
        nombre_modcom= nom_modcom.get_attribute("value")
        t_prc_sel= driver.find_element_by_id("tipoProceso")
        tipo_prc_sel= t_prc_sel.get_attribute("value")
        nom_prc_sel= driver.find_element_by_id("tipoProcesoNombre")
        nombre_prc_sel= nom_prc_sel.get_attribute("value")
        tablaexpedientes = driver.find_elements_by_tag_name("td")
        datostabla=[]

        for i in range(len(tablaexpedientes)//14):
            regexpediente = ()
            regexpediente += (dato_año,)
            regexpediente += (id_entidad,)
            regexpediente += (id_expediente,)
            regexpediente += (i+1,)
            regexpediente += (tablaexpedientes[i*14+0].text,)
            regexpediente += (tablaexpedientes[i*14+1].text,)
            regexpediente += (tablaexpedientes[i*14+2].text,)
            regexpediente += (tablaexpedientes[i*14+3].text,)
            regexpediente += (tablaexpedientes[i*14+4].text,)
            regexpediente += (tablaexpedientes[i*14+5].text,)
            regexpediente += (tablaexpedientes[i*14+6].text,)
            regexpediente += (tablaexpedientes[i*14+7].text,)
            regexpediente += (tablaexpedientes[i*14+8].text,)
            regexpediente += (tablaexpedientes[i*14+9].text,)
            regexpediente += (tablaexpedientes[i*14+10].text,)
            regexpediente += (tablaexpedientes[i*14+11].text,)
            regexpediente += (tablaexpedientes[i*14+12].text,)
            datostabla.append(regexpediente)    

        
        #guardar data 
        EXP_arreglo =  [( id_entidad, dato_año, id_expediente , nom_entidad, tipo_ope, nombre_ope,tipo_modo_compra , nombre_modcom , tipo_prc_sel, nombre_prc_sel)]
        c.executemany('INSERT INTO EXPEDIENTE_ADMIN VALUES (?,?,?,?,?,?,?,?,?,?)', EXP_arreglo)
        c.executemany('INSERT INTO DATOS_EXPEDIENTE VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datostabla)

        driver.back()
    except :
        print("Error al ingresar la data")
        driver.refresh()
        pass
      
    for f in listdir("segmentada/"):   
        try:   
            os.remove("segmentada/"+f) 
        except:
            pass

if (i == total_consultas):
    #Revision de tablas
    c.execute('SELECT * FROM EXPEDIENTE_ADMIN')
    print("Tabla EXPEDIENTE_ADMIN")
    print( c.fetchall())

    c.execute('SELECT * FROM DATOS_EXPEDIENTE')
    print(" Tabla DATOS_EXPEDIENTE ")
    print( c.fetchall())

