__author__ = 'Luka'


from fractions import Fraction
import math
import copy
from tkinter import *
from tkinter.filedialog import *
import os


class Matrika:
    def __init__(self , cifre):
        dol = len(cifre[0])
        for j in cifre:
            if len(j)!=dol:
                Print("nc ne bo")
                break
        self.cifre = cifre


    def __eq__(self, other):
        if self.cifre == other.cifre:
            return True
        else:
            return False

    def ali_kvadratna(self):
        if len(self.cifre)==len(self.cifre[0]):
            return  True
        else:
            return False

    def determinanta(self):
        if len(self.cifre)==2:
            return self.cifre[0][0]*self.cifre[1][1] - self.cifre[0][1]*self.cifre[1][0]
        else:
            nasa = self.nula_pod_prvo()
            clen = nasa.cifre[0][0]
            poddet = nasa.podmatrika(1,1)
            return clen * poddet.determinanta()

    def podmatrika(self,i,j):
    #i,j ta poddeterminanta (i-ta vrstica j-ti stolpec)
        if i>len(self.cifre) or j>len(self.cifre):
            return False
        nove_cifre = copy.deepcopy(self.cifre)
        for vrstica in nove_cifre:
            del(vrstica[j-1])
        del(nove_cifre[i-1])
        return Matrika(nove_cifre)

    def zgori_nenicelna(self):
        res = []
        if self.cifre[0][0] != 0:
            return Matrika(self.cifre)
        for i,vrstica in enumerate(self.cifre):
            if vrstica[0] != 0:
                res.append(vrstica)
                del(self.cifre[i])
                uspel = True
        for j in self.cifre:
            res.append(j)
        return Matrika(res)

    def nula_pod_prvo(self):
        nasa = self.zgori_nenicelna()
#     if nasa[0][0]==0:
#            return Matrika([[0,0,0],[0,0,0],[0,0,0]])     #ker je to ubistvu sam za determinanto in ce se neda nardit zgorinenicelne je determinanta 0 == ni obrnljiva
        prva = nasa.cifre[0]
        res = []
        res.append(prva)
        for vrstica in nasa.cifre[1:]:
            resvrs = []
            for vodilni,clen in zip(prva,vrstica):
                print(vrstica[0],prva[0])                   # treba zbrisat
                k = -Fraction(vrstica[0],prva[0])
                clen = k*vodilni + clen
                resvrs.append(clen)        #morm dat v floor d mam pol lep fraction
            res.append(resvrs)
        return Matrika(res)

    def transponirana(self):
        if self.ali_kvadratna()==False:
            print("neda se")
            return False
        else:
            res = []
            for j in  range(len(self.cifre)):
                tem = []
                for i in range(len(self.cifre)):
                    tem.append(self.cifre[i][j])
                res.append(tem)
        return Matrika(res)

    def inverz(self):
        if self.determinanta()==0:
            print("neda se")
            return False
        else:
            res = []
            a = Fraction(1,self.determinanta())
            for j in range(len(self.cifre)):
                temp = []
                for i in range(len(self.cifre)):
                    trenutna = self.podmatrika(i+1,j+1)
                    det = trenutna.determinanta()
                    temp.append(det*a)
                res.append(temp)
            return Matrika(res)

    def sled(self):
        res = 0
        for j in range(len(self.cifre)):
            res += self.cifre[j][j]
        return res

class Tkmatrika:
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=600, height=350)
        self.imedat = StringVar(master, value=None)
        self.vhodmatrika = StringVar(master,value=None)
        self.izhodmatrika = StringVar(master,value=None)
        self.detispis = StringVar(master,value=None)
        self.sledispis = StringVar(master,value=None)
        self.errorfild = StringVar(master,value=None)
        self.aktivna = Matrika([[1,2],[3,4]])
#        matrika.grid(row=1,column=0,rowspan=5,columnspan=5)

        self.DEFCON1 = 0 #stanje ce je ze ispisana matrika
        self.DEFCON2 = 0 #stanje za inverz
        self.DEFCON3 = 0 #stanje za determinanto
        self.DEFCON4 = 0 #stanje za sled

        gumb_izberi = Button(master, text="Izberi datoteko", command= self.odpri,height=2)
        gumb_izberi.grid(row=0,column=0,sticky=N+S+E+W)

        gumb_det = Button(master, text="Determinanta", command= self.determinanta,height=2)
        gumb_det.grid(row=4,column=0,sticky=N+S+E+W)

        gumb_sled = Button(master, text="Sled", command= self.sled,height=2)
        gumb_sled.grid(row=5,column=0,sticky=N+S+E+W)

        gumb_inverz = Button(master, text="Inverz", command= self.inverz,height=2)
        gumb_inverz.grid(row=7,column=0,sticky=N+S+E+W)

    #    gumb_kvadrat = Button(master, text="Kvadratna", command= self.kvadrat)
    #    gumb_kvadrat.grid(row=7,column=0,sticky=N+S+E+W)

        gumb_trans = Button(master, text="Transponirano", command= self.trans,height=2)
        gumb_trans.grid(row=6,column=0,sticky=N+S+E+W)

        gumb_izpisi = Button(master, text="Ispisi", command= self.izpisi,height=2)
        gumb_izpisi.grid(row=3,column=0,sticky=N+S+E+W)

        text_imedat = Label(master,textvariable= self.imedat,height=2)
        text_imedat.grid(row=2,column=0,sticky=N+S+E+W)

        text_imedat = Label(master,text = "Ime datoteke:",height=2)
        text_imedat.grid(row=1,column=0,sticky=N+S+E+W)

        text_vhodmatrika = Label(master,textvariable= self.vhodmatrika,height=2)
        text_vhodmatrika.grid(row=0,column=2,columnspan=4,rowspan=4,sticky=N+S+E+W)

        text_izhodmatrika = Label(master,textvariable= self.izhodmatrika,height=2)
        text_izhodmatrika.grid(row=4,column=2,columnspan=4,rowspan=4,sticky=N+S+E+W)

        text_naddet = Label(master,text = "Determinanta:",height=2)
        text_naddet.grid(row=3,column=1,sticky=N+S+E+W)

        text_det = Label(master,textvariable= self.detispis,height=2)
        text_det.grid(row=4,column=1,sticky=N+S+E+W)

        text_nadsled = Label(master,text = "Sled:",height=2)
        text_nadsled.grid(row=5,column=1,sticky=N+S+E+W)

        text_sled = Label(master,textvariable= self.sledispis,height=2)
        text_sled.grid(row=6,column=1,sticky=N+S+E+W)

        text_sled = Label(master,textvariable= self.errorfild,height=2)
        text_sled.grid(row=0,column=1,rowspan=2,sticky=N+S+E+W)

    def odpri(self):
        fileName = askopenfilename(filetypes = ( ("text files", "*.txt") , ("all files", "*.*") ))
        ind = 0
        for i,j in enumerate(str(fileName)):
            if j=="/":
                ind = i
        datoteka = str(fileName)[ind+1:]
        self.imedat.set(datoteka)
        file = open(fileName, "r")
        res = []
        for line in file:
            tre = []
            line = line.strip("\n")
            line = line.strip("[")
            line = line.strip("]")
            line = line.split(",")
            for i in line:
                tre.append(int(i))
            print(line)                 #treba zbrisat
            res.append(tre)
        print(res)
        self.aktivna = Matrika(res)
        if self.aktivna.ali_kvadratna()==Fasle:
            self.errorfild.set("Vnesena matrika ni kvadratna \nIzberite drugo datoteko")



    def izpisi(self): #to naj bi naredilo iz matrike str in ga postavilo v tkinter (treba je se dodati obliko
        if self.DEFCON1 == 0:
            res = "Vnesli ste naslednjo matriko: \n"
            for line in self.aktivna.cifre:
                tren = ""
                for j in line:
                    try:
                        if j.denominator==1:
                            tren+=str(j.numerator)+"   "
                        else:
                            tren+=str(j.numerator)+"/"+str(j.denominator)+"   "
                    except:
                        tren+=str(j)+"   "
                res+=tren+"\n"
            self.vhodmatrika.set(res)
            self.DEFCON1 = 1
        else:
            self.vhodmatrika.set("")
            self.DEFCON1 = 0

    def determinanta(self):
        if self.DEFCON3 == 0:
            det = self.aktivna.determinanta()
            try:
                if det.denominator==1:
                    res = str(det.numerator)
                else:
                    res = str(det.numerator)+"/"+str(det.denominator)
            except:
                res = str(round(det,4))
            self.detispis.set(res)
            self.DEFCON3=1
        else:
            self.detispis.set("")
            self.DEFCON3=0

    def inverz(self):
        if self.DEFCON2 != 1:
            inverz = self.aktivna.inverz()
            res = "Inverz matrike je naslednja matrika: \n"
            for line in inverz.cifre:
                tren = ""
                for j in line:
                    try:
                        if j.denominator==1:
                            tren+=str(j.numerator)+"   "
                        else:
                            tren+=str(j.numerator)+"/"+str(j.denominator)+"   "
                    except:
                        tren+=str(j)+"   "
                res+=tren+"\n"
            self.izhodmatrika.set(res)
            self.DEFCON2=1
        elif self.DEFCON2 == 1:
            self.izhodmatrika.set("")
            self.DEFCON2 = 0

    def trans(self):
        if self.DEFCON2 != 2:
            trans = self.aktivna.transponirana()
            res = "Naslednja matrika transponirano: \n"
            for line in trans.cifre:
                tren = ""
                for j in line:
                    try:
                        if j.denominator==1:
                            tren+=str(j.numerator)+"   "
                        else:
                            tren+=str(j.numerator)+"/"+str(j.denominator)+"   "
                    except:
                        tren+=str(j)+"   "
                res+=tren+"\n"
            self.izhodmatrika.set(res)
            self.DEFCON2=2
        elif self.DEFCON2 == 2:
            self.izhodmatrika.set("")
            self.DEFCON2 = 0

    def sled(self):
        if self.DEFCON4 == 0:
            sled = self.aktivna.sled()
            try:
                if sled.denominator==1:
                    res = str(sled.numerator)
                else:
                    res = str(sled.numerator)+"/"+str(sled.denominator)
            except:
                res = str(round(sled,4))
            self.sledispis.set(res)
            self.DEFCON4 = 1
        else:
            self.DEFCON4 = 0
            self.sledispis.set("")



root = Tk()
root.wm_title("Matrika")
okno = Tkmatrika(root)
root.mainloop()
