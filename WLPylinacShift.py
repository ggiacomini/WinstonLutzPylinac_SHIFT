
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 18:45:01 2021

Improved Pylinac Winston Lutz test based on EPID images.

The code performs analysis at ideal isocenter point, virtually applying the necessary shift.

*Requirements: Install Pylinac 3.0 (https://pylinac.readthedocs.io/en/release-3.0/installation.html)

@author: ggiacomini
"""

from pylinac import WinstonLutz
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#### open folder
root = tk.Tk()
root.withdraw()
folder = filedialog.askdirectory()
folder=folder.replace("/","\\",-1)
os.chdir(folder) #define diretorio atual
os.getcwd()


#my_directory = "C:\\Users\\ggiacomini\\Desktop\\Python\\winstonlutz28621"
my_directory=folder

wl = WinstonLutz(my_directory, use_filenames=True)


list = os.listdir(my_directory) # dir is your directory path
number_files = 0


for count in range(len(list)):
    if list[count][-4:] == ".dcm":
        number_files = number_files+1

# plot an individual image
#wl.images[0].plot()
# save a figure of the image plots
#wl.save_plots('wltest.png')

wl.publish_pdf('mywl.pdf')

############
# Shift a ser aplicado considerando Gantry e Mesa

latc=wl.bb_shift_vector.x
longc=wl.bb_shift_vector.y
vertc=wl.bb_shift_vector.z

# Shift a ser aplicado considerando somente Gantry 

latcg= 0.59    # RIGHT + / LEFT -
longcg=  -0.47   # IN + / OUT -
vertcg= 0.15 # UP + / DOWN -



wl.bb_shift_instructions()

#Decomposicao vetores

imagens=wl.images
result_vector = (np.zeros((number_files, 6) ))

for x in range(number_files):
    #wl.images[x].plot()
    image=wl.images[x]  
    gantry=image.gantry_angle
    col=image.collimator_angle
    couch=image.couch_angle
    a=round(image.cax2bb_vector.x,2)
    b=round(image.cax2bb_vector.y,2)
    result_vector[x,0]=gantry
    result_vector[x,1]=col
    result_vector[x,2]=couch 
    result_vector[x,3]=a
    result_vector[x,4]=b
    result_vector[x,5]=round(image.cax2bb_distance,2)
    
    
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)



# Apos Correcao Gantry e Mesa
result_vectorc = (np.zeros((number_files, 6) ))

for x in range(number_files):
    #wl.images[x].plot()
    image=wl.images[x]      
    gantry=image.gantry_angle
    col=image.collimator_angle
    couch=image.couch_angle
    if couch == 0:
        if gantry==0:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorc[x,0]=gantry
            result_vectorc[x,1]=col
            result_vectorc[x,2]=couch 
            result_vectorc[x,3]=a+latc
            result_vectorc[x,4]=b+longc
            result_vectorc[x,5]=((a+latc)**2+(b+longc)**2)**0.5
        if gantry==180:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorc[x,0]=gantry
            result_vectorc[x,1]=col
            result_vectorc[x,2]=couch 
            result_vectorc[x,3]=a-latc
            result_vectorc[x,4]=b+longc
            result_vectorc[x,5]=((a-latc)**2+(b+longc)**2)**0.5
        if gantry==90:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorc[x,0]=gantry
            result_vectorc[x,1]=col
            result_vectorc[x,2]=couch 
            result_vectorc[x,3]=a-vertc
            result_vectorc[x,4]=b+longc
            result_vectorc[x,5]=((a-vertc)**2+(b+longc)**2)**0.5
        if gantry==270:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorc[x,0]=gantry
            result_vectorc[x,1]=col
            result_vectorc[x,2]=couch 
            result_vectorc[x,3]=a+vertc
            result_vectorc[x,4]=b+longc
            result_vectorc[x,5]=((a+vertc)**2+(b+vertc)**2)**0.5
    if couch==270:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorc[x,0]=gantry
        result_vectorc[x,1]=col
        result_vectorc[x,2]=couch 
        result_vectorc[x,3]=a+longc
        result_vectorc[x,4]=b-latc
        result_vectorc[x,5]=((a+longc)**2+(b-latc)**2)**0.5
    if couch==90:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorc[x,0]=gantry
        result_vectorc[x,1]=col
        result_vectorc[x,2]=couch 
        result_vectorc[x,3]=a-longc
        result_vectorc[x,4]=b+latc
        result_vectorc[x,5]=((a-longc)**2+(b+latc)**2)**0.5
    if couch==315:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorc[x,0]=gantry
        result_vectorc[x,1]=col
        result_vectorc[x,2]=couch 
        result_vectorc[x,3]=a+((2**.5)/2)*(longc+latc)
        result_vectorc[x,4]=b+((2**.5)/2)*(longc-latc)
        result_vectorc[x,5]=((result_vectorc[x,3])**2+(result_vectorc[x,4])**2)**0.5        
    if couch==45:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorc[x,0]=gantry
        result_vectorc[x,1]=col
        result_vectorc[x,2]=couch 
        result_vectorc[x,3]=a+((2**.5)/2)*(-longc+latc)
        result_vectorc[x,4]=b+((2**.5)/2)*(longc+latc)
        result_vectorc[x,5]=((result_vectorc[x,3])**2+(result_vectorc[x,4])**2)**0.5        
            
     
            
# Apos Correcao somente Gantry 
result_vectorcg = (np.zeros((number_files, 6) ))

for x in range(number_files):
    #wl.images[x].plot()
    image=wl.images[x]      
    gantry=image.gantry_angle
    col=image.collimator_angle
    couch=image.couch_angle
    if couch == 0:
        if gantry==0:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorcg[x,0]=gantry
            result_vectorcg[x,1]=col
            result_vectorcg[x,2]=couch 
            result_vectorcg[x,3]=a+latcg
            result_vectorcg[x,4]=b+longcg
            result_vectorcg[x,5]=((a+latcg)**2+(b+longcg)**2)**0.5
        if gantry==180:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorcg[x,0]=gantry
            result_vectorcg[x,1]=col
            result_vectorcg[x,2]=couch 
            result_vectorcg[x,3]=a-latcg
            result_vectorcg[x,4]=b+longcg
            result_vectorcg[x,5]=((a-latcg)**2+(b+longcg)**2)**0.5
        if gantry==90:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorcg[x,0]=gantry
            result_vectorcg[x,1]=col
            result_vectorcg[x,2]=couch 
            result_vectorcg[x,3]=a-vertcg
            result_vectorcg[x,4]=b+longcg
            result_vectorcg[x,5]=((a-vertcg)**2+(b+longcg)**2)**0.5
        if gantry==270:
            a=round(image.cax2bb_vector.x,2)
            b=round(image.cax2bb_vector.y,2)
            result_vectorcg[x,0]=gantry
            result_vectorcg[x,1]=col
            result_vectorcg[x,2]=couch 
            result_vectorcg[x,3]=a+vertcg
            result_vectorcg[x,4]=b+longcg
            result_vectorcg[x,5]=((a+vertcg)**2+(b+longcg)**2)**0.5
    if couch==270:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorcg[x,0]=gantry
        result_vectorcg[x,1]=col
        result_vectorcg[x,2]=couch 
        result_vectorcg[x,3]=a+longcg
        result_vectorcg[x,4]=b-latcg
        result_vectorcg[x,5]=((a+longcg)**2+(b-latcg)**2)**0.5
    if couch==90:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorcg[x,0]=gantry
        result_vectorcg[x,1]=col
        result_vectorcg[x,2]=couch 
        result_vectorcg[x,3]=a-longcg
        result_vectorcg[x,4]=b+latcg
        result_vectorcg[x,5]=((a-longcg)**2+(b+latcg)**2)**0.5
    if couch==315:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorcg[x,0]=gantry
        result_vectorcg[x,1]=col
        result_vectorcg[x,2]=couch 
        result_vectorcg[x,3]=a+((2**.5)/2)*(longcg+latcg)
        result_vectorcg[x,4]=b+((2**.5)/2)*(longcg-latcg)
        result_vectorcg[x,5]=((result_vectorcg[x,3])**2+(result_vectorcg[x,4])**2)**0.5        
    if couch==45:
        a=round(image.cax2bb_vector.x,2)
        b=round(image.cax2bb_vector.y,2)
        result_vectorcg[x,0]=gantry
        result_vectorcg[x,1]=col
        result_vectorcg[x,2]=couch 
        result_vectorcg[x,3]=a+((2**.5)/2)*(-longcg+latcg)
        result_vectorcg[x,4]=b+((2**.5)/2)*(longcg+latcg)
        result_vectorcg[x,5]=((result_vectorcg[x,3])**2+(result_vectorcg[x,4])**2)**0.5        
            
            
  
print()
print('Winston Lutz')
print()
print("  GANTRY   COL   COUCH     X     Y     Vetor" )
print(result_vector)
              

print()
print('Winston Lutz corrected by Gantry+Couch')
print()
print("  GANTRY   COL   COUCH     X     Y     Vetor" )
print(result_vectorc)
    

print()
print('Winston Lutz corrected by Gantry')
print()
print("  GANTRY   COL   COUCH     X     Y     Vetor" )
print(result_vectorcg)
    


##save results in pdf

#df = pd.DataFrame(result_vector), columns = (" GANTRY","COL","COUCH","X","Y","Vetor")

#fig, ax =plt.subplots(figsize=(10,6))
#ax.axis('tight')
#ax.axis('off')
#the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')

#https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
#pp = PdfPages("foo.pdf")
#pp.savefig(fig, bbox_inches='tight')
#pp.close()
