import sympy.combinatorics.graycode

def varToBinary(E, rho):
    E_bin = [int(x) for x in list('{0:050b}'.format(int(E)))]
    rho_bin = [int(x) for x in list('{0:050b}'.format(int(rho)))]
    return E_bin + rho_bin

def binaryToVar(bin):
    E = "".join(str(x) for x in bin[0:50])
    rho = "".join(str(x) for x in bin[51:100])
    E = sympy.combinatorics.graycode.gray_to_bin(E)
    rho = sympy.combinatorics.graycode.gray_to_bin(rho)

    E = int(E, 2)
    rho = int(rho, 2)

    return [E, rho]

def binaryToStr(bin):
    return "".join(str(x) for x in bin)

def ModalTwoPoint(ind1, ind2):
    size = len(ind1)
    cxpoint1 = int(round(1.0*size/3.0))
    cxpoint2 = int(round(2.0*size/3.0))

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]
    return ind1, ind2

def ModalSixPoint(ind1, ind2):
    size = len(ind1)
    cxpoint1 = int(round(1.0*size/7.0))
    cxpoint2 = int(round(2.0*size/7.0))
    cxpoint3 = int(round(3.0*size/7.0))
    cxpoint4 = int(round(4.0*size/7.0))
    cxpoint5 = int(round(5.0*size/7.0))
    cxpoint6 = int(round(6.0*size/7.0))

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]
    ind1[cxpoint3:cxpoint4], ind2[cxpoint3:cxpoint4] = ind2[cxpoint3:cxpoint4], ind1[cxpoint3:cxpoint4]
    ind1[cxpoint5:cxpoint6], ind2[cxpoint5:cxpoint6] = ind2[cxpoint5:cxpoint6], ind1[cxpoint5:cxpoint6]
    return ind1, ind2

def Modal40Point(ind1, ind2):
    size = len(ind1)
    cxpoint1 = int(round(1.0*size/10.0))
    cxpoint2 = int(round(2.0*size/10.0))
    cxpoint3 = int(round(3.0*size/10.0))
    cxpoint4 = int(round(4.0*size/10.0))
    cxpoint5 = int(round(5.0*size/10.0))
    cxpoint6 = int(round(6.0*size/10.0))
    cxpoint7 = int(round(7.0*size/10.0))
    cxpoint8 = int(round(8.0*size/10.0))
    cxpoint9 = int(round(9.0*size/10.0))

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]
    ind1[cxpoint3:cxpoint4], ind2[cxpoint3:cxpoint4] = ind2[cxpoint3:cxpoint4], ind1[cxpoint3:cxpoint4]
    ind1[cxpoint5:cxpoint6], ind2[cxpoint5:cxpoint6] = ind2[cxpoint5:cxpoint6], ind1[cxpoint5:cxpoint6]
    ind1[cxpoint7:cxpoint8], ind2[cxpoint7:cxpoint8] = ind2[cxpoint7:cxpoint8], ind1[cxpoint7:cxpoint8]
    ind1[cxpoint9:size], ind2[cxpoint9:size] = ind2[cxpoint9:size], ind1[cxpoint9:size]
    return ind1, ind2