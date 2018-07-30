import json

setNames = [
    'Antiquities',
    'Fallen Empires',
    'Legends',
    'Arabian Nights',
    'Homelands',
    'The Dark'
]

setToCards = {}

for sn in setNames:
    with open(sn + '.tsv', 'r') as f:
        contents = f.read()

    cards = []

    lines = contents.split('\r\n')
    for l in lines:
        cardName = l.split('\t')[0]
        rarity   = l.split('\t')[1]

        cards.append({
            'name': cardName,
            'rarity': rarity
        })

    setToCards[sn] = cards

with open('Old Rarities.json', 'w') as f:
    f.write(json.dumps(setToCards))

# for sn in setToCards:
#     cards = setToCards[sn]

#     with open(sn + '.json', 'w') as f:
#         f.write(json.dumps(cards))

