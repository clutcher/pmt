# -*- coding: utf-8 -*-

import math


def kin(non, oz, l, a, t, dvn, p, sigmaT, method, typeD):
    """non - номинальное окружное напряжение
    oz - осевые усилия
    l - длина дефекта(l=2*l)
    a (phi) - глубина дефекта, угол дефекта
    t - толщина стенки трубы
    dvn - внутренний диаметр трубы
    p - максимальное рабочее давление
    meth - метод решения"""

    def df(a, R, t, myu, typeF='a'):
        """a (phi) - глубина дефекта, угол дефекта
        R - средний радиус трубы
        t - толщина стенки трубы
        myu - коэффициент поперечной деформации
        typeF - a  -- поиск Ya; -c -- поиск Yc"""

        r1 = a * a * (0.628 - 1.45 * a + 2.49 * a * a - 2.3 * a * a * a + 0.483 * a * a * a * a) / ((1 - a) * (1 - a))
        r2 = a * a * (0.627 - 2.01 * a + 3.68 * a * a - 3.57 * a * a * a + 1.35 * a * a * a * a) / ((1 - a) * (1 - a))
        y1 = 0.265 * ((1 - a) ** 4) + (0.857 + 0.265 * a) / ((1 - a) ** 1.5)
        if a <= 0.001:
            y2 = 1.22
        else:
            y2 = math.sqrt(2 * math.tan(math.pi * a / 2) / (math.pi * a)) * (0.923 + 1.99 * ((1 - math.sin(math.pi * a / 2)) ** 4)) / (math.cos(math.pi * a / 2))

        if typeF == 'a':
            return y1 * math.sqrt(math.pi * a) * (1 - r1 * y2 / (y1 * (R / (9 * t) + r2)))
        else:
            return y1 * math.sqrt(math.pi * a) * (1 - r1 * y2 / (y1 * (math.sqrt(R / t) / (9 * math.pi * (1 - myu * myu)) ** 0.25)))

    def parametr(l, a, t, R, typeP="o"):
        """l - длина дефекта(l=2*l)
        a (phi) - глубина дефекта, угол дефекта
        t - толщина стенки трубы
        R - средний радиус трубы
        typeP - o --для осевых дефектов; -k --для кольцевых дефектов
        """

        d = min(a, l)
        myu = 2 * l / t

        if a > l:
            ksi = math.sqrt(1 / a)
            q = 1 + 1.464 * ((a / l) ** 1.65)
        else:
            ksi = 1.
            q = 1 + 1.464 * ((a / l) ** 1.65)

        if typeP == 'o':
            F = 1.12 + 0.053 * myu + 0.0055 * myu * myu + (1 + 0.02 * myu + 0.0191 * myu * myu) * (20 - R / t) * (20 - R / t) / 1400
        else:
            F = 1 + (0.02 + 0.0103 * myu + 0.00617 * myu * myu + 0.0035 * (1 + 0.7 * myu) * ((R / t - 5) ** 0.7)) * q * q

        return myu, ksi, q, F, d

    R = dvn / 2
    l = l / 2

    #typeD, method = math.modf(meth)

    if method == 1:
        myu, ksi, q, F, d = parametr(l, a, t, R)

        if typeD == 0.1:
            k1 = non * math.sqrt(math.pi * d / q) * F * ksi
            k2 = non * df(a / t, R, t, myu)

            k = min(k1, k2)

        elif typeD == 0.2:
            k1 = (non + p) * math.sqrt(math.pi * d / q) * F * ksi
            k2 = (non + p) * df(a / t, R, t, myu)

            k = min(k1, k2)

    elif method == 2:
        d = min(a, l)
        a1 = min(a, l)
        l1 = max(a, l)
        q = 1 + 1.464 * ((a1 / l1) ** 1.65)

        eps = a1 / l1
        nyu = 2 * a1 * l1 / t

        F = 1 + nyu * (0.1786 + 0.039 * eps - 0.8255 * eps * eps + 0.8897 * eps * eps * eps) +\
            nyu * nyu * (-0.6485 - 0.3101 * eps + 3.3302 * eps * eps - 3.1083 * eps * eps * eps) +\
            nyu * nyu * nyu * (1.9715 - 2.4531 * eps + 0.0386 * eps * eps + 1.3748 * eps * eps * eps)

        k = non * math.sqrt(math.pi * d / q) * F

    elif method == 3:
        lyam = l / math.sqrt(R * t)
        F = math.sqrt(1 + 0.52 * lyam + 1.29 * lyam * lyam + 0.07 * lyam * lyam * lyam)

        k = (non + p) * math.sqrt(math.pi * l * F)

    elif method == 4:
        myu, ksi, q, F, d = parametr(l, a, t, R, typeP='k')
        if typeD == 0.1:
            k1 = oz * math.sqrt(math.pi * d / q) * F * ksi
            k2 = oz * df(a / t, R, t, myu, typeF='c')

            k = min(k1, k2)

        elif typeD == 0.2:
            k1 = (oz + p) * math.sqrt(math.pi * d / q) * F * ksi
            k2 = (oz + p) * df(a / t, R, t, myu)

            k = min(k1, k2)

    elif method == 5:
        d = min(a, l)
        a1 = min(a, l)
        l1 = max(a, l)
        q = 1 + 1.464 * ((a1 / l1) ** 1.65)

        eps = a1 / l1
        nyu = 2 * a1 * l1 / t

        F = 1 + nyu * (0.1786 + 0.039 * eps - 0.8255 * eps * eps + 0.8897 * eps * eps * eps) +\
            nyu * nyu * (-0.6485 - 0.3101 * eps + 3.3302 * eps * eps - 3.1083 * eps * eps * eps) +\
            nyu * nyu * nyu * (1.9715 - 2.4531 * eps + 0.0386 * eps * eps + 1.3748 * eps * eps * eps)

        k = oz * math.sqrt(math.pi * d / q) * F

    elif method == 6:
        d = t
        q = 1 + 1.464 * ((d / l) ** 1.65)

        if 5 <= R / t <= 10:
            A = (0.125 * R / t - 0.25) ** 0.25
        elif 10 < R / t <= 20:
            A = (0.4 * R / t - 0.3) ** 0.25

        F = 1 + A * (5.3303 * ((a / math.pi) ** 1.5) + 18.773 * ((a / math.pi) ** 4.24))

        k = oz * math.sqrt(math.pi * d / q) * F

    elif method == 7:

        k = non / sigmaT
        sigmaZ = 1.1 * sigmaT * (1 - 0.8 * k)

        myu = 2 * l / t
        f1 = 1.12 + 0.053 * myu + 0.0055 * myu * myu + (1 + 0.02 * myu + 0.0191 * myu * myu) * (20 - R / t) * (20 - R / t) / 1400
        at = a / t
        f2 = 1.12 + 6 * at * at - 7.672 * (at ** 4) + 28.65 * (at ** 6) - 22.09 * (at ** 8)
        F = min(f1, f2)

        kz = sigmaZ * math.sqrt(math.pi * a) * F

        k1 = kin(non, oz, l, a, t, dvn, p, 1, typeD)

        k = k1 + kz

    elif method == 8:
        k1 = kin(non, oz, l, a, t, dvn, p, 4.1)
        bt = 2 * l / t
        at = a / t

        if bt <= 2:
            if at <= (0.05 * (bt ** 0.55)):
                ro = 0.51 * (bt ** 0.27)
                s = -0.31
            else:
                ro = 0.83
                s = 0.15 * (bt ** 0.46)
        else:
            if at <= 0.073:
                ro = 0.615
                s = -0.31
            else:
                ro = 0.83
                s = -0.2

        m = ro * ((at) ** s)

        k = k1 * m

    return k
