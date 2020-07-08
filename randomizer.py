#!/usr/bin/env python3
import json
from random import randint


#----------------------------------------------------------
#Method for making sure all information is valid
#The HTML code should handle most of the info validation, but we double check because better safe than sorry
#Returns an error message, or the deck size
#----------------------------------------------------------
def verifyInformation(normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands):

    #Make sure the user percentages total 1 and there are no negative values
    for x in range(len(normal_rarity_percents)):
        if normal_rarity_percents[x] < 0:
            return("Error! Negative value detected for normal rarity decimals")
        if commander_rarity_percents[x] < 0:
            return("Error! Negative value detected for commander rarity decimals")
        if land_rarity_percents[x] < 0:
            return("Error! Negative value detected for land rarity decimals")
    if sum(normal_rarity_percents) != 1:
        return("Error! Normal rarity decimals dont equal 1")
    if sum(commander_rarity_percents) != 1:
        return("Error! Commander rarity decimals dont equal 1")
    if sum(land_rarity_percents) != 1:
        return("Error! Land rarity decimals dont equal 1")

    #Makes sure artifact percentage is 0<x<1
    if artifact_percent > 1 or artifact_percent < 0:
        return("Error! Artifact percentage decimal isnt between 0 and 1")

    #Makes sure basic lands percentage is 0<x<1
    if basic_land_percent > 1 or basic_land_percent < 0:
        return("Error! Basic land percentage decimal isnt between 0 and 1")

    #Makes sure basic lands removal percentage is 0<x<1
    if basic_land_percent_removal > 1 or basic_land_percent_removal < 0:
        return("Error! Basic land removal percentage decimal isnt between 0 and 1")

    #Make sure the deck mode is supported
    if deck_mode != "brawl" and deck_mode != "standard":
        return("Error! Unsupported deck mode! Current options are brawl and standard")
    
    #Set the deck size
    deck_size = 0
    if deck_mode == "brawl" or deck_mode == "standard":
        deck_size = 60

    #Make sure the number of lands is valid
    if min_lands > max_lands:
        return("Error! Minimum lands must be less than or equal too maximum lands")
    if max_lands > deck_size:
        return("Error! Maximum lands must be less than or equal too the maximum deck size")

    return deck_size
#----------------------------------------------------------

#----------------------------------------------------------
#Method for picking a card
#----------------------------------------------------------
def pick_a_card(manaCost, name, types, rarityPercents, deckCMC, deck, flag, artifact_percent, basic_land_percent):
     
    #For lands, we need to pass in the color of the land as the manaCost
    landColors = []
    if flag == 1:
        landColors = manaCost
        manaCost = []

    #See if you are picking a basic land
    if manaCost == [] and types == [] and randint(0, 100) < 100*basic_land_percent:

        #Calculate the range for each basic land type
        basic_land_range = [[], [], [], [], []]
        total = 0
        for x in range(len(basic_land_range)):
            if deckCMC[x] > 0:
                basic_land_range[x] = [total, deckCMC[x] + total]
                total = total + deckCMC[x]
            else:
                basic_land_range[x] = [-1, -1]

        #If we get a colorless deck, basic lands are islands
        if total == 0:
            deckCMC[3] = 1
            total = 1
            basic_land_range[3][0] = 0
            basic_land_range[3][0] = 0

        #Randomly select a basic land, and since we dont use deckCMC, we can start subtracting from here to reflect lands
        #However, if the deckCMC is 1, dont subtract to allow for more basics to be added
        basicLands = ["Mountain", "Plains", "Swamp", "Island", "Forest"]
        randomBasic = randint(0, total - 1)
        for x in range(len(basicLands)):
            if randomBasic >= basic_land_range[x][0] and randomBasic <= basic_land_range[x][1]:
                deck.append(basicLands[x])
                if deckCMC[x] != 1 and deckCMC[x] != 0:
                    deckCMC[x] = deckCMC[x] - 1
                break
        return deck, deckCMC

    #Set up rarity ranges
    common = [0, (rarityPercents[0] * 100) - 1]
    uncommon = [(rarityPercents[0] * 100), (rarityPercents[0] * 100) + (rarityPercents[1] * 100) - 1]
    rare = [(rarityPercents[0] * 100) + (rarityPercents[1] * 100), (rarityPercents[0] * 100) + (rarityPercents[1] * 100) + (rarityPercents[2] * 100) - 1]
    mythic = [(rarityPercents[0] * 100) + (rarityPercents[1] * 100) + (rarityPercents[2] * 100), (rarityPercents[0] * 100) + (rarityPercents[1] * 100) + (rarityPercents[2] * 100) + (rarityPercents[3] * 100) - 1]
    rarities = [common, uncommon, rare, mythic]

    randomRarity = randint(0, 100)

    #Pick the rarity
    mode = 0
    for x in range(len(rarities)):
        if randomRarity >= rarities[x][0] and randomRarity <= rarities[x][1]:
            mode = x
            break

    #See if a card of that rarity exists
    if len(name[mode]) == 0:
        return deck, deckCMC

    #Pick the card
    else:
        randomIndex = randint(0, len(name[mode])-1)
        if ((deck_mode == "brawl" and name[mode][randomIndex] not in deck) or (deck_mode == "standard")):
            if types != []:
                if types[mode][randomIndex].find("Artifact") != -1 and randint(0, 100) > 100*artifact_percent: #Lowers the chance you get an artifact
                    return deck, deckCMC
            deck.append(name[mode][randomIndex])

            #Update CMC
            manaSymbols = ["R", "W", "B", "U", "G"]
            if manaCost != []:
                for y in manaCost[mode][randomIndex].replace("{", "").replace("}", ""):
                    if y in manaSymbols:
                        deckCMC[manaSymbols.index(y)] = deckCMC[manaSymbols.index(y)] + 1
                    else:
                        try:
                            deckCMC[5] = deckCMC[5] + int(y)
                        except:
                            deckCMC[5] = deckCMC[5] + 0
            
            #Update CMC for lands
            if landColors != []:
                land_color = landColors[mode][randomIndex]
                for y in manaSymbols:
                    if y in land_color and deckCMC[manaSymbols.index(y)] != 1 and deckCMC[manaSymbols.index(y)] != 0:
                        deckCMC[manaSymbols.index(y)] = deckCMC[manaSymbols.index(y)] - 1
    return deck, deckCMC
#----------------------------------------------------------

#----------------------------------------------------------
#Main method, used for generating a deck
#----------------------------------------------------------
def generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard):

    retCode = verifyInformation(normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands)

    deck_size = 0
    if type(retCode) == str:
        return retCode
    else:
        deck_size = retCode

    #Array index 0 = common, 1 = uncommon, 2 = rare, 3 = mythic
    name = [[], [], [], []]
    colors = [[], [], [], []]
    manaCost = [[], [], [], []]
    types = [[], [], [], []]

    commanders = [[], [], [], []]
    commanderColorCombo = [[], [], [], []]
    commanderManaCost = [[], [], [], []]

    lands = [[], [], [], []]
    landColors = [[], [], [], []]

    all_card_names = []

    #For each set
    for sets in setsToInclude:
        data = ""

        #Load the json
        with open("./Sets/"+sets+".json", "r", encoding="utf8") as read_file:
            data = json.load(read_file)

        #For each card
        for x in data["cards"]:

            #See if the card has dual names
            cardName = ""
            if x["layout"] == "adventure": #adventure cards
                if x["types"] == "Creature": #only look at the creature portion of the adventure
                    cardName = x["names"][0]
                else:
                    continue
            elif x["layout"] == "split": #split cards use both names
                cardName = x["names"][0] + " // " + x["names"][1]
            else:
                cardName = x["name"]

            #If that card is legal in the format we want and unique
            if (((x["legalities"]["brawl"] == "Legal" and deck_mode == "brawl") or (x["legalities"]["standard"] == "Legal" and deck_mode == "standard")) and (cardName not in all_card_names)):

                #Track all card names
                all_card_names.append(cardName)

                #Set the magic number based on rarity
                magic_number = 0
                if x["rarity"].lower() == "common":
                    magic_number = 0
                elif x["rarity"].lower() == "uncommon":
                    magic_number = 1
                elif x["rarity"].lower() == "rare":
                    magic_number = 2
                elif x["rarity"].lower() == "mythic":
                    magic_number = 3

                #Find the color identity
                colorIdentity = ""
                for y in x["colorIdentity"]:
                    colorIdentity = colorIdentity + y
                colorIdentity = "".join(sorted(colorIdentity)).replace("/", "")

                #If the card is a land card
                if x["types"][0] == "Land":
                    lands[magic_number].append(cardName)
                    landColors[magic_number].append(colorIdentity)

                else:
                    colors[magic_number].append(colorIdentity)
                    manaCost[magic_number].append(x["manaCost"].replace("/", ""))
                    name[magic_number].append(cardName)
                    types[magic_number].append(x["types"][0])

                    #If the card is a legendary creature or planeswalker, mark it as a commander
                    if ((x["type"].find("Legendary Creature") != -1) or (x["type"].find("Legendary Planeswalker") != -1)):
                        commanders[magic_number].append(cardName)
                        commanderColorCombo[magic_number].append(colorIdentity)
                        commanderManaCost[magic_number].append(x["manaCost"].replace("{", "").replace("}", ""))

    colorCombo = ""
    deckCMC = [0, 0, 0, 0, 0, 0] #R, W, B, U, G, Colorless
    deck = []

    #Sort all the color combos
    for x in range(len(possibleColorCombos)):
        possibleColorCombos[x] = "".join(sorted(possibleColorCombos[x]))

    #If standard, pick a color combo
    if deck_mode == "standard":
        colorCombo = possibleColorCombos[randint(0, len(possibleColorCombos)-1)]

    #If commander, pick a commander that fits a color combo
    else:
        attempts = 0
        while len(deck) < 1:
            deck, deckCMC = pick_a_card(commanderManaCost, commanders, [], commander_rarity_percents, deckCMC, deck, 0, artifact_percent, basic_land_percent)
            attempts = attempts + 1
            for x in range(len(commanders)):
                try:
                    colorCombo = commanderColorCombo[x][commanders[x].index(deck[0])]
                    break
                except:
                    colorCombo = "N/A"
            if colorCombo not in possibleColorCombos:
                deck = []
                deckCMC = [0, 0, 0, 0, 0, 0]
            if attempts > 1000:
                return("Warning! After 1000 attempts, a commander could not be found. Please change your rarity values to allow for more cards to be chosen")

    #The more colors in your deck, the less likely you are to get basics
    if len(colorCombo) > 1:
        basic_land_percent = basic_land_percent - (len(colorCombo) * basic_land_percent_removal)

    #Remove all cards that are not part of the colorCombo
    for x in range(len(colors)):
        markForDeletion = []
        for y in range(len(colors[x])):
            if colorCombo.find(colors[x][y]) == -1:
                markForDeletion.append(y)
        for y in sorted(markForDeletion, reverse = True):
            del colors[x][y]
            del manaCost[x][y]
            del name[x][y]
            del types[x][y]
    for x in range(len(landColors)):
        markForDeletion = []
        for y in range(len(landColors[x])):
            if colorCombo.find(landColors[x][y]) == -1:
                markForDeletion.append(y)
        for y in sorted(markForDeletion, reverse = True):
            del lands[x][y]
            del landColors[x][y]

    #Set up the base number of times to loop
    if deck_mode == "standard":
        numberOfLoops = deck_size - numberOfLands[1]
    else:
        numberOfLoops = deck_size - numberOfLands[1] - 1 #-1 b/c you already have the commander

    #Start picking normal cards
    attempts = 0
    while len(deck) < numberOfLoops:
        deck, deckCMC = pick_a_card(manaCost, name, types, normal_rarity_percents, deckCMC, deck, 0, artifact_percent, basic_land_percent)
        attempts = attempts + 1
        if attempts > 1000:
            return("Warning! After 1000 attempts, a normal card could not be found. Please change your rarity values to allow for more cards to be chosen")

    #Calculate the average cmc of the deck
    averageCMC = int(round(sum(deckCMC)/len(deck)))
    numLands = numberOfLands[0] + averageCMC - 1
    if numLands > numberOfLands[1]:
        numLands = numberOfLands[1]

    #Start picking lands
    ogDeckSize = len(deck)
    attempts = 0
    while len(deck) < numLands + ogDeckSize:
        deck, deckCMC = pick_a_card(landColors, lands, [], land_rarity_percents, deckCMC, deck, 1, artifact_percent, basic_land_percent)
        if attempts > 1000:
            return("Warning! After 1000 attempts, a normal card could not be found. Please change your rarity values to allow for more cards to be chosen")

    #Might need to pick more cards
    attempts = 0
    while len(deck) < deck_size:
        deck, deckCMC = pick_a_card(manaCost, name, types, normal_rarity_percents, deckCMC, deck, 0, artifact_percent, basic_land_percent)
        if attempts > 1000:
            return("Warning! After 1000 attempts, a normal card could not be found. Please change your rarity values to allow for more cards to be chosen")

    #Sideboard
    if sideBoard == True:
        attempts = 0
        while len(deck) < deck_size+15:
            deck, deckCMC = pick_a_card(manaCost, name, types, normal_rarity_percents, deckCMC, deck, 0, artifact_percent, basic_land_percent)
            if attempts > 1000:
                return("Warning! After 1000 attempts, a normal card could not be found. Please change your rarity values to allow for more cards to be chosen")

    #Print deck
    deck_to_return = ""
    basics = [0, 0, 0, 0, 0]
    basicLands = ["Mountain", "Plains", "Swamp", "Island", "Forest"]
    for x in range(deck_size):
        if x == 0 and deck_mode == "brawl":
            deck_to_return = deck_to_return + "Commander\n"
        elif ((x == 1 and deck_mode == "brawl") or (x == 0 and deck_mode == "standard")):
            deck_to_return = deck_to_return + "\nDeck\n"
        elif x == 60:
            deck_to_return = deck_to_return + "\nSideboard\n"
        skip = 0
        for y in range(len(basicLands)):
            if deck[x] == basicLands[y]:
                basics[y] = basics[y] + 1
                skip = 1
                break
        if skip == 0:
            deck_to_return = deck_to_return + "1 "+ deck[x] + "\n"
    for x in range(len(basics)):
        if basics[x] != 0:
            deck_to_return = deck_to_return + str(basics[x]) + " " + basicLands[x] + "\n"

    if sideBoard == True:
        deck_to_return = deck_to_return + "\nSideboard\n"
        for x in range(len(deck)-deck_size):
            deck_to_return = deck_to_return + "1 "+ deck[x+deck_size] + "\n"
    return deck_to_return[:-1]
#----------------------------------------------------------

#----------------------------------------------------------
#Main
#----------------------------------------------------------
if __name__ == "__main__":

    #TODO -- These should be check boxes on html
    #The sets you want to draw cards from
    dominaria = False
    historic_anthology_1 = False
    historic_anthology_2 = False
    historic_anthology_3 = False
    ixalan = False
    rivals_of_ixalan = False
    core_2019 = False
    guilds_of_ravnica = True
    ravnica_allegiance = True
    war_of_the_spark = True
    core_2020 = True
    throne_of_eldraine = True
    theros_beyond_death = True
    ikoria = True
    core_2021 = True
    setsToInclude = []
    if guilds_of_ravnica == True:
        setsToInclude.append("GRN")
    if ravnica_allegiance == True:
        setsToInclude.append("RNA")
    if war_of_the_spark == True:
        setsToInclude.append("WAR")
    if core_2020 == True:
        setsToInclude.append("M20")
    if throne_of_eldraine == True:
        setsToInclude.append("ELD")
    if theros_beyond_death == True:
        setsToInclude.append("THB")
    if ikoria == True:
        setsToInclude.append("IKO")
    if core_2021 == True:
        setsToInclude.append("M21")

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #The odds you will get a normal card of a certain rarity (written as decimals, must add to 1)
    normal_common_rarity = .15
    normal_uncommon_rarity = .75
    normal_rare_rarity = .10
    normal_mythic_rarity = 0
    normal_rarity_percents = [normal_common_rarity, normal_uncommon_rarity, normal_rare_rarity, normal_mythic_rarity]

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #The odds you will get a commander card of a certain rarity (written as decimals, must add to 1)
    commander_common_rarity = 0
    commander_uncommon_rarity = .25
    commander_rare_rarity = .5
    commander_mythic_rarity = .25
    commander_rarity_percents = [commander_common_rarity, commander_uncommon_rarity, commander_rare_rarity, commander_mythic_rarity]

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #The odds you will get a land card of a certain rarity (written as decimals, must add to 1)
    land_common_rarity = .5
    land_uncommon_rarity = .5
    land_rare_rarity = 0
    land_mythic_rarity = 0
    land_rarity_percents = [normal_common_rarity, normal_uncommon_rarity, normal_rare_rarity, normal_mythic_rarity]

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #Odds you will get an artifact (stacked on after normal percents, must be between 0 and 1)
    artifact_percent = .25

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #Odds you will get a basic land (stacked on before land percents, must be between 0 and 1)
    basic_land_percent = .9

    #TODO -- https://www.w3schools.com/tags/att_input_type_number.asp -- assume values between 0 and 1
    #For each color, remove this percent from basic_land_percent, so you have less basics for more colors
    basic_land_percent_removal = .1

    #TODO -- make a drop down menu
    #The game mode you want to play
    deck_mode = "brawl" #standard, brawl

    #The min and max number of lands
    min_lands = 23
    max_lands = 27
    numberOfLands = [min_lands, max_lands]

    #TODO -- should be check boxes
    #The possible color combinations your deck could be
    possibleColorCombos = ["", "R", "W", "G", "U", "B", "RW", "RG", "RU", "RB", "WG", "WU", "WB", "GU", "GB", "UB", "RGB", "WGU", "BRU", "GWR", "UWB", "URW", "RWB", "BGU", "RUG", "WGB"]

    #TODO -- should be a checkbox
    sideBoard = True

    returned = generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard)    
    print(returned)
#----------------------------------------------------------
