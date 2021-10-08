##Code written by: Russlan Jaafreh

import numpy as np
import pandas as pd
import os
import pymatgen.core as pg

##Initializing A,A_1, B and X as elements used in this work. Please refer to Fig. 6a in the paper

A = ["Li","Na","K","Rb","Cs"]
A_1 = ["Be","Mg","Ca","Sr","Ba"]
B = ["Ti","Zr","Hf","V","Nb","Ta","Cr","Mo","W","Mn","Tc","Re","Fe","Os","Ru","Co","Rh","Ir","Ni","Pt","Pd","Cu","Ag","Au","Zn","Cd","Hg","Al","Ga","In","Tl","Si","Ge","Ga","Sn","Pb","As","Sb","Bi","Se","Te"]
X = ["F","Cl","Br","I","O","S","P"]


##Read all 4 prototype structures and replace A,B,X by elements from A,bA_1, B, and X

os.chdir(r".\Supplementary files\ML Code\prototype_Poscar")
with open('protoA3B2X9.txt') as f:  
    lines = f.read()

#this is to create the properties file header that will be used in Magpie later

for_text = []
initial = "filename delta_e structure"
for_text.append(initial)

##Make a directory A3B2X9 in prototypes to create poscar files from the elemtens and prototype structure A3B2X9

os.chdir(r".\prototypes\A3B2X9")

counter = 1
for i in A:
    for j in B:
        for k in X:
            
            for_output = lines.replace("A",i)
            for_output_2 = for_output.replace("B",j)
            for_output_3 = for_output_2.replace("X",k)
            for_text.append(f"{counter}-{i}3{j}2{k}9 none {counter}")
            with open(f"{counter}-{i}3{j}2{k}9", "w") as text_file:
                text_file.write(for_output_3)
            counter = counter + 1

##This is for the properties file again
textfile = open("properties.txt", "w")
for element in for_text:
    textfile.write(element + "\n")
textfile.close()

##The outcome should be: a properties.txt file and almost a thousand poscar file of combination replaced in the prototype file that is ready to be used in Magpie for feature generation