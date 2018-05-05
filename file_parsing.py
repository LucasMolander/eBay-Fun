def parseExpansionFile(pathToFile):
    with open(pathToFile, 'r') as inFile:
        rawContents = inFile.read().split('\n')

    # Get some basic info from the top of the file
    setName = rawContents[0]
    packsPerBox = int(rawContents[1])
    pFoil = float(rawContents[2])

    nMythics = int(rawContents[3])
    nRares = int(rawContents[4])
    nUncommons = int(rawContents[5])
    nCommons = int(rawContents[6])
    nAll = nMythics + nRares + nUncommons + nCommons

    # Get indices for the cards
    mStart = 8
    mEnd = rawContents.index('RARES') - 1

    rStart = mEnd + 2
    rEnd = rawContents.index('UNCOMMONS') - 1

    uStart = rEnd + 2
    uEnd = rawContents.index('COMMONS') - 1

    cStart = uEnd + 2
    cEnd = len(rawContents) - 1

    # Assign the cards
    mythicNames = []
    rareNames = []
    uncommonNames = []
    commonNames = []
    allNames = [] # Nice for multithreading

    for i in range(mStart, mEnd + 1):
        mythicNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(rStart, rEnd + 1):
        rareNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(uStart, uEnd + 1):
        uncommonNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(cStart, cEnd + 1):
        commonNames.append(rawContents[i])
        allNames.append(rawContents[i])

    # Return the variables in a dictionary
    out = {
        'setName': setName,
        'packsPerBox': packsPerBox,
        'pFoil': pFoil,
        'nMythics': nMythics,
        'nRares': nRares,
        'nUncommons': nUncommons,
        'nCommons': nCommons,
        'nAll': nAll,
        'mythicNames': mythicNames,
        'rareNames': rareNames,
        'uncommonNames': uncommonNames,
        'commonNames': commonNames,
        'allNames': allNames
    }

    return out
