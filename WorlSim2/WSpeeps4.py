import random
import WSParms4 as pm


class person():

    def adam():
        pname = 1           # 11111110010010000
        BIT0 = pm.adamAge   # Age

        BIT1 = 1            # Gender
        BIT2 = 1            # Fertile
        BIT3 = 1            # Pheromones1
        BIT4 = 1            # Pheromones2
        BIT5 = 1            # Willing to marry
        BIT6 = 1            # Willing to mate
        BIT7 = 0            # Is a killer
        BIT8 = 0            # Is a victim
        BIT9 = 1            # Long life
        BITA = 0            # predisposed to terminal illness
        BITB = 0            # Pregnant
        BITC = 1            # Married
        BITD = 0            # ???
        BITE = 0            # ???
        BITF = 0            # ???
        BITG = 0            # ???

        return pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG

    def eve():
        pname = 2           # 0111110010110000
        BIT0 = pm.eveAge    # Age

        BIT1 = 0            # Gender
        BIT2 = 1            # Fertile
        BIT3 = 1            # Pheromones1
        BIT4 = 1            # Pheromones2
        BIT5 = 1            # Willing to marry
        BIT6 = 1            # Willing to mate
        BIT7 = 0            # Is a killer
        BIT8 = 0            # Is a victim
        BIT9 = 1            # Long life
        BITA = 0            # predisposed to terminal illness
        BITB = 1            # Pregnant
        BITC = 1            # Married
        BITD = 0            # ???
        BITE = 0            # ???
        BITF = 0            # ???
        BITG = 0            # ???

        return pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG

    def createPerson():
        ''' Creates a persons '''

        # Create a name
        pm.PeepsName += 1
        pname = pm.PeepsName

        # Build their dna
        dna = ''
        for i in range(17):
            dna += str(random.randint(0, 1))

        BIT0 = 0                # Age

        BIT1 = int(dna[1])      # Gender
        BIT2 = int(dna[2])      # Fertile
        BIT3 = int(dna[3])      # Pheromones1
        BIT4 = int(dna[4])      # Pheromones2
        BIT5 = int(dna[5])      # Willing to marry
        BIT6 = int(dna[6])      # Willing to mate
        BIT7 = int(dna[7])      # Is a killer
        BIT8 = int(dna[8])      # Is a victim
        BIT9 = int(dna[9])      # Long life
        BITA = int(dna[10])     # predisposed to terminal illness
        BITB = 0                # Pregnant
        BITC = 0                # Married
        BITD = int(dna[13])     # ???
        BITE = int(dna[14])     # ???
        BITF = int(dna[15])     # ???
        BITG = int(dna[16])     # ???

        return pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, \
            BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG

    # used to decode stored hex chromosomes Future use
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
