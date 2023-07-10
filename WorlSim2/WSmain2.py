# My attempt to make a world simulator. This package is still
# A work in progress. It runs, but not all the planned functionality is
# represented... YET! NOTE See WSParms.py for more details.
#
# NOTE: My first program, so it probably isn't very good python coding.
# But, I can write a mean assembler program!
#
# TheBigD Started: 02/04/2022. Development continues.
# Copyright (c) 2023 Dennis J. Smith All Rights Reserved License: MIT

import WSParms2 as pm       # Parameter file.
import WSpeeps as cp        # Class to create a peep.
import WSTools as t         # Tool class.
import sqlite3              # sqllit3 database.
import datetime
import termcolor as tc
import os
import sys
import csv
from statistics import mean
from DJSTimer import Timer

os.system('Clear')

# Set global in memory accumulators and parms.
# NOTE Investigate make this a data class
population = 0          # program population
year = 0                # In memory variable
EvePassed = 0           # Flags
AdemPassed = 0
foodstore = 50          # In memory storage container.
longlife = pm.LongLife  # From parm file stored for program use
life = pm.AvgLife
sbirth = pm.brithBegin
ebirth = pm.brithEnd
marrageAge = pm.marrageBegin
world = []              # Memory stor of the condition of the world file
avgDR = []              # After a given cycle (epoch)
avgBR = []

print(f'\n>> World Simulation II {pm.program} V{pm.version}')


def init():
    '''
    Sets Program defaults and creates the first two peeps
    residing in the world and stores the information in the Peeps
    database table Peeps; Adam and Eve. Initial settings for
    Adam and Eve are stored in the parm file WSparms.py
    '''
    global population

    pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
        BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
        BITD, BITE, BITF = cp.person.adam()

    tb.execute('''
                INSERT INTO Peeps(Name,Age,Gender,Prego,married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ''',
               (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
    db.commit()

    pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
        BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
        BITD, BITE, BITF = cp.person.eve()

    tb.execute('''
                INSERT INTO Peeps(Name,Age,Gender,Prego,married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ''',
               (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
    db.commit()

    LGyear = 1
    population = 2

    return LGyear


def population_cnt():
    '''
    Determines the current size of the population from the DB
    Created because the program accumulator was not being updated
    correctly
    '''
    tb.execute("SELECT COUNT (*) FROM Peeps")
    dbpop = tb.fetchone()
    x = int(dbpop[0])

    return x


def calculate_death_range(starved):
    '''
    Calculate the death (deletes) range by peeps name.
    The x_factors should be a factor less then 1.

    NOTE a peeps name is Pnnnnn. This function is called as it 
    has been determined death range was the outcome
    '''

    global population, year

    # if year > 20:    No clue what this is here
    #     return 0

    # Init prams
    start_factor = .001
    end_factor = .001

    # Get the minimum Pname
    sql1 = 'SELECT MIN(Name) FROM Peeps WHERE Name NOT IN ("Adam","Eve")'
    tb.execute(sql1,)
    x = tb.fetchone()

    # Calculate the starting Pname and ending Pname to delete
    xnum = int(' '.join([(x[0])[1:]]))
    s = f'P{xnum + int(starved * start_factor)}'
    e = f'P{xnum + int(starved * end_factor)}'

    # And off to heaven they go.
    DelSQL = 'DELETE FROM Peeps WHERE Name BETWEEN ? AND ? and Name NOT IN ("Adam","Eve")'
    tb.execute(DelSQL, (s, e))
    death_cnt = tb.rowcount

    db.commit()

    population -= death_cnt

    return death_cnt


def loveBoat():
    '''
    In this simulation females and males get married to have kids. Sorry if this  may bother some folks. The more kids, The more workers per family unit to work the fields. No other reason.
    '''

    marg = 0
    mstart = (pm.marrageBegin,)

    # list of unmarried peeps
    m = '''SELECT Name, Gender, Age, BIT0, BIT2, BIT3, BIT4 FROM Peeps
            WHERE married = 0
            AND Age > ?
        '''
    tb.execute(m, (mstart))
    rows = tb.fetchall()
    d = len(rows)
    mrows = []
    frows = []

    # Split out the boys from the girls
    for x in range(len(rows)):
        if rows[x][1] == 1:
            mrows += rows
        else:
            frows += rows

    # Pull out the returned columns and process
    for males, females in zip(mrows, frows):
        mname, mgen, mage, mb0, mb2, mb3, mb4 = males
        fname, fgen, fage, fb0, fb2, fb3, fb4 = females

        sheSaidYes = 0
        heSaidYes = 0

        # Calculate pheromone effectiveness the higher the number the
        # stronger the pheromone. If both DNA bits 2 & 3 on, then phara
        # is 3, else if bit 3 is on, then 2 else 1
        if (fb2 + fb3) == 2:    # Her pheromone
            herph = 3
        elif fb3 == 1:
            herph = 2
        else:
            herph = fb2

        if (mb2 + mb3) == 2:    # His pheromone
            hisph = 3
        elif mb3 == 1:
            hisph = 2
        else:
            hisph = mb2

        # Determine if the male proposes
        if (mage < 35 and t.flip(pm.marprob21)) or    \
                (mage <= 45 and t.flip(pm.marprob31)):
            if hisph >= herph and mb4 == 1:
                sheSaidYes = 1

        # Determine if the female proposes
        if (fage < 35 and t.flip(pm.marprob21)) or    \
                (fage <= 45 and t.flip(pm.marprob31)):
            if herph >= hisph and fb4 == 1:
                heSaidYes = 1

        # Oh now the troubles starts
        if sheSaidYes or heSaidYes:
            sql1 = '''UPDATE Peeps SET married = 1 WHERE Name = ?'''
            sql2 = '''UPDATE Peeps SET married = 1 WHERE Name = ?'''
            tb.execute(sql1, (mname,))
            tb.execute(sql2, (fname,))
            marg += 1
            db.commit()

    return marg


def LoveNthunder():
    ''' 
    Get a list of eligible girls to see if they are willing to become
    pregnant
    '''
    global sbirth, ebirth
    brithRange = (sbirth, ebirth)
    pregnent = 1
    pregCount = 0

    # Process the mairried cuples first
    pregnantGals = '''SELECT Name, BIT5 FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 0
                    AND married = 1
                    AND Age BETWEEN ? and ?'''
    tb.execute(pregnantGals, (brithRange))
    frows = tb.fetchall()

    # if peeps are married, they want kids... right?
    for i in range(len(frows)):
        if t.flip(pm.fertel) == True:
            IPname, BIT5 = frows[i]
            UPD = '''UPDATE Peeps SET Prego = ? WHERE Name = ?'''
            bun = (pregnent, IPname)
            tb.execute(UPD, bun)
            pregCount += 1
            db.commit()

   # Process peeps fooling around and other such backseat misgivings
    pregnantGals = '''SELECT Name, BIT5 FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 0
                    AND Age BETWEEN ? and ?'''
    tb.execute(pregnantGals, (brithRange))
    frows = tb.fetchall()

    # Walk thru the list to see if this peep wants to get pregnant
    for i in range(len(frows)):
        IPname, BIT5 = frows[i]
        if BIT5 == 1 and t.flip(pm.lessFertal) == True:
            # Update lady peep to be pregnint
            UPD = '''UPDATE Peeps SET Prego = ? WHERE Name = ?'''
            bun = (pregnent, IPname)
            tb.execute(UPD, bun)
            pregCount += 1
            db.commit()

    return pregCount


def withChild():
    '''
    To determine if a pregnant female gives brith
    '''
    global ebirth, sbirth, population

    birthcnt = 0
    twcnt = 0
    pregnantGals = '''
                    SELECT Name FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 1
                   '''
    tb.execute(pregnantGals,)
    rows = tb.fetchall()

    # Walk thru the list to see if this peep is infact giveing birth
    for i in range(len(rows)):
        if t.flip(pm.missCarrage) == True:  # Misscaridge?
            IPname = rows[i]
            UPD = '''UPDATE Peeps SET Prego = 0 WHERE Name = ?'''
            tb.execute(UPD, IPname)
            db.commit()
        elif t.flip(pm.twins) == True:
            # Twins! Create the little buggers
            pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
                BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
                BITD, BITE, BITF = cp.person.createPerson()
            tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
                       (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
            db.commit()

            pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
                BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
                BITD, BITE, BITF = cp.person.createPerson()
            tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
                       (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
            db.commit()
            population += 2
            birthcnt += 2
            twcnt += 1
        else:
            # Yah... the cute little bambino
            pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
                BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
                BITD, BITE, BITF = cp.person.createPerson()
            tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
                       (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
            db.commit()
            population += 1
            birthcnt += 1

    return birthcnt, twcnt


def fieldofDreams():
    '''
    Determines the state of the food supply by calulatting able
    bodied peeps to plant, grow and harvest the fields. In this 
    simulation all peeps live to help the whole population.
    '''

    global population, foodstore

    ablePeeps = 0     # able bodied people
    foodGen = 0       # food generated
    stravation = 0
    famineCount = 0

    # What part of the peep population can actually work?
    bt = (pm.workage, (pm.LongLife - 5))
    SEL_sql1 = "SELECT COUNT(*) FROM Peeps WHERE Age BETWEEN ? AND ?"
    tb.execute(SEL_sql1, (bt))
    ablePeeps = tb.fetchone()
    ablePeeps = ablePeeps[0]    # make it a number not a tupel

    # Take the generated food and add it to the foodstore
    # NOTE: children & elderly should probably make less then
    #       20-55 year olds ?? some fraction ?? This isn't
    #       accounted for in the parms file or the program.
    foodGen = int((ablePeeps * pm.workperf))
    foodstore += foodGen

    # Did we have a famine?
    if t.flip(pm.famine):
        foodstore -= int(foodstore * pm.spoilage)
        famineCount += 1
        if foodstore < 1:
            foodstore = 0

    # Note food is 1 unit per-person for an entire
    # year. So, if foodstore drops below population, so do the peeps
    if foodstore < (population * pm.foodpop):
        starved = population - foodstore
        stravation = calculate_death_range(starved)
        population -= stravation
        foodstore -= population
    else:
        foodstore -= population

    if foodstore < 1:
        foodstore = 0

    return foodGen, stravation, ablePeeps, famineCount


def deadPool(year):
    '''
    The grim weeper comes a calling
    '''

    global EvePassed, AdemPassed, population

    totalDeaths = 0
    naturalDeath = 0
    sicknessDeath = 0
    murderedDeath = 0

    # Deal with normal life exspectsy spand deaths
    lifeExpectancy = (life,)
    oldage = '''
             DELETE FROM Peeps
             WHERE Age > ?
             AND BIT8 = 0 AND Name NOT IN ("Adam","Eve")
             '''
    tb.execute(oldage, lifeExpectancy)
    totalDeaths += tb.rowcount
    naturalDeath += tb.rowcount
    db.commit()

    # Now check on the folks with the long life gean
    lifeExpectancy = (longlife,)
    oldage = '''
             DELETE FROM Peeps
             WHERE Age > ?
             AND BIT8 = 1 AND Name NOT IN ("Adam","Eve")
             '''
    tb.execute(oldage, lifeExpectancy)
    totalDeaths += tb.rowcount
    naturalDeath += tb.rowcount
    db.commit()

    # Dealing with terminal illness
    sick = '''
           SELECT Name FROM Peeps
           WHERE BIT9 = 1 AND Name NOT IN ("Adam","Eve")
           '''
    tb.execute(sick,)
    rows = tb.fetchall()

    # Does this person sercume to their illness?
    if len(rows) > 0:
        for i in range(len(rows)):
            if t.flip(pm.terminal):
                name = rows[i]
                sql = 'DELETE FROM Peeps WHERE Name = ?'
                tb.execute(sql, (name))
                totalDeaths += 1
                sicknessDeath += 1
                db.commit()

    # When Eve dies source Bible
    if EvePassed == 0 and year > 438:
        tb.execute("DELETE FROM Peeps WHERE Name = 'Eve'")
        EvePassed = 1
        totalDeaths += 1
        naturalDeath += 1
        db.commit

    # When adem dies source Bible
    if AdemPassed == 0 and year > 953:
        tb.execute("DELETE FROM Peeps WHERE Name = 'Adem'")
        AdemPassed = 1
        totalDeaths += 1
        naturalDeath += 1
        db.commit()

    # If the kill flag is off (eq zero) then check the kill dna bit
    # of the top 5 persons that are old enough to murder
    # NOTE: I have not tried this piece of code yet
    if pm.Killoff == 0:
        kage = (pm.Killage,)
        ksql = """SELECT Name FROM Peeps
                    WHERE BIT6 = 1
                    AND Age > ?
                    ORDER BY Age DESC
                    LIMIT 5 OFFSET 3
                  """
        tb.execute(ksql, (kage))
        krows = tb.fetchall
        db.commit
        for k in range(len(krows)):
            if t.flip(pm.murder):
                tb.execute("""DELETE FROM Peeps
                            WHERE BIT7 = 1
                            AND Name NOT IN ("Adam","Eve")
                            HAVING MAX(AGE)
                    """)
                murderedDeath += tb.rowcount
                totalDeaths += murderedDeath

    population -= totalDeaths

    return totalDeaths, naturalDeath, sicknessDeath, murderedDeath


def lifeIsGood(LGyear):
    '''
    Control the circle of life for a giving year
    '''

    global life, longlife, ebirth, sbirth, marrageAge, population, avgBR, avgDR

    # Additional fields for the simulator file used for analises
    pregnatCNT = 0
    births = 0
    twins = 0
    workers = 0
    married = 0
    foodgen = 0
    starved = 0
    famine = 0
    deathrate = 0
    brithRate = 0

    # We process the year in this order; harvest food before checking
    # that any peep has died. Also, birthdays are done last so that they
    # don't die before their time

    # 1) Forage and process food
    foodgen, starved, workers, famine = fieldofDreams()

    # 2) Death is ineviable
    Tdeath, Ndeath, Sdeath, Mdeath = deadPool(year)

    # 3) Did we have an increase in population and sleepless nights?
    births, twins = withChild()

    # 4) Peeps falling in love
    married = loveBoat()

    # 5) Peeps getting pregnant
    pregnatCNT = LoveNthunder()

    # 6) Claculate brith rate
    if births > 0 and population > 0:
        brithRate = (float(f'{((births / population) * 100):.2f}'))
        avgBR.append(float(f'{brithRate:.2f}'))

    # 7) Calculate death rate
    if Tdeath > 0 and population > 0:
        deathrate = (float(f'{((Tdeath / population) * 100):.2f}'))
        avgDR.append(float(f'{deathrate:.2f}'))

    # 8) Everyone is a year older... Happy birthday!
    tb.execute('UPDATE Peeps SET Age = Age + 1')
    db.commit

    # every x years, the world gets a little... smarter ?
    # Bump up the numbers as the peeps progress through the years
    if not year % pm.LifeImprovment:
        longlife += pm.LifeExtended
        life += pm.LifeExtended
        # this is where Peepmanity gets smarter
        marrageAge += pm.LifeExtended
        if sbirth < 21:
            sbirth += pm.LifeExtended
        if ebirth < longlife:
            ebirth += pm.LifeExtended

    # Print some outcomes for the year (epochs) so we know the program
    # is still running. NOTE that the line is writting in place
    print(f'''\r   Year {LGyear:,} Pop {population:,} Deaths {Tdeath:,} Rate {deathrate:.2f}% Briths {births:,} Rate {brithRate:.2f}% Foodstore {foodstore:,}''', end='   \r')

    # Gather all counts for later analysis. This is a memory table
    world.append([LGyear, population, workers, foodstore, foodgen, famine, starved, births,
                 twins, brithRate, pregnatCNT, Tdeath, Ndeath, Sdeath, Mdeath, deathrate, married])

    LGyear += 1

    return LGyear


def endStats():
    '''
    At the end of the simulation, get some stats from the database
    '''

    tb.execute("SELECT COUNT(*) FROM Peeps")
    dbpop = tb.fetchone()
    tb.execute("SELECT COUNT(*) FROM Peeps where Gender = 1")
    mpop = tb.fetchone()
    tb.execute("SELECT COUNT(*) FROM Peeps where Gender = 0")
    fpop = tb.fetchone()
    tb.execute('SELECT AVG(Age) FROM Peeps')
    avgAge = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age < 11')
    u11 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 10 and Age < 21')
    u21 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 20 and Age < 31')
    u31 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 30 and Age < 41')
    u41 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 40 and Age < 51')
    u51 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 50 and Age < 61')
    u61 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 60 and Age < 71')
    u71 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Age > 70')
    g70 = tb.fetchone()
    tb.execute('SELECT COUNT(*) FROM Peeps where Married = 1')
    mag = tb.fetchone()

    pop = dbpop[0]
    males = mpop[0]
    females = fpop[0]
    avg = avgAge[0]
    under11 = u11[0]
    under21 = u21[0]
    under31 = u31[0]
    under41 = u41[0]
    under51 = u51[0]
    under61 = u61[0]
    under71 = u71[0]
    over70 = g70[0]
    marg = mag[0]

    return pop, males, females, avg, under11, under21, \
        under31, under41, under51, under61, under71, over70, marg


# ---------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------

# Start the elapse time; timmer
with Timer(name='World Simulator II'):

    # Set up the Peeps database tables
    db = sqlite3.connect('PeepsDB.db')
    tb = db.cursor()
    print("   Open database successfull")
    tb.execute("DELETE From Peeps")
    db.commit()
    print('   Table cleared')
    print(f'\n>> Simulate {pm.cycle} years.')

    # Setup the file name for later ploting
    now = datetime.datetime.now()
    filename = f'WorldSim_Y{pm.cycle}_D{now.year}{now.month:02}{now.day:02}_H{now.hour:02}M{now.minute:02}.csv'

    statsName = f'WorldStats_Y{pm.cycle}_D{now.year}{now.month:02}{now.day:02}_H{now.hour:02}{now.minute:02}.txt'

    # Get the ball rolling
    year = init()

    # Main Loop
    while year < (pm.cycle + 1):
        year = lifeIsGood(year)

        # Terminate the program if all the peps died
        if population < 1:
            warn = (
                f'\n\n\t>>> All Peeps have passed away. Population: {population} <<<')
            print(tc.colored(warn, 'yellow', 'on_blue', ('bold', 'blink')))
            print(f'\n\t>>> Program Terminated Abnormaly <<<\n')
            sys.exit("\n\t>>> Fatel Error: That's all folks\n")
        else:
            population = population_cnt()

    # End of simulation stats from the DB
    pop, males, females, avg, under11, under21, under31, under41, under51, under61, under71, over70, married = endStats()

    # Some calculations with the data
    malePcent = str(f'{((males / pop) * 100):.2f}')
    femalePcent = str(f'{((females / pop) * 100):.2f}')
    marriedPcent = str(f'{((married / pop) * 100):.2f}')
    adr = round(mean(avgDR), 2)
    abr = round(mean(avgBR), 2)

    # Print this stuff out to the terminal
    # NOTE: This probably should be a txt file. It is now.
    line = ''
    line += f'\n\n>> End Satistices.'
    line += f'\n   World: {pop:,} Males: {males:,} ({malePcent}%) Females: {females:,} ({femalePcent}%)'
    line += f'\n   Average Death Rate: {adr}% Average Birth Rate: {abr}%'
    line += f'\n   Married: {married:,} ({marriedPcent}%) Avg Age: {avg:.2f}\n'
    line += f'\n\tAge 1-10:  {under11:>9,}\tAge 11-20: {under21:>9,}'
    line += f'\n\tAge 20-30: {under31:>9,}\tAge 30-40: {under41:>9,}'
    line += f'\n\tAge 40-50: {under51:>9,}\tAge 50-60: {under61:>9,}'
    line += f'\n\tAge 60-70: {under71:>9,}\tAge 70+:   {over70:>9,}\n'

    print(line)

    db.close()

    with open(statsName, 'w') as f:
        f.write(line)
        f.close()

    # Reached the end of time, final data writes: CSV Fields
    fields1 = ['Year', 'Population', 'Workers', 'Food Store', 'Food Generated',
               'Famine', 'Starved', 'Births', 'Twins', 'Birth Rate',
               'Pergnat CNT', 'Deaths', 'Natural', 'Sickness', 'Merdured', 'Married']

    # writing to csv file
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields1)
        csvwriter.writerows(world)

    print('>> Details File created:', filename)
    print('>> Stats File created:', statsName)
    print(f'   World Simulation II {pm.program} V{pm.version} Complete')
    print("   A river in your derci! (Arrivederci, if ya didn't get it)")
    print(' ')

print()
