import random
import WSParms2 as pm


class person():
    def adam():
        pname = 'Adam'
        pgender = 1
        page = pm.adamAge
        pprego = 0
        pmarried = 1
        BIT0 = 1    # 1011111001000000
        BIT1 = 0
        BIT2 = 1
        BIT3 = 1
        BIT4 = 1
        BIT5 = 1
        BIT6 = 1
        BIT7 = 0
        BIT8 = 0
        BIT9 = 1
        BITA = 0
        BITB = 0
        BITC = 0
        BITD = 0
        BITE = 0
        BITF = 0

        return pname, pgender, page, pprego, pmarried, BIT0, BIT1, \
            BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9,        \
            BITA, BITB, BITC, BITD, BITE, BITF

    def eve():
        pname = 'Eve'
        pgender = 0
        page = pm.eveAge
        pprego = 1
        pmarried = 1
        BIT0 = 0     # 0111111001000000
        BIT1 = 1
        BIT2 = 1
        BIT3 = 1
        BIT4 = 1
        BIT5 = 1
        BIT6 = 1
        BIT7 = 0
        BIT8 = 0
        BIT9 = 1
        BITA = 0
        BITB = 0
        BITC = 0
        BITD = 0
        BITE = 0
        BITF = 0

        return pname, pgender, page, pprego, pmarried, BIT0, BIT1, \
            BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9,        \
            BITA, BITB, BITC, BITD, BITE, BITF

    def createPerson():
        ''' Creates a persons '''

        # Create a name
        pm.gname += 1
        pname = 'P' + str(pm.gname)
        page = 0
        pprego = 0

        # Build their dna
        dna = ''
        for i in range(pm.ChromLen):
            # Bits 6 & 7 deals with murder, if murder is turned off
            # Just st these two bits to 00
            if i == 6 and pm.Killoff:
                dna += '00'
                i += 1
            else:
                dna += str(random.randint(0, 1))

        pgender = dna[0]

        BIT0 = dna[0]
        BIT1 = dna[1]
        BIT2 = dna[2]
        BIT3 = dna[3]
        BIT4 = dna[4]
        BIT5 = dna[5]
        BIT6 = dna[6]
        BIT7 = dna[7]
        BIT8 = dna[8]
        BIT9 = dna[9]
        BITA = dna[10]
        BITB = dna[11]
        BITC = dna[12]
        BITD = dna[13]
        BITE = dna[14]
        BITF = dna[15]
        
        page = 0
        pprego = 0
        pmarried = 0

        return pname, pgender, page, pprego, pmarried, BIT0, BIT1, \
            BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9,        \
            BITA, BITB, BITC, BITD, BITE, BITF

    # used to decode stored hex chromosomes furture
    # def decode_Chromosome(CHRM):
    #     x = bin(int(CHRM, pm.Ch))
    #     y = bin(int(x, 2))[2:]
    #   # When hex is turned into numeric string, leading 0 can be missing.
    #   # this fixes this problem.
    #     DNA = y
    #     x = pm.Ch - len(y)
    #     if x != 0:
    #         for i in range(x):
    #             DNA = '0' + DNA
    #     return DNA
