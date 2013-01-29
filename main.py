# -*- coding: utf-8 -*-

import xlwt
import lib.kin
import lib.dn
import lib.kzm


"""
m - коэфициент условия работы
k1, k2 - коэфициент надежности по материалу
kn - коэфициент надежности по назначению
np - коэфициент надежности по нагрузке (внутреннее давление)
sigmaB - граница крепкости материала
sigmaT - граница текучести
k1c - характеристика трещиностойксти - критический КИН

typeD - тип дефекта

l - (2l) длина дефекта
b - (2b) ширина дефекта
a - глубина дефекта

dn - толщина стенки
dvn - диаметр трубы
p - внетренние давление (максимальное рабочее давление)
"""


def importFile():

    f = open('import.txt', 'r')
    data = []
    fileD = f.read()
    lines = fileD.splitlines()
    for line in lines:
        data.append(line.split(';'))
    return data


def calc(defect, methS, typeDS, methK, typeDK):

    [nd, pd, m, k1, k2, kn, np, nt, sigmaB, sigmaT, k1c, kcv, l, a, b,
        dn, dvn, p, typeOfDefect] = defect

    non, oz = lib.dn.oz(nt, np, p, dvn, dn)
    sigmaR = lib.dn.dn(non, oz, np, dn, dvn, methS, typeDS, l, a)
    K = lib.kin.kin(non, oz, l, a, dn, dvn, p, sigmaT, methK, typeDK)

    dkzm = lib.kzm.dkzm(k1, kn, m)
    kzm, kd = lib.kzm.kzm(K, k1c, sigmaR, sigmaB, sigmaT, dkzm, methK)

    return [non, oz, sigmaR, K, dkzm, kzm, kd]


def exportExcel(data, result):

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Result')

    indexes = ['nd', 'pd', 'm', 'k1', 'k2', 'kn', 'np', 'nt',
               'sigmaB', 'sigmaT', 'k1c', 'kcv', 'l', 'a', 'b', 'dn', 'dvn', 'p',
               'typeOfDefect', 'non', 'oz', 'sigmaR', 'K', 'dkzm', 'kzm', 'kd']
    i = 0
    for name in indexes:
        ws.write(0, i, name)
        i = i + 1

    lx = len(result)
    ly = len(data[0]) + len(result[0])
    flagResult = len(data[0])
    for x in xrange(0, lx):
        for y in xrange(0, ly):
            if y < flagResult:
                try:
                    ws.write(x + 1, y, str(data[x][y]).decode('utf-8'))
                except:
                    ws.write(x + 1, y, str(data[x][y]).decode('utf-8'))
            else:
                try:
                    ws.write(x + 1, y, str(round(result[x][y - flagResult], 3)).decode('utf-8'))
                except:
                    ws.write(x + 1, y, str(result[x][y - flagResult]).decode('utf-8'))

    wb.save('result.xls')


if __name__ == '__main__':

    data = importFile()
    result = []

    for defect in data:
        for i in xrange(0, len(defect)):
            try:
                defect[i] = float(defect[i])
            except:
                #If kcv, then calc k1c
                if i == 10:
                    try:
                        defect[11] = float(defect[11])
                    except:
                        continue
                    defect[10] = float(lib.kzm.k1c(defect[11]))
                continue

        meth = 1
        typeD = 0.1

        try:
            result.append(calc(defect, meth, typeD, meth, typeD))
        except:
            err = 'error'
            result.append([err, err, err, err, err, err, err])

    exportExcel(data, result)
