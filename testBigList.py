
from main import *

names = [
    "Chalice of the Void",
    "Doubling Season",
    "Engineered Explosives",
    "Arcbound Ravager",
    "Aether Vial",
    "Pact of Negation",
    "Cryptic Command",
    "Blood Moon",
    "Academy Ruins",
    "Maelstrom Pulse",
    "Tooth and Nail",
    "Summoner's Pact",
    "Glimmervoid",
    "Life from the Loam",
    "Glen Elendra Archmage",
    "Kira, Great Glass-Spinner",
    "Ethersworn Canonist",
    "Sarkhan Val",
    "Lotus Bloom",
    "Woodfall Primus",
    "Gifts Ungiven",
    "Bridge from Below",
    "Knight of the Reliquary",
    "Grand Arbiter Augustin IV",
    "Stonehewer Giant",
    "City of Brass",
    "Angel's Grace",
    "Blinkmoth Nexus",
    "Slaughter Pact",
    "Extirpate",
    "Oona, Queen of the Fae",
    "Greater Gargadon",
    "Chalice of the Void",
    "Doubling Season",
    "Engineered Explosives",
    "Arcbound Ravager",
    "Aether Vial",
    "Pact of Negation",
    "Cryptic Command",
    "Blood Moon",
    "Academy Ruins",
    "Maelstrom Pulse",
    "Tooth and Nail",
    "Summoner's Pact",
    "Glimmervoid",
    "Life from the Loam",
    "Glen Elendra Archmage",
    "Kira, Great Glass-Spinner",
    "Ethersworn Canonist",
    "Sarkhan Val",
    "Lotus Bloom",
    "Woodfall Primus",
    "Gifts Ungiven",
    "Bridge from Below",
    "Knight of the Reliquary",
    "Grand Arbiter Augustin IV",
    "Stonehewer Giant",
    "City of Brass",
    "Angel's Grace",
    "Blinkmoth Nexus",
    "Slaughter Pact",
    "Extirpate",
    "Oona, Queen of the Fae",
    "Greater Gargadon",
    "Chalice of the Void",
    "Doubling Season",
    "Engineered Explosives",
    "Arcbound Ravager",
    "Aether Vial",
    "Pact of Negation",
    "Cryptic Command",
    "Blood Moon",
    "Academy Ruins",
    "Maelstrom Pulse",
    "Tooth and Nail",
    "Summoner's Pact",
    "Glimmervoid",
    "Life from the Loam",
    "Glen Elendra Archmage",
    "Kira, Great Glass-Spinner",
    "Ethersworn Canonist",
    "Sarkhan Val",
    "Lotus Bloom",
    "Woodfall Primus",
    "Gifts Ungiven",
    "Bridge from Below",
    "Knight of the Reliquary",
    "Grand Arbiter Augustin IV",
    "Stonehewer Giant",
    "City of Brass",
    "Angel's Grace",
    "Blinkmoth Nexus",
    "Slaughter Pact",
    "Extirpate",
    "Oona, Queen of the Fae",
    "Greater Gargadon"
]

allPrices = []

threads = []
i = -1
for n in names:
    i += 1

    # Instantiate everything in the output
    allPrices.append(0.0)

    # card, isFoil, removes, tIndex, out
    arguments = (n, True, [], i, allPrices)
    t = threading.Thread(target=getMedian, args=arguments)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print('Prices:')
for p in allPrices:
    print(p)