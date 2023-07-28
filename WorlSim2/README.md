# Program: WSMain2.py Version '3.1.2023.03'

### *World simulation program. A constant evelution in code.*
\
**NOTE: Misspellings by siri.**

**NOTE: See `Peeps.sql` for database schema**

**Just** a project I though of doing and then modify as I get better at
writting python code. It all started with the question, can one populated the world with just two people starting out?

**There** has been three versions, V2 flopped, *I don't want to talk about it*. The issue I had with version 1 was throughput performace and memory usage. As the propulation grew, the program slowed down and then memory was used up. All peeps info was held in memory (I have 64g). I tried to go to 1,000 years, got to 2 billion peeps when it died, 31 hours later! I would like to go to 2,023 years and then 2025 and see how close to real numbers the simulation gets. Although, this simulated world is not like planet earth.

**Version 3** I added a sqlite3 database (*to solve the memory problem*),
added peeps DNA and fixed some of the events to be more radom. The DNA is also randomly built. I fixed or reworked the code to be more efficant, as best I can. 

However, it is still very slow. Adding the database is slow as the population grows; adding, deletting and updating records. I can't even run a 200 year test!

**Version 4** I removed the sqlite3 database, running to slow for practical use. I'm using a dictionary, whitch runs faster. However, I'm back to the memory issue. I took some memory tables out. Made a differance, still more work to be dome.

## World interactions  See WSparms4.py for more deatils about the planet environment.

---
The idea of this current world is that peeps works to the betterment of all peeps. Therefore, all peeps effort is food generation.

Food is procces into uints, a single unit feeds one peep for one year. The goal for the peeps is to have some percent of food units as surpules to be carried over to the next year. If the population plus 2% (`popultion * 1.02`) is greater than the number of food units, peeps die.

Famnime affects food units production as well as spoilage. Something I need to consider, as the population grows, so will the space needed for fields. More peeps, more homes needed, less space for feilds. Over population

*Murder has been added based on ones DNA. However, eventhough the code is in the program,
I have not tested it yet.*

## Addtions I want to impelment
---
- At this point, I have six DNA bits unassigned that I want to assign, just not sure what to use them for.

- I am planning on having war (riots) as part of the simulation, just not thought out all the details for war yet.

- I want to add natural disasters.

## Gaols
---

1) Efficant code. Still running really slow. I found out I had a few bugs as I restuctured the code. Now that these bugs are fixed, it runs slow again.

2) Better memory usage?

3) Better I/O for accsessing Peeps information? Differant database??

4) Get to year 2025

5) I would like to make a lot of
these functions into classes. But with the
database calls, I was getting errors. *Not even sure if making classes will make any differance.* One reason version 2 flopped is....**no... wait... I don't want to talk about it**.

6) Add AI componets to a Peep.
