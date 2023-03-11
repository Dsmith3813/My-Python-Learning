program = 'WSMain2.py'
# version = '1.0.2022.02' <<===<<< Original
version = '3.1.2023.03'

'''
World simulation program. A constant evelution in code.

NOTE: Misspellings by siri.
NOTE: See Peeps.sql for database schema

Just a project I though of doing and then modify as I get better at
writting python code. It all started with the question, can one populated the world with just two people starting out?

There has been three versions, number 2 flopped, I don't want to talk about it. The issue I had with version 1 was throughput performace and memory usage. As the propulation grew, the program slowed down and then memory was used up. All peeps info was held in memory (I have 64g). I tried to go to 1,000 years, got to 2 billion peeps when it died, 31 hours later! I would like to go to 2,023 years and then 2025 and see how close to real numbers the simulation gets. Although, this simulated world is not like planet earth.

Verion 3 I added a sqlite3 database (to solve the memory problem),
peeps DNA and fixed some of the events to be more radom. The DNA is also randomly built. I fixed or reworked the code to be more efficant. However,
it is still very slow. Adding the database is slow as the population grows; adding, deletting and updating records. 

The idea of this current world is that peeps works to the betterment of
all peeps. Therefore, all peeps effort is food generation. 

Food is procces into uints, a single unit feeds one peep for one year. The goal for the peeps is to have some percent of food units as surpules to be carried over to the next year. If the population plus 2% (popultion * 1.02) is greater than the number of food units, peeps die. 

Famnime affects food units production as well as spoilage. Something I need to consider, as the population grows, so will the space needed for fields. More peeps, more homes needed, less space for feilds. Over population

Murder has been added based on ones DNA. However, eventhough the code is there,
I have not tested it yet. 

At this point, I have six DNA bits unassigned that I want to assign, just not sure what to use them for.

I am planning on having war (riots) as part of the simulation, just not thought out all the details for war yet.

I want to add natural disasters.


Gaols; 
Efficant code. Still running really slow. I found out I had a few bugs as I restuctured the code. Now that these bugs are fixed, it still runs slow.
Better memory usage?
Better I/O for accsessing Peeps?
Get to year 2025
I would like to make a lot of these functions into classes. But with the 
database calls, I was getting errors. Not even sure if doing that will make any differance. One reason version 2 flopped.... no... wait... I don't want to talk about it.
Add AI componets to a Peep. 
'''

# Grid parms FOR FUTURE USE
# blockSize = 5           # Grid block size
# windowHight = 1200      # Grid hight
# windowWidth = 860       # Grid width
# WHITE = (255, 255, 255)
# BROWN = (210, 105, 30)
# YELLOW = (255, 255, 0)
# RED = (255, 0, 0)

# Peeps
gname = 1                        # STARTING NAME for common peeps
startPopulation = 2              # Adam & Eve starts this ball of wax
ChromLen = 16                    # size of a chromosome future AI
adamChrom = '1011111001000000'   # Adam's chromosome 0xbe40
eveChrom = '0111111001000000'    # Eve's chromosome  0x7e40
# Hex values was an idea I had for storing DNA

adamAge = 18
eveAge = 18

cycle = 100            # How many years to run the simulation

# Program parms
Num_nodes = 5          # number of neurons (input/output) FUTURE AI
Num_intnodes = 2       # number of hidden neurons  FUTURE AI
Killoff = 1            # Turn kill bit off 1 true, 0 false
Killage = 20           # Starting age for getting the urge to kill
LongLife = 72          # longest life length subject to change
AvgLife = 65           # Average life expectancy
LifeExtended = 1       # How much years to add whole numbers
LifeImprovment = 50    # Every x years improve life settings
brithBegin = 15        # age when a female can start having kids
brithEnd = 40          # age when no further births occur
marrageBegin = 14      # age someone can get married
Bitoff = '0'           # program use
Biton = '1'            # program use
warduration = 5        # If war breaks out, this is the duration
workage = 10           # starting age to begin to work
workperf = 2.25        # how much food units can a peep produce
foodpop = 1.02         # popualation pecent used for calculating events

# Probabilites. The simulation has a flip a coin function, these values are
# passed to that function
fertel = 0.400         # of a women getting pregneate
lessFertal = 0.150     # of older women not able to get preg
missCarrage = 0.030    # of a mis-carrage  - actual statistic from W.H.O
twins = 0.050          # of having twins   - actual statistic form W.H.O
marprob21 = 0.700      # marrage probability for young folks
marprob31 = 0.400      # marrage proabilty for older folks
warprob = 0.013        # chance of war Not implemented yet
terminal = 0.030       # chance of having a terminal sickness
famine = 0.100         # chance of a famine hitting
spoilage = 0.090       # how many food units could spoil
murder = 0.080         # chance of someone getting killed

'''
Chromosome is built from two 8 bit geano (16 bits)
DNA bit meanings
Bit 0 Gender        Female = 0, male = 1
Bit 1 Fertil        If female, able to be pregnint male able to impregnate
Bit 2 Pheromones1   How affective pheromons are; level 1
Bit 3 Pheromones2   Level 2. If both levels on, level 3
Bit 4 Marigae       Willing to marry
Bit 5 Mates         Willing to mate
Bit 6 Kill          Willing to kill
Bit 7 VICTIM        Beings a Victim
Bit 8 Longlife      lives longer than most people
Bit 9 PreDisp       predisposed to terminal illness
Bit A ???
Bit B ???
Bit C ???
Bit D ???
Bit E ???
Bit F ???
'''
