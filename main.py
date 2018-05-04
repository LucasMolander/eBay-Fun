"""
This file is for proofs of concept for different parts of the overall program.
    - Getting web requests to work
    - Calculating minimums/maximums of functions
    - Etc.
"""

"""
General notes:
    - How to identify a card in Yugioh:
        * ID

    - How to identify a card in MTG:
        * Name and Set

    - Determinants of price:
        * Foil
        * Grade
        * Condition (might only be in item description)
        * Multiplicity
        * Common alterations (e.g. "Altered art")
"""



from find_prices import reportMTGBox

reportMTGBox('Expansions', 'Dominaria.txt')




# #
# # Get a report for each of these expansions and write them to a file.
# #
# expansions = [
#     'Amonkhet',
#     'Eternal Masters',
#     'Hour of Devastation',
#     'Iconic Masters',
#     'Innistrad',
#     'Ixalan',
#     'Modern Masters 2013',
#     'Modern Masters 2015',
#     'Modern Masters 2017',
#     'Rise of the Eldrazi',
#     'Shadows Over Innistrad',
#     'Worldwake',
#     'Zendikar'
# ]

# expectedValues = []

# for e in expansions:
#     ev = reportMTGBox('Expansions', e + '.txt')
#     expectedValues.append(ev)

# outFile = open('Expected Values/01.01.2018.txt', 'w')

# for i in range(0, len(expansions)):
#     outFile.write(expansions[i]+':\t'+str(round(expectedValues[i], 2))+'\n')

# outFile.close()

