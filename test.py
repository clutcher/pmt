# -*- coding: utf-8 -*-

import lib.kin as kin
import lib.dn as dn
import lib.kzm as kzm

if __name__ == '__main__':
    #print "Primer 1"
    #non, oz = dn.oz(1, 1.1, 4.1, 0.9978, 0.0111)
    #print non, oz
    #a = dn.aotd(non, oz, 0.151, 0.002553, 0.0111, 0.9978, 5)
    #print a
    #sigmaR = dn.dn(a, non, oz, 1., 0, 0)
    #print "SigmaR =", sigmaR

    #print "\nPrimer 2"
    #non, oz = dn.oz(1., 1.1, 4.1, 0.9978, 0.0116)
    #a = dn.aotd(0.034, 0.00464, 0.0116, 0.9978, 1)
    #sigmaR = dn.dn(a, non, oz, 1., 0, 0)
    #print "SigmaR =", sigmaR
    #K = kin.kin(non, oz, 0.034, 0.00464, 0.0116, 0.9978, 4.1, 1)
    #print "KIN=", K
    #dkzm = kzm.dkzm(1.47, 1., 0.9)
    #kzm1 = kzm.kzm(K, 62., sigmaR, 510., 363., dkzm)
    #print "KZM=", kzm1
    #print "DKZM=", dkzm


    print "\nPrimer 4"
    non, oz = dn.oz(1, 1.1, 4.1, 0.9978, 0.0089)
    #a = dn.aotd(0.03, 0.002, 0.0089, 0.9978, 1)
    #sigmaR = dn.dn(a, non, oz, 1., 0, 0)
    #print "Etap 1:"
    #print "SigmaR =", sigmaR
    K = kin.kinzva(non, oz, 0.03, 0.002, 0.0089, 0.9978, 4.1, 363, 1.1)
    print "K=", K
