program = 'WSMain4.py'
# version = '1.0.2022.02' <<===<<< Original
version = '4.1.2023.07'
PGMDescription = 'World Simulation IV'

'''
World simulation program. A constant evolution in code.

NOTE: Misspellings by Siri.
NOTE: See Peeps.sql for database schema

Just a project I though of doing and then modify as I get better at
writing python code. It all started with the question, can one populated the world with just two people starting out?

Change Log
----------

Version 1

The issue I had with version 1 was throughput performance and memory usage. As the population grew, the program slowed down and then memory was used up. All peeps info was held in memory (I have 64g). I tried to go to 1,000 years, got to 2 billion peeps when it died, 31 hours later! I would like to go to 2,023 years and then 2025 and see how close to real numbers the simulation gets. Although, this simulated world is not like planet earth. This version used a list to store the Peeps.

Version 2 flopped, I don't want to talk about it. I was adding new code and I had some sort of crash and lost it. 

Version 3 

I used version 1 as the base and removed the list and added a sqlite3 database (to solve the memory problem), gave peeps DNA and fixed some of the events to be more radom. The DNA is also randomly built. I fixed or reworked the code to be more efficient. 

However, it is still very slow (slower than version 1). Adding the database is slow as the population grows; adding, deleting and updating records becomes more I/O intensive.I checked the web for some trick, but they shaved off minutes, I couldn't run 200 years with out running into long hours (6-10 hours). NOTE: Adding the database made the program run even slower. Running for 100 years takes about 32.3 seconds. Running for 200 years, one would think it takes maybe 1-5 minutes. NO! It takes 420+ minutes. Vary unacceptable. It does use the GPU, but the max I have seen it go is 20-26%. The database solved the memory issue, but not even close for how long it takes to run.

Version 4

I removed the database and created a dictionary. This has helped the run times, but it still uses a lot of memory. 500 years takes about 90gb of ram before dying. The coded was reworked, and some improvements made the code cleaner. Also correct some logic as it wasn't correct in some spots. Now, I am working to reduce the memory foot print. There are 4 areas of concern:

Peeps {} This is the main dictionary that hold the peeps population

        Key         Peeps identifier.
        Attributes  A groups of concerning the peeps
                    Age int
                    Bit0-G DNA type values that describes the peep
                    About 19 bytes

MalesRows & Females rows. These are temp dictionaries that hold all males & females that can get married. Size is the same as Peeps. The idea was to introduce a way to having children occur more predictably than say non married females getting pregnant. The process;

Gather all males that are not married and are of marring age.
Gather all females that are not married and are of marring age.
Walk thru these two and see if they marry each other.
If they do, set the marry bit and update the Peeps.
At the end, delete the MalesRows & FemaleRows dictionaries.

I'm thinking of removing this constraint to test how this may help. To do this,
I will need to also make a change to the WithChild function to use only one
fertility probability.

Also thinking of a way to compress the DNA part of the peeps entry. Some test show that I can shave the size for 19 bytes to 9 bytes. Still testing.

I will be splitting the PARMS file (parameter file) into two parts. Static values and dynamic values. This will give the ability to make some changes on the fly.


The world order
---------------

The idea of this current world is that peeps works to the betterment of
all peeps. Food is the utmost important commodity, Peeps don't live without food. Therefore, all peeps effort is food generation and storage. 

Food is processed into units, a single unit feeds one peep for one year. The goal for the peeps is to have some percent of food units as surplus to be carried over to the next year. If the population is greater than the number of food units, Peeps die. 

Famine affects food unit production. Spoilage affects food storage. NOTE: Something I need to consider, as the population grows, so will the space needed for fields. More peeps, more homes needed, less space for fields. Over population. 

Murder has been added based on ones DNA. However, even though the code is there,
I have not tested it out yet. 

At this point, I have four DNA bits unassigned that I want to assign, just not sure what to use them for.

I am planning on having war (riots) as part of the simulation, just not thought out all the details for war yet.

I want to add natural disasters.


Gaols:
------ 
Efficient code. Still running really slow. I found out I had a few bugs as I restructured the code. Now that these bugs are fixed, it still runs slow.
Better memory usage?
Better I/O for accessing Peeps?  <<<< This is a biggie
Get to year 2025
I would like to make a lot of these functions into classes. But with the 
database calls, I was getting errors. Not even sure if doing that will make any difference. One reason version 2 flopped.... no... wait... I don't want to talk about it.
Add AI components to a Peep. 
'''

# Grid parms # NOTE: FOR FUTURE USE
# blockSize = 5           # Grid block size
# windowHight = 1200      # Grid hight
# windowWidth = 860       # Grid width
# WHITE = (255, 255, 255)
# BROWN = (210, 105, 30)
# YELLOW = (255, 255, 0)
# RED = (255, 0, 0)

# Parms for the simulator

# STARTING NAME for common peeps. NOTE: This parm is updated by WSpeeps?.py
# Since it is not stored and incremented in any other program.
PeepsName = 2

startPopulation = 2              # Adam & Eve starts this ball of wax
ChromLen = 16                    # size of a chromosome future AI
adamChrom = '1111111010000000'   # Adam's chromosome 0xfe80
eveChrom = '0111110010000000'    # Eve's chromosome  0x7c80
# Hex values was an idea I had for storing DNA

adamAge = 18
eveAge = 18

cycle = 300            # How many years to run the simulation
LifeImprovements = 25  # Every x years improve life settings

# Program parms
Num_nodes = 5          # number of neurons (input/output) FUTURE AI
Num_intnodes = 2       # number of hidden neurons  FUTURE AI

Killoff = 1            # Turn kill bit off 1 true, 0 false
Killage = 20           # Starting age for getting the urge to kill

LongLife = 72          # longest life length subject to change
AvgLife = 65           # Average life expectancy
LifeExtended = 1       # How many years to add in whole numbers

birthBegin = 16        # age when a female can start having kids
birthBeginMax = 21     # Maximum starting birthing age.
birthEnd = 40          # age when no further births occur
birthMiddleAge = 30    # Middle age of a female when they become less fertile

marriageBegin = 17     # age someone can get married

warDuration = 5        # If war breaks out, this is the duration

WorkAge = 9              # starting age to begin to work
WorkAgeEnd = LongLife - 5
WorkProduce = 1.95        # How much units of food a peep can make
ProduceMaxStore = 2       # how much food units can be stored
NaturalPlanetFood = 1000  # Natural food found on the planet in units

# Probabilities. The simulation has a flip a coin function, these values are
# passed to that function
fertile = 0.050        # of a women getting pregnant
lessFertile = 0.040    # of older women not able to get pregnant
missCarriage = 0.060   # of a mis-carriage  - actual statistic from W.H.O
twins = 0.030          # of having twins   - actual statistic form W.H.O
marprob21 = 0.700      # marriage probability for young folks
marprob31 = 0.350      # marriage probability for older folks

warprob = 0.013        # chance of war Not implemented yet
terminal = 0.050       # chance of having a terminal sickness

famine = 0.150         # chance of a famine hitting
spoiled = 0.150        # chance of stored food spoiling
Spoilage = 0.200       # how much food units could spoil

murder = 0.080         # chance of someone getting killed

# Chromosome values

# Booleans values for DNA chromosomes
Female = 0
Male = 1
Yes = 1
No = 0

# Positions into the DNA chromosomes
Age = 0
Gender = 1
PH1 = 3
PH2 = 4
WillingM = 5
Mates = 6
LongLifeSpan = 9
Sick = 10
Pregnant = 11
Married = 12


'''
Chromosome is built from two 8 bit geans (16 bits) plus age byte
DNA bit meanings
Bit 0 Age
Bit 1 Gender        Female = 0, male = 1
Bit 2 Fertile       If female, able to be pregnant male able to impregnate
Bit 3 Pheromones1   How affective pheromones are; level 1
Bit 4 Pheromones2   Level 2. If both levels on, level 3
Bit 5 Marriage      Willing to marry
Bit 6 Mates         Willing to mate
Bit 7 Kill          Willing to kill
Bit 8 VICTIM        Can be a Victim
Bit 9 Long life     lives longer than most people
Bit A PreDisp       predisposed to terminal illness
Bit B Pregnant
Bit C Married
Bit D ???
Bit E ???
Bit F ???
Bit G ???
'''
'''
Some space and population info

Radius of earth 3977 miles
Formula for surface area of spheres
S = 4 * PIE * (3977^2) = 198,655,604.24 (199 million sq miles)
30% of earth's surface is habitable land
0.30 * 199 = 60 million sq miles
1 sq mile is 27,878,400 sq feet (from google)

For my world 5 sq feet = 1 living space per-person.
27,878,400 / 5 = 5,575,680 persons in a sql mile.
5,575,680 * 60 million sq miles = 334,540,800,000,000
Current earth population is 8 trillion


Some other figures
29% (149 million km^2) land mass
71% (104 million km^2) Habitable land 
        50% (51 million km^2) agriculture
        48% (48 million km^2) Forest/grasses
77% (40 million km^2) 

How many Peeps for a family unit?
How much land is required to grow food?
How much land is required to raise food live stock?
'''
