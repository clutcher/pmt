# -*- coding: utf-8 -*-

import math


def oz(nt, np, p, dvn, dn, at=0.0000158, deltaT=-20, e=200000, myu=0.3):
    """nt, np - коэффициент надежности при нагрузке
    p - максимальное рабочее давление
    dvn - внутренний диаметр трубы
    dn - номинальная толщина стенки
    at - коэффициент линейного теплового розширения
    deltaT - температурный перепад между температурой монтажа и експлуатации
    e - модуль упругости
    myu - коэффициент поперечной деформации
    """
    non = np * p * dvn / (2. * dn)
    oz = (-1) * at * nt * deltaT * e + myu * non
    return non, oz


def dn(non, oz, np, t, dvn, method, typeD, l, a, c=0., b=0., i=1., st3=0., sx3=0.):
    """
    non - номинальное окружное напряжение
    oz - осевые усилия
    np - коэффициент надежности при нагрузке
    t - толщина стенки трубы
    dvn - внутренний диаметр трубы
    meth - метод решения
    l(b) - длина дефекта(l=2*l)
    a (phi) - глубина дефекта, угол дефекта
    с - доина дефекта вдоль трубы
    b - коэффициент для трубы с осевой сквозной трещиной
    i - коэффициент категории напряжений
    st3, sx3 - оболочковые изгибающие моменты
    """
    #method = math.trunc(meth)
    #typeD = meth - method

    R = dvn / 2
    l = l / 2

    if method == 1:

        tau = (t - a) / t
        lyam = l / math.sqrt(R * t)

        a1 = (1 + tau * tau + 4 * lyam * lyam * (1 - tau) * tau) / (1 + tau * tau + 4 * lyam * lyam * (1 - tau))
        a2 = 0.5 * tau * tau / (lyam * lyam) + tau

        if typeD == 0.1:
            alpha = min(a1, a2)
        elif typeD == 0.2:
            alpha = a1
        elif typeD == 0.3:
            cb = 0.85 + 0.45 * b - 1.3 * (b ** 4)
            alpha = cb / (math.sqrt(1 + 1.6 * lyam * lyam) - 1 + cb)
        else:
            print typeD
            return "Incorrect method"

        sigmaR = (non + (2. / 3) * st3 / i) / alpha
        sigmaXp = abs((non + (2. / 3) * sx3 / i) / alpha)
        sigmaXm = abs((non - (2. / 3) * sx3 / i) / alpha)
        sigmaXpT = abs(sigmaXp - non)
        sigmaXmT = abs(sigmaXm - non)

        dn = max(sigmaR, sigmaXp, sigmaXm, sigmaXpT, sigmaXmT)

    elif method == 2:

        f = oz * 2 / (2)
        #g = (oz-oz)/2

        phiFlag = 0
        phi = (math.pi * (f - a / 2) + a * l / (t * R)) / (2 - a)
        if (phi + math.pi / 2) >= (l / R):
            phi = (math.pi * f + (math.pi - l / R) * (1 - a) + (1 - a / t) * (1 - a) * l / R - (1 - a / t)(1 - a / 2) * math.pi) / (1 - a / t) * (2 - a)
            phiFlag = 1

        if typeD == 0.1:
            if phiFlag == 0:
                alpha = (2 - a) * math.cos(phi) - (a / t) * math.sin(l / R)
            else:
                alpha = (2 - a) * (1 - a / t) * math.cos(phi) + (1 - a) * (a / t) * math.sin(l / R)
        elif typeD == 0.2:
            if phiFlag == 0:
                alpha = (2 - a) * math.cos(phi) - (2 * a / t) * math.sin(l / R)
            else:
                alpha = (2 - a) * math.cos(phi) - (a / t) * math.sin(l / R)
        elif typeD == 0.3:
            phi = (math.pi * (f - a / 2) + l / R) / (2 - a)
            alpha = (2 - a) * math.cos(phi) - math.sin(l / R)
        else:
            return "Incorrect method"

        dn = (non + (2. / 3) * st3 / i) / alpha

    elif method == 3:

        dn1 = np * p * R / (t - a)
        dn2 = oz * t / (t - a)
        dn3 = abs(dn2 - dn1)

        dn = max(dn1, dn2, dn3)

    elif method == 4:
        lyaml = (9 / 16) * c * c / (R * t)
        lyamb = l * l / (R * t)

        a1 = math.sqrt((R / t) * (R / t) * (math.acos(1 - c / R) ** 4)) - (R / t) * math.acos(1 - c / R) * math.acos(1 - c / R)
        a2 = math.sqrt(lyamb ** 2 + 1) - lyamb

        A = max(a1, a2)

        alpha = (1 + 2 * lyaml * A * (1 - A)) / (1 + s * lyaml * (1 - A))

        sigmaR = (non + (2. / 3) * st3 / i) / alpha
        sigmaXp = abs((non + (2. / 3) * sx3 / i) / alpha)
        sigmaXm = abs((non - (2. / 3) * sx3 / i) / alpha)
        sigmaXpT = abs(sigmaXp - non)
        sigmaXmT = abs(sigmaXm - non)

        dn = max(sigmaR, sigmaXp, sigmaXm, sigmaXpT, sigmaXmT)

        if dn < 0:
            dn = dn + oz

    return dn