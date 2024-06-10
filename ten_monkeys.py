import sys
from fractions import Fraction
nred = int(sys.argv[1])
nblack = int(sys.argv[2])
nchecked_red = int(sys.argv[3])


def redwin_proba(nred, nblack, nchecked_red):
    if nblack == 0:
        return Fraction(1,1)
    if nred <= nblack:
        return Fraction(0,1)
    if nred + nblack == 4:
        return Fraction(2, (4 - nchecked_red))
    kick_black_proba = Fraction(nblack, (nblack + nred - nchecked_red))
    return kick_black_proba * redwin_proba(nred - 1, nblack - 1, max(nchecked_red - 1, 0)) + (1 - kick_black_proba) * redwin_proba(nred - 2, nblack, max(nchecked_red - 1, 0))

if __name__ == "__main__":
    print(redwin_proba(nred, nblack, nchecked_red))