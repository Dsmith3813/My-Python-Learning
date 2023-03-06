program = 'WSMain2.py'
# version = '1.0.2022.02'
version = '3.1.2023.03'

'''
World simulation program. A constant evelution in code.

Just a project I though of doing and then modify
as I get better writting code. There has been three versions, number 2
flopped. The issue I had with version 1 was throughput performace and
memory use. As the propulation grew, the program slowed down and then 
memory was used up. All persons info was held in memory. I tried to go
to 1,000 years, got to 3 billion persons when it died, 26 hours later.

Verion 3 I added a database (to solve the memory problem), DNA and 
fixed some of the events to be more radom. Also, the DNA is also 
randomly built.

The idea of this current world is that everyone works to the betterment of
all. So, everyone's effort is food generation. Food is procces into uints,
a sigel unit feeds one person for one year. The main goal is to have some
percent of food unit surpules. If the population plus 2% (popultion * 1.02)
is greater than the number of food units, people die. Famnime affects
food units. 

Murder as been added based on ones DNA. At this point, I have six bits 
unassigned that I want to assign, just not sure what to attribute to peeps
yet.

I am planning having war part of the simulation, just now thought out a 
good mechinisem for war yet.

Gaols; 
Efficant code.
Better memory usage.
Better I/O for accsessing Peeps.
To add AI componets to a Peep, so their actions is really made from their
 DNA.
'''

# Grid parms FOR FUTURE USE
# blockSize = 5           # Grid block size
# windowHight = 1200      # Grid hight
# windowWidth = 860       # Grid width
# WHITE = (255, 255, 255)
# BROWN = (210, 105, 30)
# YELLOW = (255, 255, 0)
# RED = (255, 0, 0)

# persons
gname = 1                        # STARTING NAME for common people
startPopulation = 2              # Adam & Eve starts this ball of wax
Ch = 16                          # size of a chromosome
adamChrom = '1011111001000000'   # Adam's chromosome 0xbe40
eveChrom = '0111111001000000'    # Eve's chromosome  0x7e40
adamAge = 18
eveAge = 18

cycle = 600          # How many years to run simulation

# Program parms
Num_nodes = 5        # number of neurons (input/output) FUTURE
Num_intnodes = 2     # number of hidden neurons  FUTURE
Killoff = 1          # Turn kill bit off 1 true, 0 false
Killage = 20         # Starting age
LongLife = 70        # longest life length subject to change
Life = 60            # Average life expectancy
LifeExtended = 1     # How much years to add
LifeImprovment = 76  # Years to improve life expectancy (change parms)
Bbirth = 16          # age when a female cat start having kids
Ebirth = 35          # age when no further births occur
marstart = 14        # age someone can get married
Bitoff = '0'         # program use
Biton = '1'             ''     ''
warduration = 5      # If war breaks out, this is the duration
workage = 10         # starting age to begining to work
workperf = 1.75      # how much food units can a person produce
popup = 1.02         # popualation pecent used for calculating events

# Probabilites
fertel = 0.400       # of a women getting pregneate
unfertel = 0.100     # of older women not able to get preg
missc = 0.030        # of a mis-carrage  - actual statistic from W.H.O
twin = 0.050         # of having twins   - actual statistic form W.H.O
marprob21 = 0.085    # marrage probability for young folks
marprob31 = 0.533    # marrage proabilty for older folks
warprob = 0.013      # chance of war
termill = 0.030      # of having a terminal sickness
famine = 0.050       # of a famine hitting
spoilage = 0.030     # how many food units could spoil
murder = 0.080       # of someone gets killed

'''
Chromosome is built from two 8 bit geano (16 bits)
DNA attributs bit meaning
Bit 0 Gender      Female = 0, male = 1
Bit 1 Fertil      If female, able to be pregnint male able to impregnate
Bit 2 Pheromones1 How affective pheromons are; level 1
Bit 3 Pheromones2 Level 2 If both levels on, level 3
Bit 4 Marigae     Willing to marry
Bit 5 Mates       Willing to mate
Bit 6 Kill        Willing to kill
Bit 7 VICTIM      Beings a Victim
Bit 8 Longlife    lives longer than most people
Bit 9 PreDisp     predisposed to terminal illness
Bit A ???
Bit B ???
Bit C ???
Bit D ???
Bit E ???
Bit F ???
'''