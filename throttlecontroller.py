LB = 0
UB = 255


def openleft(x, a, b):
    return 1 if x <= a else 0 if x >= b else (x - a) / (b - a)


def openleftarea(mu, a, b):
    b1 = b - mu*(b-a)
    b2 = b - LB
    return 0.5*mu*(b1+b2)


def openright(x, a, b):
    return 1 if x >= b else 0 if x <= a else (b - x) / (b - a)


def openrightarea(mu, a, b):
    b1 = UB - a - mu*(b - a)
    b2 = UB - a
    return 0.5*mu*(b1+b2)


def triangular(x, a, b, c):
    return max(0, min((x-a)/(b-a), (c-x)/(c-b)))


def trianglearea(mu, a, b, c):
    b1 = (c - mu*(c-b)) - (a + mu*(b-a))
    b2 = c-a
    return 0.5*mu*(b1+b2)


def trapezoidal(x, a, b, c, d):
    return max(0, min((x-a)/(b-a), 1, (d-x)/(d-c)))


# both inputs and output have the same fuzzy set definitions so making use of the same function 'fuzzifier'
def fuzzifier(x):
    NL = openleft(x, 31, 61)
    NM = triangular(x, 31, 61, 95)
    NS = triangular(x, 61, 95, 127)
    ZE = triangular(x, 95, 127, 159)
    PS = triangular(x, 127, 159, 191)
    PM = triangular(x, 159, 191, 223)
    PL = openright(x, 191, 223)

    return NL, NM, NS, ZE, PS, PM, PL


def compare(a, b):
    return a if b == 0 else b if a == 0 else min(a, b)


def rule(speed_difference, acceleration):

    NLSD, NMSD, NSSD, ZESD, PSSD, PMSD, PLSD = speed_difference
    NLAC, NMAC, NSAC, ZEAC, PSAC, PMAC, PLAC = acceleration

    NLTC = NMTC = NSTC = ZETC = PSTC = PMTC = PLTC = 0

    # rule 1 and 2
    PLTC1 = min(NLSD, ZEAC)
    PLTC2 = min(ZESD, NLAC)
    PLTC = compare(PLTC1, PLTC2)

    # rule 3 and 8
    PMTC1 = min(NMSD, ZEAC)
    PMTC2 = min(ZESD, NMAC)
    PMTC = compare(PMTC1, PMTC2)

    # rule 4 and 7
    PSTC1 = min(NSSD, PSAC)
    PSTC2 = min(ZESD, NSAC)
    PSTC = compare(PSTC1, PSTC2)

    # rule 5
    NSTC = min(PSSD, NSAC)

    # rule 6
    NLTC = min(PLSD, ZEAC)

    return NLTC, NMTC, NSTC, ZETC, PSTC, PMTC, PLTC


def defuzzifier(throttle):
    NLTC, NMTC, NSTC, ZETC, PSTC, PMTC, PLTC = throttle

    NLTCarea = openleftarea(NLTC, 31, 61)
    NMTCarea = trianglearea(NMTC, 31, 61, 95)
    NSTCarea = trianglearea(NSTC, 61, 95, 127)
    ZETCarea = trianglearea(ZETC, 95, 127, 159)
    PSTCarea = trianglearea(PSTC, 127, 159, 191)
    PMTCarea = trianglearea(PMTC, 159, 191, 223)
    PLTCarea = openrightarea(PLTC, 191, 223)

    numerator = NLTCarea*(LB - 61)/2 + NMTCarea*61 + NSTCarea*95 + \
        ZETCarea*127 + PSTCarea*159 + PMTCarea*191 + PLTCarea*(UB - 191)/2
    denominator = NLTCarea + NMTCarea + NSTCarea + \
        ZETCarea + PSTCarea + PMTCarea + PLTCarea

    if denominator == 0:
        print("No rules to calculate the output")
        return -1

    return numerator/denominator


speed_difference = fuzzifier(100)
acceleration = fuzzifier(70)

throttle = rule(speed_difference, acceleration)
print(defuzzifier(throttle))
