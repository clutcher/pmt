def koroziya(a1, a2, dt, dn, kkr=2.):

    Va = (a2 - a1) / dt
    a = 0.8 * dn
    t = (a2 - a) / (kkr * Va)

    return t


def stress(a1, ast, n, kin, dn):
    a = 0.8 * dn
    v = ast * (kin ** n)
    t = v / (a - a1)

    return t


def nav(a1, bf, m, dkin, dn):
    a = 0.8 * dn
    v = bf * (dkin ** m)
    n = v / (a - a1)

    return int(n)