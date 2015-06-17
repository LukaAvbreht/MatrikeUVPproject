__author__ = 'Luka'


from fractions import Fraction
import math
import copy
from tkinter import *
from tkinter.filedialog import *



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
        if nasa[0][0]==0:
            return Matrika([[0,0,0],[0,0,0],[0,0,0]])     #ker je to ubistvu sam za determinanto in ce se neda nardit zgorinenicelne je determinanta 0 == ni obrnljiva
        prva = nasa.cifre[0]
        res = []
        res.append(prva)
        for vrstica in nasa.cifre[1:]:
            resvrs = []
            for vodilni,clen in zip(prva,vrstica):
                k = -Fraction(vrstica[0],prva[0])
                clen = k*vodilni + clen
                resvrs.append(clen)        #morm dat v floor d mam pol lep fraction
            res.append(resvrs)
        return Matrika(res)

    def nenicelna(self,i,j):            # to ne dela nc pametnega se
        if i>len(self.cifre):
            return False
        if j>len(self.cifre[0]):
            return False
        res = []
        kont = -1
        i = i-1
        j = j-1
        res = []
        if self.cifre[i][j] != 0:
            return Matrika(self.cifre)
        for ind,line in enumerate(self.cifre):
            if ind<i:
                res.append(line)
            else:
                break
        for ind,line in enumerate(self.cifre[i:]):
            if line[j]!=0:
                res.append(line)
                kont = ind
        if kont==-1:
            print("neda se")
            return False
        for ind,line in enumerate(self.cifre[:i]):
            if ind!=kont:
                res.append(line)
        res.append(self.cifre[kont])
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
        return Matrika(res)

class Tkmatrika:
    def __init__(self, master):
        self.master = master
        self.master.minsize(width=600, height=350)
       # self.datoteka = StringVar(master, value = None)
        matrika = StringVar(master,value=None)
#        matrika.grid(row=1,column=0,rowspan=5,columnspan=5)

        gumb_izberi = Button(master, text="Izberi datoteko", command= self.odpri)
        gumb_izberi.grid(row=0,column=0,sticky=N+S+E+W)

        gumb_det = Button(master, text="Determinanta", command= self.determinanta)
        gumb_det.grid(row=1,column=0,sticky=N+S+E+W)

        gumb_inverz = Button(master, text="Inverz", command= self.inverz)
        gumb_inverz.grid(row=2,column=0,sticky=N+S+E+W)

        gumb_kvadrat = Button(master, text="Kvadratna", command= self.kvadrat)
        gumb_kvadrat.grid(row=3,column=0,sticky=N+S+E+W)



    def odpri(self):
        fileName = askopenfilename(filetypes = ( ("text files", "*.txt") , ("all files", "*.*") ))
        with open(fileName) as f:
            res = []
            for line in f:
                line = line.strip("\n")
                print(line)
                res.append(line)
            aktivna = Matrika(res)
            matrika.set(aktivna)

    def izpisi(self):               #to naj bi naredilo iz matrike str in ga postavilo v tkinter (treba je se dodati obliko
        res = "Vnesli ste naslednjo matriko: \n"
        for line in aktivna.cifre:
            tren = ""
            for j in line:
                if type(j)==fractions.Fraction:
                    tren+=str(j.numerator)+"/"+str(a.denominator)
                else:
                    tren+=str(j)
            res+=tren+"\n"
        self.matrika.set(res)

    def determinanta(self):
        self.determinanta = aktivna.determinanta()

    def inverz(self):
        self.inverz = aktivna.inverz()

    def kvadrat(self):
        self.kvadrat = aktivna.ali_kvadratna()
        print("ni se narjen")

    """with open(fileName,"r") as vhod:    #Ta del bo iz datoteke narediu matriko s katero znamo racunat
        sez = []
        for line in vhod:
            sez.append(line)
        aktivna = Matrika(sez)"""







root = Tk()
#fileName = tkFileDialog.askopenfilename( filetypes = ( ("text files", "*.txt") , ("all files", "*.*") ))
root.wm_title("Matrika")
okno = Tkmatrika(root)
root.mainloop()
