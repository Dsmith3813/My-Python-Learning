# My attempt to make a world simulator. This package is still
# A work in progress. It runs, but not all the planned funtionality is
# represented.
# TheBigD Stared: 08/04/2021. Development continues.

import WSParms2 as pm       # Parameter file.
import WSPerson as cp       # Class to create a person.
import WSTools as t         # Tool class.
import sqlite3              # sqllit3 database.
import datetime
from statistics import mean
import os
import csv
from DJSTimer import Timer

os.system('Clear')

# Set global accumilators and parms. These are used to heal reduce
# the DB acces thru a single year.

population = 0          # program population
dbpop = 0               # Acuale population stored in the DB
year = 0                # In memory varable
EvePassed = 0           # Flags
AdemPassed = 0
foodstore = 0           # In memory storage contanir.
longlife = pm.LongLife  # From parm file stored for program use
life = pm.Life
sbirth = pm.Bbirth
ebirth = pm.Ebirth
mstart = pm.marstart
world = []              # Memory stor of the condition of the world
avgDR = []              # After a given cycle (epoch)
avgBR = []

print(f'\n >> World Simulation II {pm.program} V{pm.version}')


def init():
    '''
    Sets Program defaults and creats the first two persons
    residing in the world and stores the information in the Persons
    database table Peeps; Adem and Eve. Initional setings for
    Adem and Eve are stored in the parm file WSparms.py
    '''
    global population

    pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
        BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
        BITD, BITE, BITF = cp.person.adem()
    tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,Married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
               (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
    db.commit()

    pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
        BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
        BITD, BITE, BITF = cp.person.eve()
    tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,Married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
               (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
    db.commit()

    LGyear = 1
    population = 2

    return LGyear


def population_cnt():
    '''
    Determines the current size of the population from the DB
    '''
    tb.execute("SELECT COUNT (*) FROM Peeps")
    dbpop = tb.fetchone()
    x = dbpop[0]

    return x


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

    return pop, males, females, avg,   \
        under11, under21, under31, under41, under51,   \
        under61, under71, over70


def calculate_death_range():
    '''
    Calutate the death (delete) range by peeps name.
    The x_factors should be a factor less then 1. If not,
    use defaults. Note a persons name is Pnnnnn.
    '''

    global population

    # Init prams
    start_factor = .0001
    end_factor = .001

    # Gewt the minimum Pname
    sql1 = 'SELECT MIN(Name) FROM Peeps'
    tb.execute(sql1,)
    x = tb.fetchone()

    # Adam & Eve do not pass away using this funtion. See
    # function deadpool.
    if x[0] == 'Adam' or x[0] == 'Eve':
        x[0] = ('p5',)

    # Now calculate the starting Pname and ending Pname to delete
    xnum = int(' '.join([(x[0])[1:]]))
    s = f'P{str(xnum + int(round((population * start_factor),0)))}'
    e = f'P{str(xnum + int(round((population * end_factor),0)))}'

    # And off to heaven the go.
    DelSQL = 'DELETE FROM Peeps WHERE Name BETWEEN ? AND ?'
    tb.execute(DelSQL, (s, e))
    death_cnt = tb.rowcount

    db.commit()

    population -= death_cnt

    return death_cnt


def loveBoat():
    '''
    In this sumulation females and males get married to have kids.
    If this bothers you, delete these programs from your computer.
    More kids, more workers
    '''

    mcnt = 0
    mstart = (pm.marstart,)
    sheSaidYes = 0
    heSaidYes = 0

    # list of unmarried men
    m = '''SELECT Name, Age, BIT2, BIT3, BIT4 FROM Peeps
            WHERE Gender = 1
            AND Married = 0
            AND Age > ?
        '''
    tb.execute(m, (mstart))
    mrows = tb.fetchall()

    # list of unmarried females
    f = '''SELECT Name, Age, BIT2, BIT3, BIT4 FROM Peeps
            WHERE Gender = 0
            AND Married = 0
            AND Age > ?
        '''
    tb.execute(f, (mstart))
    frows = tb.fetchall()

    # Line them up at the high school dance
    hmales = len(mrows)
    hfemales = len(frows)

    # test the waters for the males looking for a female.
    # NOTE: Investigate using "zip" to process these two lists
    if hmales <= hfemales:
        for l1 in range(hmales):
            sheSaidYes = 0
            mname, mage, mb2, mb3, mb4 = mrows[l1]  # get a male
            fname, fage, fb2, fb3, fb4 = frows[l1]  # get a female

            herph = 0       # Pharamons
            hisph = 0

            # Calaculate how efective the females pharamons are on the guy
            if fb2 == 1 and fb3 == 1:
                herph = 3
            elif fb2 == 1:
                herph = 1
            elif fb3 == 1:
                herph = 2

            # and now the males.
            if mb2 == 1 and mb3 == 1:
                hisph = 3
            elif mb2 == 1:
                hisrph = 1
            elif mb3 == 1:
                hisph = 2

            # So, will this male pop the question?
            if mage < 31 and t.flip(.6) == True:
                if hisph >= herph and fb4 == 1:
                    sheSaidYes = 1
            else:
                if mage >= 31 and t.flip(.3) == True:
                    if hisph >= herph and fb4 == 1:
                        sheSaidYes = 1

        # Oh now the troubles start
        if sheSaidYes == 1:
            sql1 = '''UPDATE Peeps SET Married = 1 WHERE Name = ?'''
            sql2 = '''UPDATE Peeps SET Married = 1 WHERE Name = ?'''
            tb.execute(sql1, (mname,))
            tb.execute(sql2, (fname,))
            mcnt += 1
            db.commit()

    # test the waters for her
    if hmales <= hfemales:
        for l1 in range(hmales):
            heSaidYes = 0
            mname, mage, mb2, mb3, mb4 = mrows[l1]  # get a male
            fname, fage, fb2, fb3, fb4 = frows[l1]  # get a female

            herph = 0
            hisph = 0

            if fb2 == 1 and fb3 == 1:
                herph = 3
            elif fb2 == 1:
                herph = 1
            elif fb3 == 1:
                herph = 2

            if mb2 == 1 and mb3 == 1:
                hisph = 3
            elif mb2 == 1:
                hisrph = 1
            elif mb3 == 1:
                hisph = 2

            if fage < 31 and t.flip(.4) == True:
                if herph >= hisph and mb4 == 1:
                    heSaidYes = 1
            else:
                if fage >= 31 and t.flip(.6) == True:
                    if herph >= hisph and mb4 == 1:
                        heSaidYes = 1

        if heSaidYes == 1:
            sql1 = '''UPDATE Peeps SET Married = 1 WHERE Name = ?'''
            sql2 = '''UPDATE Peeps SET Married = 1 WHERE Name = ?'''
            tb.execute(sql1, (mname,))
            tb.execute(sql2, (fname,))
            mcnt += 1
            db.commit()

    return mcnt


def LoveNmariage():
    ''' 
    Get a list of eligable girls to see if they will become
    pregniet
    '''
    global sbirth, ebirth
    IPupd = 0
    IPprego = 0
    pcnt = 0

    # Process the mairried cuples first
    xbt = (sbirth, ebirth)  # Brithing range
    get_girls = '''SELECT Name, BIT5 FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 0
                    AND Married = 1
                    AND Age BETWEEN ? and ?'''

    tb.execute(get_girls, (xbt))
    frows = tb.fetchall()

    # Walk thru the list to see if this gal wants to get pregnint
    for i in range(len(frows)):
        IPname, BIT5 = frows[i]

        if BIT5 == 1:  # willing to mate
            if t.flip(pm.fertel) == True:
                IPprego = 1
                IPupd = 1

        # Update the person to be pregnint
        if IPupd == 1:
            UPD = '''UPDATE Peeps SET Prego = ? WHERE Name = ?'''
            bn = (IPprego, IPname)
            tb.execute(UPD, bn)
            IPupd = 0
            pcnt += 1
            db.commit()

   # Process fooling around and other such backseat misgivings
    WCbt = (sbirth, ebirth)
    get_girls = '''SELECT Name, BIT5 FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 0
                    AND Age BETWEEN ? and ?'''

    tb.execute(get_girls, (WCbt))
    frows = tb.fetchall()

    # Walk thru the list to see if this gal wants to get pregnint
    for i in range(len(frows)):
        IPname, BIT5 = frows[i]

        if BIT5 == 1:  # willing to mate
            if t.flip(pm.unfertel) == True:
                IPprego = 1
                IPupd = 1

        # Update the person to be pregnint
        if IPupd == 1:
            UPD = '''UPDATE Peeps SET Prego = ? WHERE Name = ?'''
            bn = (IPprego, IPname)
            tb.execute(UPD, bn)
            IPupd = 0
            pcnt += 1
            db.commit()

    return pcnt, IPprego, IPupd


def withChild():
    '''
    To determine if a pregnait female gives brith
    '''
    global ebirth, sbirth, population

    birthcnt = 0
    twcnt = 0
    get_girls = '''SELECT Name FROM Peeps
                    WHERE Gender = 0
                    AND Prego = 1
                    AND Age < ?
                '''
    tb.execute(get_girls, (ebirth,))
    rows = tb.fetchall()

    # Walk thru the list to see if this gal in fact does gives birth
    for i in range(len(rows)):
        if t.flip(pm.missc) == True:  # Misscaridge?
            WCprego = 0
        elif t.flip(pm.twin) == True:
            # Twins! Create the little buggers
            pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
                BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
                BITD, BITE, BITF = cp.person.createPerson()
            tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,Married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
                       (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
            db.commit()

            pname, pgender, page, pprego, pmarried, BIT0, BIT1, BIT2, \
                BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, \
                BITD, BITE, BITF = cp.person.createPerson()
            tb.execute('''
                   INSERT INTO Peeps(Name,Age,Gender,Prego,Married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                   INSERT INTO Peeps(Name,Age,Gender,Prego,Married,BIT0,BIT1,BIT2,BIT3,BIT4,BIT5,BIT6,BIT7,BIT8,BIT9,BITA,BITB,BITC,BITD,BITE,BITF) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ''',
                       (pname, page, pgender, pprego, pmarried, BIT0, BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8, BIT9, BITA, BITB, BITC, BITD, BITE, BITF))
            db.commit()
            population += 1
            birthcnt += 1

    return birthcnt, twcnt


def fieldofDreams():
    '''
    Determines the state of the food supply by calulate able bodied
    people to plant, grow and harvest the fields. In this simulation
    all pepoles live to help the whole population.
    '''

    global population, foodstore

    ablePersons = 0     # able bodied people
    foodGen = 0         # food generated
    stravation = 0
    fcnt = 0

    # What part of the population can actually work
    bt = (pm.workage, (pm.LongLife - 5))

    SEL_sql1 = "SELECT COUNT(*) FROM Peeps WHERE Age BETWEEN ? AND ?"
    tb.execute(SEL_sql1, (bt))
    ablePersons = tb.fetchone()

    foodGen = int((ablePersons[0] * pm.workperf))
    foodstore += foodGen

    if population > 10000:
        # Did we have a famine?
        if t.flip(pm.famine):
            foodstore -= int(foodstore * pm.spoilage)
            fcnt += 1
            if foodstore < 1:
                foodstore = 0

    # Note that the food is 1 unit per-person for an entire
    # year. So, if food drops below population, so do the people
    if population > 10000:
        if foodstore < population * pm.popup:
            stravation = calculate_death_range()  # Dose deletes
            population -= stravation
            foodstore -= population
        else:
            foodstore -= population
            if foodstore < 5:
                foodstore = 0

    return foodGen, stravation, int(ablePersons[0]), fcnt


def deadPool(year):
    '''
    The grim weeper comes a calling
    '''

    global EvePassed, AdemPassed, population

    Tdeaths = 0
    Ndeath = 0
    Sdeath = 0
    Mdeath = 0

    # Deal with normal life spand deaths
    lexp = (life,)
    oldage = '''DELETE FROM Peeps
                WHERE Age > ?
                AND BIT8 = 0
             '''
    tb.execute(oldage, (lexp))
    Tdeaths = Tdeaths + tb.rowcount
    Ndeath += tb.rowcount
    db.commit()

    # Now check on the folks with the long life gean
    lexp = (longlife,)
    oldage = '''DELETE FROM Peeps
                WHERE Age > ?
                AND BIT8 = 1
             '''
    tb.execute(oldage, (lexp))
    Tdeaths = Tdeaths + tb.rowcount
    Ndeath += tb.rowcount
    db.commit()

    # Getting terminal illness
    sick = '''SELECT Name FROM Peeps
                WHERE BIT9 = 1
             '''
    tb.execute(sick,)
    rows = tb.fetchall()

    # Does this person sercume to the illness?
    if len(rows) > 0:
        for i in range(len(rows)):
            if t.flip(pm.termill):
                name = rows[i]
                sql = 'DELETE FROM Peeps WHERE Name = ?'
                tb.execute(sql, (name))
                Tdeaths += 1
                Sdeath += 1
                db.commit()

    # When Eve dies source Bible
    if EvePassed == 0 and year > 438:
        tb.execute("DELETE FROM Peeps WHERE Name = 'Eve'")
        EvePassed = 1
        Tdeaths += 1
        Ndeath += 1
        db.commit

    # When adem dies source Bible
    if AdemPassed == 0 and year > 953:
        tb.execute("DELETE FROM Peeps WHERE Name = 'Adem'")
        AdemPassed = 1
        Tdeaths += 1
        Ndeath += 1
        db.commit()

    # If the kill flag is off (eq zero) then check the kill bit
    # of the top 5 persons that are old enough to murder
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
                            HAVING MAX(AGE)
                    """)
                Mdeath = tb.rowcount
                Tdeaths += Mdeath

    population -= Tdeaths

    return Tdeaths, Ndeath, Sdeath, Mdeath


def lifeIsGood(LGyear):
    '''
    Control the curcile of life for a giving year
    '''

    global life, longlife, ebirth, sbirth, mstart, population, avgBR, avgDR

    LGpcnt = 0
    LGbrths = 0
    LGable = 0
    LGable = 0
    LGmcnt = 0
    foodgen = 0
    LGstrav = 0
    LGfcnt = 0
    deathrate = 0
    brithRate = 0

    # Forage and process food
    foodgen, LGstrav, LGable, LGfcnt = fieldofDreams()

    # Everyone is a year older Happy birthday!
    tb.execute('UPDATE Peeps SET Age = Age + 1')
    db.commit

    LGbrths, twcnt = withChild()             # gave brith?
    LGmcnt = loveBoat()                      # cuples getting married?
    LGpcnt, IPprego, IPupd = LoveNmariage()  # cuples getting prenate?

    if LGbrths > 0:
        brithRate = ((LGbrths / population) * 100)
        avgBR.append(brithRate)

    Tdeath, Ndeath, Sdeath, Mdeath = deadPool(year)  # death is ineviable
    Tdeath += LGstrav

    if Tdeath > 0:
        deathrate = ((Tdeath / population) * 100)
        avgDR.append(deathrate)

    # every x years, the world gets a little... smarter ?
    # Bump up the numbers
    if not year % pm.LifeImprovment:
        longlife += pm.LifeExtended
        life += pm.LifeExtended
        # this is where Peepmanity gets smarter
        mstart += pm.LifeExtended
        if sbirth < 21:
            sbirth += pm.LifeExtended
        if ebirth < longlife:
            ebirth += pm.LifeExtended

    # Print some outcomes for the year
    print(f'''\r    Year: {LGyear:,} Pop: {population:,} Deaths: {Tdeath:,} Rate: {deathrate:.2f}% Briths {LGbrths:,} Rate {brithRate:.2f}%''', end='   \r')

    # Gather all counts for later analysis.
    world.append([LGyear, population, LGable, foodstore, foodgen, LGfcnt, LGbrths, brithRate,
                 twcnt, LGpcnt, IPprego, IPupd, Tdeath, Ndeath, deathrate, Sdeath, Mdeath, LGmcnt])

    LGyear += 1

    return LGyear

# ---------------------------------------------------------------------
#
# Main Program


# Start the elapse time; timmer
with Timer(name='World Simulator II'):
    # Set up the Peeps database tables
    db = sqlite3.connect('PersonDB.db')
    tb = db.cursor()
    print("    Open database successfull")
    tb.execute("DELETE From Peeps")
    db.commit()
    print('    Table cleared')
    print(f'\n >> Simulate {pm.cycle} years.')

    # Setup the file for later ploting
    now = datetime.datetime.now()
    filename = f'WorldSim_Y{pm.cycle}_DATA_D{now.year}{now.month}{now.day}_H{now.hour}M{now.minute}.csv'
    filename1 = filename

    year = init()

    while year < (pm.cycle + 1):
        year = lifeIsGood(year)

    # End of simulation stats
    pop, males, females, avg, under11, under21, under31, under41, under51, under61, under71, over70 = endStats()

    # Some calculations
    malePcent = str(f'{((males / pop) * 100):.2f}')
    femalePcent = str(f'{((females / pop) * 100):.2f}')
    adr = round(mean(avgDR), 2)
    abr = round(mean(avgBR), 2)

    # Print this stuff out.
    # NOTE: This probably should be a file.
    print(f'\n\n >> End Satistices.')
    print(
        f'    World: {pop:,} Males: {males:,} ({malePcent}%) Females: {females:,} ({femalePcent}%)')
    print(f'    Average Death Rate: {adr}% Average BR: {abr}%')
    print(f'\n\t\tAvg Age: {avg:.2f}')
    print(f'    Age 1-10:  {under11:,}\tAge 11-20: {under21:,}')
    print(f'    Age 20-30: {under31:,}\tAge 30-40: {under41:,}')
    print(f'    Age 40-50: {under51:,}\tAge 50-60: {under61:,}')
    print(f'    Age 60-70: {under71:,}\tAge 70+:   {over70:,}\n')

    db.close()

    # Reached the end of time, final data writes
    fields1 = ['Year', 'Population', 'AblB', 'FoodST', 'FoodG', 'FoodF', 'Births', 'Brate',
               'TWcnt', 'Pcnt', 'PGcnt', 'IPupd', 'Deaths', 'Natural', 'Drate', 'Stav', 'Murdr', 'Mcnt']

    # writing to csv file
    with open(filename1, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields1)
        csvwriter.writerows(world)

    print(' >> File created:', filename1)
    print(f' >> World Simulation II {pm.program} V{pm.version} Complete')
    print(' ')

print()
