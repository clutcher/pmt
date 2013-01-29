# -*- coding: utf-8 -*-


def k1c(kcv, e=200000, myu=0.3):
    import math

    k1c = 0.1 * math.sqrt(0.1 * kcv * e / (1 - myu * myu))
    return k1c


def dkzm(k1, kn, m):
    """Допустимый коэффициент запаса прочности
    k1, kn, m - смотреть в СНиП 2.05.06
    k1 - коэффициент надежности по материалу
    kn - коэффициент надежности по назначению
    m - коэффициент условия работы
    """
    return 0.9 * k1 * kn / m


def kzm(k1, k1c, sigmaR, sigmaB, sigmaT, k, method):
    """
    k - допустимый коэфициент запаса прочности
    """

    def kd(kra, sra, tb, k):
        if 0.9 <= sra <= 1:
            return "Критический"
        elif tb / 1.1 <= sra < 0.9:
            if 0 <= kra < (-1 * sra + 0.45):
                return "Значительный"
            else:
                return "Критический"
        elif 1 / k <= sra < tb / 1.1:
            if 0 <= kra < (-1 * sra + 0.5 * tb / 1.1):
                return "Умеренный"
            elif (-1 * sra + 0.5 * tb / 1.1) <= kra < (-1 * sra + 0.45):
                return "Значительный"
            else:
                return "Критический"

        if 0.9 <= kra <= 1:
            return "Критический"
        elif tb / 1.1 <= kra < 0.9:
            if 0 <= sra < (-1 * kra + 0.45):
                return "Значительный"
            else:
                return "Критический"
        elif 1 / k <= kra < tb / 1.1:
            if 0 <= sra < (-1 * kra + 0.5 * tb / 1.1):
                return "Умеренный"
            elif (-1 * kra + 0.5 * tb / 1.1) <= sra < (-1 * kra + 0.45):
                return "Значительный"
            else:
                return "Критический"

        if 0.41 / k <= sra < 1 / k:
            if 0 <= kra < -sra + 0.5 / k:
                return "Не значительный"
            elif -sra + 0.5 / k <= kra < -sra + 0.5 * tb / 1.1:
                return "Умеренный"
            elif kra >= -sra + 0.5 * tb / 1.1:
                return "Значительный"
        elif sra < 0.41 / k:
            return "Не значительный"

    if method == 1:
        if k1 == 0:
            return sigmaB / sigmaR

        kra = k1 / k1c
        sra = sigmaR / sigmaB

        tb = sigmaT / sigmaB

        a1 = 1 / sra
        a2 = 0.7 / (1 - 0.7 * tb)
        b1 = -1 / kra
        b2 = 1.
        c1 = 0.
        c2 = -1 * (1 - 0.21 * tb) / (1 - 0.7 * tb)

        sra2 = -1 * (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
        kra2 = -1 * (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)

        if 0.0 <= kra2 < 0.3:
            sra2 = 1.
            kra2 = kra / sra
        elif 0.0 <= sra2 < 0.7 * tb:
            kra2 = 1.
            sra2 = sra / kra

        kzm = kra2 / kra
        kategoriya = kd(kra, sra, tb, k)

    elif method == 2:
        kzm = sigmaB / sigmaR
        kategoriya = 'Not defined'

    return kzm, kategoriya
