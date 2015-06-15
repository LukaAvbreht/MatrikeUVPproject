__author__ = 'Luka'


from fractions import Fraction
import math
import copy
from tkinter import *


class Matrika:
    def __init__(self , cifre):
        dol = len(cifre[0])
        for j in cifre:
            if len(j)!=dol:
                return False
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
        if self.ali_kvadratna()==False:
            return False
        else:
            if len(self.cifre)==2:
                return self.cifre[0][0]*self.cifre[1][1] - self.cifre[0][1]*self.cifre[1][0]
            else:
                if self.nula_pod_prvo()==False:
                    return 0
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
        uspel = False
        if self.cifre[0][0] != 0:
            return Matrika(self.cifre)
        for i,vrstica in enumerate(self.cifre):
            if vrstica[0] != 0:
                res.append(vrstica)
                del(self.cifre[i])
                uspel = True
        for j in self.cifre:
            res.append(j)
        if uspel:
            return Matrika(res)
        else:
            print("Neda se")
            return False

    def nula_pod_prvo(self):
        if self.zgori_nenicelna()==False:
            Print("Neda se")
            return False
        nasa = self.zgori_nenicelna()
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


class Tkmatrika:
    def __init__(self, master):
        pass