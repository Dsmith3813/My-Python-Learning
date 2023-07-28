# My attempt to make a world simulator. This package is still
# A work in progress. It runs, but not all the planned functionality is
# represented... YET! NOTE See WSParms.py for more details.
#
# NOTE: My first program, so it probably isn't very good python coding.
# But, I can write a mean assembler program!
#
# TheBigD Started: 02/04/2022. Development continues.
# Copyright (c) 2023 Dennis J. Smith All Rights Reserved License: MIT

# Needed bits
import WSParms4 as pm       # Parameter file.
import WSpeeps4 as cp        # Class to create a peep.
import WSTools as t         # Tool class.
import datetime
import termcolor as tc
import os
import sys
import csv
from statistics import mean
from DJSTimer import Timer

os.system('Clear')

# Set global in memory accumulators and parms.
# NOTE Investigate make this a data class?
Peeps = {}              # Peeps memory table

world = []              # Memory stor of the condition of the world file
avgDR = []              # After a given cycle (epoch)
avgBR = []

Population = 0          # program Population
year = 0                # In memory variable
EvePassed = 0           # Flags
AdamPassed = 0
FoodStore = pm.NaturalPlanetFood  # In memory storage container.

# Parm entries that change over time is stored here and modified here
# by the program
longlife = pm.LongLife
life = pm.AvgLife
EndBirth = pm.birthEnd
StartBirth = pm.birthBegin
BirthMiddleAge = pm.birthMiddleAge

# CSV Fields  (Columns names)
fields1 = ['Year', 'Population', 'Workers', 'Food Storage', 'Food Generated',   'Spoiled', 'Famine', 'Births', 'Twins',
           'Miscarriage' 'Birth Rate', 'Pregnant CNT', 'Deaths', 'Natural', 'Sickness', 'Murdered', 'Starved', 'Death Rate']

lines = ''
lines += f'\n>> {pm.PGMDescription} {pm.program} V{pm.version}'


def init():
    '''
    Sets Program defaults and creates the first two peeps
    residing in the world and stores the information in the Peeps
    database table Peeps; Adam and Eve. Initial settings for
    Adam and Eve are stored in the parm file WSparms.py
    '''
    global Population

    # Setup Adam
    pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG = cp.person.adam()

    Peeps[pname] = [BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6,
                    BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG]

    # Set up Eve
    pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG = cp.person.eve()

    Peeps[pname] = [BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6,
                    BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF]

    LGyear = 1
    Population = 2

    return LGyear


def build_persons():

    global Population

    pname, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG = cp.person.createPerson()

    Peeps[pname] = [BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6,
                    BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF, BITG]

    Population += 1


def calculate_death_range(starved):
    '''
    Calculate the death (deletes) range by peeps name. Peeps affected
    by starvation is the youngest children in this world. 
    '''

    global Population

    death_cnt = 0
    NewestPeep = pm.PeepsName           # The youngest of them all
    StartPeep = NewestPeep - starved    # The starting point of deletes.

    # Loop over peeps with calculated start stop values, and delete.
    for i in range(StartPeep, NewestPeep, 1):
        skipped = Peeps.pop(i, True)
        if skipped:
            continue
        else:
            death_cnt += 1

    Population -= death_cnt

    return death_cnt


def LoveNThunder():
    ''' 
    Get a list of eligible girls to see if they are willing to become
    pregnant
    '''

    global StartBirth, EndBirth

    pregCount = 0

    # Walk through the peeps and check females that are within birthing age
    # and not pregnant. Based on BirthMiddleAge, they have a different
    # probability of getting pregnant than younger gals
    for key, attrib in Peeps.items():
        if attrib[pm.Gender] == pm.Female          \
                and attrib[pm.Pregnant] == pm.No   \
                and attrib[pm.Age] >= StartBirth       \
                and attrib[pm.Age] <= EndBirth:

            if attrib[pm.Age] < BirthMiddleAge:
                if t.flip(pm.fertile) == True:
                    attrib[pm.Pregnant] = pm.Yes
                    Peeps.update({key: attrib})
                    pregCount += 1

            elif t.flip(pm.lessFertile) == True:
                attrib[pm.Pregnant] = pm.Yes
                Peeps.update({key: attrib})
                pregCount += 1

    return pregCount


def withChild():
    '''
    To determine if a pregnant female gives birth
    '''

    birthcnt = 0
    twcnt = 0
    miscnt = 0
    AddBaby = 0

    for key, attrib in Peeps.items():
        if attrib[pm.Gender] == pm.Female         \
                and attrib[pm.Pregnant] == pm.Yes:
            if key > 2 and t.flip(pm.missCarriage) == True:  # Miscarriage?
                attrib[pm.Pregnant] == pm.No
                Peeps.update({key: attrib})
                miscnt += 1
            elif t.flip(pm.twins) == True:  # Twins! Create the little buggers
                AddBaby += 2
                attrib[pm.Pregnant] == pm.No
                Peeps.update({key: attrib})
                birthcnt += 2
                twcnt += 1
            else:
                # Yah... the cute little bambino
                AddBaby += 1
                attrib[pm.Pregnant] == pm.No
                Peeps.update({key: attrib})
                birthcnt += 1

    if AddBaby > 0:
        for i in range(AddBaby):
            build_persons()

    return birthcnt, twcnt, miscnt


def FieldOfDreams():
    '''
    Determines the state of the food supply by calculating able
    bodied peeps to plant, grow and harvest the fields. In this 
    simulation all peeps live to help the whole Population.

    I do not round numbers concerning food production. I convert 
    calculations to int. Any fractional lost is due to the process of
    food production into units.
    '''
    global Population, FoodStore, year

    AblePeeps = 0     # able bodied people
    FoodGen = 0       # food generated
    Starvation = 0
    FamineCount = 0
    SpoiledCount = 0

    # What part of the peep Population can actually work?
    for key, attrib in Peeps.items():
        if attrib[pm.Age] >= pm.WorkAge:
            AblePeeps += 1

    # Take the generated food and add it to the FoodStore
    # NOTE: children & elderly should probably make less then
    #       20-55 year olds ?? some fraction ?? This isn't
    #       accounted for in the parms file or the program.
    FoodGen = int((AblePeeps * pm.WorkProduce))
    FoodStore += FoodGen

    # The planet has a natural food supply that is always available.
    # This check ensures there is a little bit of food to restart from
    # any disaster. Otherwise, this is not used by the Peeps but for
    # wildlife use.
    if FoodStore < pm.NaturalPlanetFood:
        FoodStore += pm.NaturalPlanetFood

    # Did we have a famine?
    if year > 50 and t.flip(pm.famine):
        FoodStore -= int(FoodStore * pm.Spoilage)
        FamineCount += 1
        if FoodStore < pm.NaturalPlanetFood:
            FoodStore = pm.NaturalPlanetFood

    # Note food is 1 unit per-person for an entire
    # year. So, if FoodStore drops below Population, so do the peeps
    if FoodStore < Population:
        starved = Population - FoodStore
        Starvation = calculate_death_range(starved)
        Population -= Starvation
        FoodStore -= Population
    else:
        FoodStore -= Population

    # check to see if the food in storage spoils
    if year > 50 and t.flip(pm.spoiled):
        FoodStore -= int(FoodStore * pm.Spoilage)
        SpoiledCount += 1
        if FoodStore < pm.NaturalPlanetFood:
            FoodStore = pm.NaturalPlanetFood

    # There is a maximum size to FoodStore; the parm file ProduceMaxStore is
    # based on Population. That way, we only store what is needed as overflow
    # for next year.

    if FoodStore > (Population * pm.ProduceMaxStore):
        FoodStore -= int(Population * pm.ProduceMaxStore)

    return FoodGen, Starvation, AblePeeps, FamineCount, SpoiledCount


def deadPool(year):
    '''
    The grim weeper comes a calling
    '''

    global EvePassed, AdamPassed, Population, longlife, life

    totalDeaths = 0
    naturalDeath = 0
    sicknessDeath = 0
    murderedDeath = 0
    delete_list = []

    # Death from old age and sickness
    for key, attrib in Peeps.items():
        if key == 1 and year > 953:     # When Adam dies source Bible
            delete_list.append(key)
            AdamPassed = 1
            totalDeaths += 1
            naturalDeath += 1
        elif key == 2 and year > 438:   # When Eve dies source Bible
            delete_list.append(key)
            EvePassed = 1
            naturalDeath += 1
            totalDeaths += 1
        elif key > 2 and attrib[pm.LongLifeSpan] == pm.Yes \
                and attrib[pm.Age] > longlife:
            delete_list.append(key)
            totalDeaths += 1
            naturalDeath += 1
        elif key > 2 and attrib[pm.LongLifeSpan] == pm.No \
                and attrib[pm.Age] > life:
            delete_list.append(key)
            totalDeaths += 1
            naturalDeath += 1
        elif key > 2 and attrib[pm.Sick] == pm.Yes and t.flip(pm.terminal):
            delete_list.append(key)
            sicknessDeath += 1
            totalDeaths += 1

    # If the kill flag is off (eq zero) then check the kill dna bit
    # of the top 5 persons that are old enough to murder
    # NOTE: I have not tried this piece of code yet
    # if pm.Killoff == 0:
    #     kage = (pm.Killage,)
    #     ksql = """SELECT Name FROM Peeps
    #                 WHERE BIT6 = 1
    #                 AND Age > ?
    #                 ORDER BY Age DESC
    #                 LIMIT 5 OFFSET 3
    #               """
    #     tb.execute(ksql, (kage))
    #     krows = tb.fetchall
    #     for k in range(len(krows)):
    #         if t.flip(pm.murder):
    #             tb.execute("""DELETE FROM Peeps
    #                         WHERE BIT7 = 1
    #                         AND Name NOT IN (1,2)
    #                         HAVING MAX(AGE)
    #                 """)
    #             murderedDeath += tb.rowcount
    #             totalDeaths += murderedDeath
    #             db.commit()

    for x in range(len(delete_list)):
        skipped = Peeps.pop(delete_list[x], True)
        if skipped:
            continue

    Population -= totalDeaths

    return totalDeaths, naturalDeath, sicknessDeath, murderedDeath


def lifeIsGood(LGyear):
    '''
    Control the circle of life for a giving year
    '''

    global FoodStore, life, longlife, EndBirth, StartBirth, BirthMiddleAge, Population, avgBR, avgDR

    # Additional fields for the simulator file used for analyses
    pregnantCNT = 0
    births = 0
    twins = 0
    miscnt = 0
    workers = 0
    FoodGen = 0
    starved = 0
    famine = 0
    deathrate = 0
    birthRate = 0
    SpoiledCount = 0

    # We process the year in this order; harvest food before checking
    # that any peep has died. Also, birthdays are done last so that they
    # don't die before their time

    # 1) Forage and process food
    FoodGen, starved, workers, famine, SpoiledCount = FieldOfDreams()

    # 2) Death is inevitable
    Tdeath, Ndeath, Sdeath, Mdeath = deadPool(year)

    # 3) Did we have an increase in Population and sleepless nights?
    births, twins, miscnt = withChild()

    # 4) Peeps getting pregnant
    pregnantCNT = LoveNThunder()

    # 5) Calculate birth rate
    if births > 0 and Population > 0:
        birthRate = (float(f'{((births / Population) * 100):.2f}'))
        avgBR.append(float(f'{birthRate:.2f}'))

    # 6) Calculate death rate
    if Tdeath > 0 and Population > 0:
        deathrate = (float(f'{((Tdeath / Population) * 100):.2f}'))
        avgDR.append(float(f'{deathrate:.2f}'))

    # 7) Everyone is a year older... Happy birthday!
    for key, attrib in Peeps.items():
        attrib[pm.Age] += 1
        Peeps.update({key: attrib})

    # every x years, the world gets a little... smarter ?
    # Bump up the numbers as the peeps progress through the years
    if not year % pm.LifeImprovements:
        longlife += pm.LifeExtended
        life += pm.LifeExtended
        # this is where Peepmanity gets smarter
        if StartBirth < pm.birthBeginMax:
            StartBirth += pm.LifeExtended
        if EndBirth < longlife:
            EndBirth += pm.LifeExtended
        if BirthMiddleAge < longlife:
            BirthMiddleAge += pm.LifeExtended

    # Print some outcomes for the year (epochs) so we know the program
    # is still running. NOTE that the lines
    # is writing in place
    print(
        f'''\r   Year {LGyear:,} Pop {Population:,} Deaths {Tdeath:,} Births {births:,} Foodstore {FoodStore:,}''', end='        \r')

    # Gather all counts for later analysis. This is a memory table
    world = ([LGyear, Population, workers, FoodStore, FoodGen, SpoiledCount, famine, births,
             twins, miscnt, birthRate, pregnantCNT, Tdeath, Ndeath, Sdeath, Mdeath, starved, deathrate])

    csvwriter.writerow(world)

    LGyear += 1

    return LGyear


def endStats():
    '''
    At the end of the simulation, get some stats from the database
    '''
    mpop = 0
    fpop = 0
    u11 = 0
    u21 = 0
    u31 = 0
    u41 = 0
    u51 = 0
    u61 = 0
    u71 = 0
    g70 = 0
    mag = 0
    age = 0

    dbpop = len(Peeps)

    for key, attrib in Peeps.items():
        age += attrib[pm.Age]
        if attrib[pm.Gender] == pm.Male:
            mpop += 1

        if attrib[pm.Gender] == pm.Female:
            fpop += 1

        if attrib[pm.Age] < 11:
            u11 += 1
        elif attrib[pm.Age] > 10 and attrib[pm.Age] < 21:
            u21 += 1
        elif attrib[pm.Age] > 20 and attrib[pm.Age] < 31:
            u31 += 1
        elif attrib[pm.Age] > 30 and attrib[pm.Age] < 41:
            u41 += 1
        elif attrib[pm.Age] > 40 and attrib[pm.Age] < 51:
            u51 += 1
        elif attrib[pm.Age] > 50 and attrib[pm.Age] < 61:
            u61 += 1
        elif attrib[pm.Age] > 60 and attrib[pm.Age] < 71:
            u71 += 1
        elif attrib[pm.Age] > 70:
            g70 += 1

        if attrib[pm.Married] == pm.Yes:
            mag += 1

    avgAge = int(age / len(Peeps))

    return dbpop, mpop, fpop, avgAge, u11, u21, u31, u41, u51, u61, u71, g70, mag


# ---------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------

# Start the elapse time; timmer
T = Timer(name=pm.PGMDescription)
T.start()

lines += f'\n>> {pm.PGMDescription} Simulating {pm.cycle} years.\n'

print(f'\n>> {pm.PGMDescription} Simulating {pm.cycle} years.')

# Setup the file name for later ploting
now = datetime.datetime.now()
filename = f'WorldSim4_Y{pm.cycle}_D{now.year}{now.month:02}{now.day:02}_H{now.hour:02}M{now.minute:02}.csv'

statsName = f'WorldStats4_Y{pm.cycle}_D{now.year}{now.month:02}{now.day:02}_H{now.hour:02}{now.minute:02}.txt'

PeepFileName = f'WorldPeeps4_Y{pm.cycle}_D{now.year}{now.month:02}{now.day:02}_H{now.hour:02}{now.minute:02}.py'

# Get the ball rolling
year = init()

# Main Loop

# Open and write yearly details column names to CSV
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields1)

    # Process loop
    while year < (pm.cycle + 1):
        year = lifeIsGood(year)

        # Terminate the program if all the peps died
        if Population < 1:
            warn = (
                f'\n\n\t>>> All Peeps have passed away. Population: {Population} <<<')
            print(tc.colored(warn, 'yellow', 'on_blue', ('bold', 'blink')))
            print(f'\n\t>>> Program Terminated Abnormaly <<<\n')
            sys.exit("\n\t>>> Fatel Error: That's all folks\n")

# End of simulation stats from the DB
pop, males, females, avg, under11, under21, under31, under41, under51, under61, under71, over70, married = endStats()

# Some calculations with the data
malePcent = str(f'{((males / pop) * 100):.2f}')
femalePcent = str(f'{((females / pop) * 100):.2f}')
marriedPcent = str(f'{((married / pop) * 100):.2f}')
u11Percent = str(f'{((under11 / pop) * 100):.2f}')
u21Percent = str(f'{((under21 / pop) * 100):.2f}')
u31Percent = str(f'{((under31 / pop) * 100):.2f}')
u41Percent = str(f'{((under41 / pop) * 100):.2f}')
u51Percent = str(f'{((under51 / pop) * 100):.2f}')
u61Percent = str(f'{((under61 / pop) * 100):.2f}')
u71Percent = str(f'{((under71 / pop) * 100):.2f}')
over70Percent = str(f'{((over70 / pop) * 100):.2f}')
adr = round(mean(avgDR), 2)
abr = round(mean(avgBR), 2)

Ptime = T.stop()

# Print this stuff out to the terminal and the file

lines += f'\n>> {pm.PGMDescription} End Statistics.'
lines += f'\n   World: {pop:,} Males: {males:,} ({malePcent}%) Females: {females:,} ({femalePcent}%)'
lines += f'\n   Average Death Rate: {adr}% Average Birth Rate: {abr}%'
lines += f'\n   Married: {married:,} ({marriedPcent}%) Avg Age: {avg:.2f}\n'
lines += f'\n\tAge 0-10:  {under11:>10,} ({u11Percent}%)\tAge 11-20: {under21:>10,} ({u21Percent}%)'
lines += f'\n\tAge 21-30: {under31:>10,} ({u31Percent}%)\tAge 31-40: {under41:>10,} ({u41Percent}%)'
lines += f'\n\tAge 41-50: {under51:>10,} ({u51Percent}%)\tAge 51-60: {under61:>10,} ({u61Percent}%)'
lines += f'\n\tAge 61-70: {under71:>10,} ({u71Percent}%)\tAge 70+:   {over70:>10,} ({over70Percent}%)\n'
lines += f'{Ptime}'

print(f'\n{lines}')

with open(statsName, 'w') as f:
    f.write(lines)
    f.close()

print('>> Details File created:', filename)
print('>> Stats File created:', statsName)
print(f'   {pm.PGMDescription} {pm.program} V{pm.version} Complete')
print("   A river in your derci! (Arrivederci, if ya didn't get it)")
print(' ')

print()
