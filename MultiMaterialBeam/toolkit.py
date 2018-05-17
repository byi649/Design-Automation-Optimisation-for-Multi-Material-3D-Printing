import sympy.combinatorics.graycode

def varToBinary(E, rho):
    E_bin = [int(x) for x in list('{0:050b}'.format(int(E)))]
    rho_bin = [int(x) for x in list('{0:050b}'.format(int(rho)))]
    return E_bin + rho_bin

def binaryToVar(bin):
    # E = int("".join(str(x) for x in bin[0:50]), 2)
    # rho = int("".join(str(x) for x in bin[51:100]), 2)
    E = "".join(str(x) for x in bin[0:50])
    rho = "".join(str(x) for x in bin[51:100])
    E = sympy.combinatorics.graycode.gray_to_bin(E)
    rho = sympy.combinatorics.graycode.gray_to_bin(rho)

    E = int(E, 2)
    rho = int(rho, 2)

    return [E, rho]

def binaryToStr(bin):
    return "".join(str(x) for x in bin)