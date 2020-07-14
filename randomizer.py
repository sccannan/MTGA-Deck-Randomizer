#!/usr/bin/env python3
"""
To generate HTML documentation for this program issue the
command:
    pydoc3 -w randomizer
"""
#---------------------------------------------------------
#---------------------------------------------------------
import json
from random import randint
from tkinter import *
#---------------------------------------------------------
#---------------------------------------------------------

#---------------------------------------------------------
#---------------------------------------------------------
def parseInformation(sets, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, deckSize, sideBoard):
    """Makes sure all passed in information is valid (correct typing, values, etc) and translate it to the format we want

    Args:
        sets (list): A list of 0/1 values for including certain sets
        possibleColorCombos (list): A list of 0/1 values for including certain colorCombos
        normal_rarity_percents (list): A list of percentages (int) for each rarity (for normal cards - not lands or commanders)
        commander_rarity_percents (list): A list of percentages (int) for each rarity for commanders
        land_rarity_percents (list): A list of percentages (int) for each rarity for lands
        artifact_percents (int): An int for how often we want to pick an artifact if we randomly select one
        basic_land_percent (int): An int for how often we want to pick a basic land
        basic_land_percent_removal (int): An int for modifying basic_land_percent
        deck_mode (str): A string representing what type of deck format we want to use
        numberOfLands (list): A list containing the minimum number of lands [0] you want in a deck, and the maximum number of lands [1] you want in a deck
        deckSize (int): The deck size
        sideBoard (int): 0 for no sideboard, 1 for sideboard

    Returns:
        list: A list of the input parameters now translated (same order as input)
    """
    
    retValues = ["", "", "", "", "", "", "", "", "", "", "", "", ""]

    #The possible color combinations
    ccToInclude = []
    possibleCC = ["", "R", "W", "G", "U", "B", "RW", "GR", "RU", "BR", "GW", "UW", "BW", "GU", "BG", "BU", "BGR", "GUW", "BRU", "GRW", "BUW", "RUW", "BRW", "BGU", "GRU", "BGW", "BGRU", "BGRW", "GRUW", "BGUW", "BRUW", "BGRUW"]
    if sum(possibleColorCombos) == 0:
        retValues[-1] = "Error!\nAt least 1 mana color box needs to be checked"
        return retValues
    if len(possibleColorCombos) != len(possibleCC):
        retValues[-1] = "Error!\nThere are 32 mana combinations available - your list has " + str(len(possibleColorCombos))
        return retValues
    for x in range(len(possibleColorCombos)):
        if possibleColorCombos[x] == 1:
            ccToInclude.append(possibleCC[x])
        elif possibleColorCombos[x] == 0:
            pass
        else:
            retValues[-1] = "Error!\nUnknown value detected - color list must contain only 0s and 1s"
            return retValues

    #Make sure the normal/commander/land percentages are numbers, total 1 after floats, there are no negative values, and that there are only 4 values present
    rarity_percents_list = [normal_rarity_percents, commander_rarity_percents, land_rarity_percents]
    rarity_percents_list_names = ["Normal", "Commander", "Land"]
    for x in range(len(rarity_percents_list)):
        if deck_mode != "brawl" and deck_mode != "friendly brawl" and rarity_percents_list[x] == commander_rarity_percents: #if we arent playing commander, ignore the commander fields
            continue
        if len(rarity_percents_list[x]) != 4:
            retValues[-1] = "Error!\nThere are only 4 rarities in MTG - the provided " + rarity_percents_list_names[x] + " rarities list has " + str(len(rarity_percents_list))
            return retValues
        for y in range(len(rarity_percents_list[x])):
            try:
                rarity_percents_list[x][y] = float(rarity_percents_list[x][y])/100
            except:
                retValues[-1] = "Error!\nNon numeric value detected for " + rarity_percents_list_names[x] + " rarity"
                return retValues
            if rarity_percents_list[x][y] < 0:
                retValues[-1] = "Error!\nNegative value detected for " + rarity_percents_list_names[x] + " rarity"
                return retValues
        if sum(rarity_percents_list[x]) != 1:
            retValues[-1] = "Error!\nThe sum of " + rarity_percents_list_names[x] + " rarity doesnt equal 100"
            return retValues

    #Makes sure artifact, basic lands, and basic lands removal percentage is 0<x<100 and is a number
    other_rarity_percents_list = [artifact_percent, basic_land_percent, basic_land_percent_removal]
    other_rarity_percents_list_names = ["Artifact", "Basic land", "Basic land removal percentage"]
    for x in range(len(other_rarity_percents_list)):
        try:
            other_rarity_percents_list[x] = float(other_rarity_percents_list[x])/100
        except:
            retValues[-1] = "Error!\nNon numeric value detected for " + other_rarity_percents_list[x] + " percentage"
            return retValues
        if other_rarity_percents_list[x] > 1 or other_rarity_percents_list[x] < 0:
            retValues[-1] = "Error!\n" + other_rarity_percents_list[x] + " percentage isnt between 0 and 100"
            return retValues

    #Make sure the deck size is a number
    try:
        deckSize = int(deckSize)
    except:
        retValues[-1] = "Error!\nNon numeric value detected for deck size"
        return retValues

    possibleSets = ["DOM", "HA1", "HA2", "HA3", "XLN", "RIX", "M19", "GRN", "RNA", "WAR", "M20", "ELD", "THB", "IKO", "M21"]

    #Make sure the deck mode is supported
    if deck_mode == "brawl" or deck_mode == "friendly brawl":
        if deckSize != 60:
            retValues[-1] = "Error!\nBrawl requires at 60 cards"
            return retValues
        if deck_mode == "brawl":
            possibleSets = possibleSets[7:]
            sets = sets[7:]

    elif deck_mode == "standard":
        if deckSize < 60:
            retValues[-1] = "Error!\nStandard requires at least 60 cards"
            return retValues
        possibleSets = possibleSets[7:]
        sets = sets[7:]

    elif deck_mode == "pauper":
        if float(normal_rarity_percents[0]) != 1 or float(commander_rarity_percents[0]) != 1 or float(land_rarity_percents[0]) != 1:
            retValues[-1] = "Error!\nPauper only supports commons"
            return retValues
        if deckSize < 60:
            retValues[-1] = "Error!\nPauper requires at least 60 cards"
            return retValues
        deck_mode = "historic"

    elif deck_mode == "artisan":
        if ((float(normal_rarity_percents[0]) + float(normal_rarity_percents[1]) != 1) or (float(commander_rarity_percents[0]) + float(commander_rarity_percents[1]) != 1) or (float(land_rarity_percents[0]) + float(land_rarity_percents[1]) != 1)):
            retValues[-1] = "Error!\nArtisan only supports commons or uncommons"
            return retValues
        if deckSize < 60 or deckSize > 250:
            retValues[-1] = "Error!\nArtisan requires at least 60 cards and maximum 250 cards"
            return retValues
        deck_mode = "standard"
        possibleSets = possibleSets[7:]
        sets = sets[7:]

    elif deck_mode == "singleton":
        if deckSize < 60:
            retValues[-1] = "Error!\nSingleton requires at least 60 cards"
            return retValues
        possibleSets = possibleSets[7:]
        sets = sets[7:]

    elif deck_mode == "historic":
        if deckSize < 60:
            retValues[-1] = "Error!\nHistoric requires at least 60 cards"
            return retValues
        deck_mode = "historic"

    elif deck_mode == "direct game":
        if deckSize < 60:
            retValues[-1] = "Error!\nA direct game requires at least 60 cards"
            return retValues

    elif deck_mode == "limited":
        if deckSize < 40:
            retValues[-1] = "Error!\nLimited requires at least 40 cards"
            return retValues

    else:
        retValues[-1] = "Error!\nUnsupported deck mode!"
        return retValues

    #The sets you want to draw cards from
    setsToInclude = []
    if sum(sets) == 0:
        retValues[-1] = "Error!\nAt least 1 set box needs to be checked that is part of your game format"
        return retValues
    for x in range(len(sets)):
        if sets[x] == 1:
            setsToInclude.append(possibleSets[x])
        elif sets[x] == 0:
            pass
        else:
            retValues[-1] = "Error!\nUnknown value detected - sets to include list must contain only 0s and 1s"
            return retValues

    #Make sure those JSONs exist
    for x in setsToInclude:
        try:
            read_file = open("./Sets/"+x+".json", "r", encoding="utf8")
            read_file.close()
        except:
            retValues[-1] = "Error!\nFile \"./Sets/" + x + ".json\" could not be found - please make sure it is in the \"Sets\" folder"
            return retValues

    #Make sure the number of lands is valid
    try:
        min_lands = int(round(float(numberOfLands[0])))
        max_lands = int(round(float(numberOfLands[1])))
    except:
        retValues[-1] = "Error!\nNon numeric value detected for minimum and/or maximum number of lands"
        return retValues
    if min_lands > max_lands:
        retValues[-1] = "Error!\nMinimum lands must be less than or equal too maximum lands"
        return retValues
    if max_lands > int(deckSize):
        retValues[-1] = "Error!\nMaximum lands must be less than or equal too the maximum deck size"
        return retValues
    if min_lands < 0:
        retValues[-1] = "Error!\nMinimum lands must be greater than 0"
        return retValues
    if max_lands < 0:
        retValues[-1] = "Error!\nMaximum lands must be greater than 0"
        return retValues

    #Make sure sideboard is valid
    try:
        sideBoard = int(sideBoard)
        if sideBoard != 0 and sideBoard != 1:
            retValues[-1] = "Error!\nSideboard must be 0 or 1"
            return retValues
    except:
        retValues[-1] = "Error!\nSideboard must be 0 or 1"
        return retValues

    return [setsToInclude, ccToInclude, rarity_percents_list[0], rarity_percents_list[1], rarity_percents_list[2], other_rarity_percents_list[0], other_rarity_percents_list[1], other_rarity_percents_list[2], deck_mode, [min_lands, max_lands], deckSize, sideBoard, ""]
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def load_json_sets(setsToInclude, deck_mode):
    """Loads the JSONs and returns a list for normal cards, commanders, and lands

    Args:
        setsToInclude (list): A list of sets you want to pull from
        deck_mode (str): The deck mode

    Returns:
        list: A list of normal cards
        list: A list of commander cards
        list: A list of land cards
    """

    #Array index 0 = common, 1 = uncommon, 2 = rare, 3 = mythic
    normal = [[], [], [], []]
    commander = [[], [], [], []]
    land = [[], [], [], []]
    all_card_names = []
    rare = ["common", "uncommon", "rare", "mythic"]

    #For each set
    for sets in setsToInclude:
        data = ""
        
        #Load the json
        with open("./Sets/"+sets+".json", "r", encoding="utf8") as read_file:
            data = json.load(read_file)

        #Some files are written differently
        jsonIndex = ""
        try:
            jsonIndex = data["cards"]
        except:
            jsonIndex = data["data"]["cards"]

        #For each card
        for x in jsonIndex:

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
            if deck_mode == "all":
                legalResult = "Legal"
            else:
                try:
                    legalResult = x["legalities"][deck_mode]
                except:
                    legalResult = "Not Legal"

            #See if the card has a manacost
            try:
                manaCost = x["manaCost"]
            except:
                try:
                    if x["types"][0] == "Land":
                        legalResult = "Legal"
                    else:
                        legalResult = "Not Legal"
                except:
                    legalResult = "Not Legal"

            if (legalResult == "Legal" and cardName not in all_card_names):
                    
                #Track all card names
                all_card_names.append(cardName)

                #Set the magic number based on rarity
                magic_number = rare.index(x["rarity"].lower())
                 
                #Find the color identity
                colorIdentity = ""
                for y in x["colorIdentity"]:
                    colorIdentity = colorIdentity + y
                colorIdentity = "".join(sorted(colorIdentity))

                #If the card is a land card
                if x["types"][0] == "Land":
                    land[magic_number].append([cardName, colorIdentity, -1, -1])

                else:
                    normal[magic_number].append([cardName, colorIdentity, x["manaCost"], x["types"][0]])
                    
                    #If the card is a legendary creature or planeswalker, mark it as a commander
                    if ((x["type"].find("Legendary") != -1) and ((x["type"].find("Creature") != -1) or (x["type"].find("Planeswalker") != -1))):
                        commander[magic_number].append([cardName, colorIdentity, x["manaCost"], x["types"][0]])

    return normal, commander, land
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def color_removal(card_list, colorCombo, deck_mode):
    """Removes all cards that are not in the specified color
       If a card is split mana (Red or White) and the mode is brawl, both colors must be valid
       If a card is split mana (Red or White) and the mode is standard, as long as 1 possible combo works keep the card

    Args:
        card_list (list): A list of cards
        colorCombo (str): The color combo you have
        deck_mode (str): The deck mode

    Returns:
        list: A list of cards with colors now removed
    """

    #For each rarirty
    for x in range(len(card_list)):
        markForDeletion = []

        #For each cared in each rarity
        for y in range(len(card_list[x])):

            #If that card isnt a land
            if card_list[x][y][2] != -1:

                #If that card is a split mana card and the format is not brawl
                if card_list[x][y][2].find("/") != -1 and deck_mode != "brawl":

                    #Make all color combos with the splits
                    colorComboSplit = []
                    def small_recursive_function(manaSymbols):
                        if manaSymbols.find("/") != -1:
                            colorComboSplit.append(small_recursive_function((manaSymbols[:manaSymbols.find("/")-1]) + (manaSymbols[manaSymbols.find("/")+1:])))
                            colorComboSplit.append(small_recursive_function((manaSymbols[:manaSymbols.find("/")]) + (manaSymbols[manaSymbols.find("/")+2:])))
                        else:
                            return manaSymbols
                    small_recursive_function(card_list[x][y][2])
                    
                    #Remove all None and repeats
                    markForDeletion2 = []
                    reducedColors = []
                    for a in range(len(colorComboSplit)):
                        if colorComboSplit[a] == None or set(colorComboSplit[a]) in reducedColors:
                            markForDeletion2.append(a)
                        else:
                            reducedColors.append(set(colorComboSplit[a]))
                    for a in sorted(markForDeletion2, reverse=True):
                        del colorComboSplit[a]

                    #As long as 1 color works, we can keep the card
                    keep = 0
                    manaSymbols = ["B", "G", "R", "U", "W"]
                    for a in range(len(colorComboSplit)):
                        tempColorIdentityList = list(set(colorComboSplit[a]))
                        tempColorIdentity = ""
                        for b in tempColorIdentityList:
                            if b in manaSymbols:
                                tempColorIdentity = tempColorIdentity + b

                        if colorCombo.find(tempColorIdentity.replace("{", "").replace("}", "")) != -1:
                            keep = 1
                            card_list[x][y][1] = tempColorIdentity
                            card_list[x][y][2] = colorComboSplit[a]
                            break
                    if keep == 0:
                        markForDeletion.append(y)
                        
                #Elif that cards color identity isnt an option
                elif colorCombo.find(card_list[x][y][1]) == -1:
                    markForDeletion.append(y)

            #Elif that cards color identity isnt an option
            elif colorCombo.find(card_list[x][y][1]) == -1:
                markForDeletion.append(y)

        #Remove the bad cards
        for y in sorted(markForDeletion, reverse = True):
            del card_list[x][y]
    return card_list
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def pick_a_card(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, landFlag, deck_mode):
    """Randomly picks a card

    Args:
        card_list (list): A list of each cards, split by rarities
        rarityPercents (list): A list of percentages (decimals) for each rarity
        deckCMC (list): A list of the number of colored and colorless mana symbols
        deck (list): A list of card names in the deck
        artifact_percent (float) A decimal for how often we want to pick an artifact if we randomly select one
        basic_land_percent (float): A decimal for how often we want to pick a basic land
        landFlag (int): 0 if we are looking at lands
        deck_mode (str): The deck mode

    Returns:
        list: A list of card names in the deck after the new card has been picked
        list: A list of the number of colored and colorless mana symbols after the new card has been picked
        str: The color identity of the card that was just added
    """    

    #See if you are picking a basic land
    if landFlag == 0 and randint(0, 100) < 100*basic_land_percent:

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
            total = 1
            basic_land_range[3][0] = 0
            basic_land_range[3][1] = 0

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
        return deck, deckCMC, ""

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
    if len(card_list[mode]) == 0:
        return deck, deckCMC, ""

    #Pick the card
    else:
        randomIndex = randint(0, len(card_list[mode])-1)
        if ((deck_mode == "brawl" and card_list[mode][randomIndex][0] not in deck) or (deck_mode == "standard" and deck.count(card_list[mode][randomIndex][0]) < 4) or (deck_mode == "historic" and deck.count(card_list[mode][randomIndex][0]) < 4) or (deck_mode == "singleton" and card_list[mode][randomIndex][0] not in deck) or (deck_mode == "limited")):
            if card_list[mode][randomIndex][3] != -1:
                #Lowers odds of getting an artifact unless your deck is colorless
                if card_list[mode][randomIndex][3].find("Artifact") != -1 and randint(0, 100) > 100*artifact_percent and sum(deckCMC[:-1]) != 0:
                    return deck, deckCMC, ""
            deck.append(card_list[mode][randomIndex][0])

            #Update CMC
            manaSymbols = ["R", "W", "B", "U", "G"]
            if card_list[mode][randomIndex][2] != -1:
                for y in card_list[mode][randomIndex][2]:
                    if y in manaSymbols:
                        deckCMC[manaSymbols.index(y)] = deckCMC[manaSymbols.index(y)] + 1
                    else:
                        try:
                            deckCMC[5] = deckCMC[5] + int(y)
                        except: #X costs, { and }
                            deckCMC[5] = deckCMC[5] + 0
            
            #Update CMC for lands
            else:
                land_color = card_list[mode][randomIndex][1]
                for y in manaSymbols:
                    if y in land_color and deckCMC[manaSymbols.index(y)] != 1 and deckCMC[manaSymbols.index(y)] != 0:
                        deckCMC[manaSymbols.index(y)] = deckCMC[manaSymbols.index(y)] - 1
    return deck, deckCMC, card_list[mode][randomIndex][1]
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def pick_a_card_helper(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops, landFlag, deck_mode):
    """A helper function for picking a card
    Tracks the number of times weve queried a card, errors if too many

    Args:
        card_list (list): A list of each cards, split by rarities
        rarityPercents (list): A list of percentages (decimals) for each rarity
        deckCMC (list): A list of the number of colored and colorless mana symbols
        deck (list): A list of card names in the deck
        artifact_percent (float) A decimal for how often we want to pick an artifact if we randomly select one
        basic_land_percent (float): A decimal for how often we want to pick a basic land
        landFlag (int): 0 if we are looking at lands
        deck_mode (str): The deck mode

    Returns:
        list: A list of card names in the deck after the new card has been picked
        list: A list of the number of colored and colorless mana symbols after the new card has been picked
        str: The color identity of the card that was just added
        str: Null if correct, error message if error
    """

    attempts = 0
    while len(deck) < numberOfLoops:
        deck, deckCMC, color = pick_a_card(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, landFlag, deck_mode)
        attempts = attempts + 1
        if attempts > 1000:
            return [], [], [], ("Warning! After 1000 attempts, a normal card could not be found. Please change your rarity values to allow for more cards to be chosen")
    return deck, deckCMC, color, ""
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def print_deck(deck, deck_size, sideBoard, deck_mode):
    """Turns the deck into an MTGA formatted string

    Args:
        deck (list): A list of each card in the deck
        deck_size (int): How large the deck is, not including the sideboard
        sideBoard (bool): True if there is a sideBoard present
        deck_mode (str): The deck mode

    Returns:
    str: The MTGA formatted string of the deck
    """

    deck_to_return = ""
    basics = [0, 0, 0, 0, 0]
    multiples = []
    multiplesCount = []
    for x in range(deck_size):
        if x == 0 and deck_mode == "brawl":
            deck_to_return = deck_to_return + "Commander\n"
        elif (x == 1 and deck_mode == "brawl"):
            deck_to_return = deck_to_return + "\nDeck\n"
        elif (x == 0 and deck_mode != "brawl"):
            deck_to_return = deck_to_return + "Deck\n"
        skip = 0

        #Check for non sideboard multiples
        tempDeck = deck[:deck_size]
        if tempDeck.count(deck[x]) > 1:
            if deck[x] not in multiples:
                multiples.append(deck[x])
                multiplesCount.append(tempDeck.count(deck[x]))
            skip = 1

        #If the card isnt a multiple
        if skip == 0:
            deck_to_return = deck_to_return + "1 "+ deck[x] + "\n"

    #Multiples
    for x in range(len(multiples)):
        deck_to_return = deck_to_return + str(multiplesCount[x]) + " " + multiples[x] + "\n"

    #If we want a sideboard 
    if sideBoard == True:
        multiples = []
        multiplesCount = []
        deck_to_return = deck_to_return + "\nSideboard\n"

        #For each sideboard card
        for x in range(len(deck)-deck_size):
            skip = 0

            #Check for sideboard multiples
            tempDeck = deck[deck_size:]
            if tempDeck.count(deck[x+deck_size]) > 1:
                if deck[x+deck_size] not in multiples:
                    multiples.append(deck[x+deck_size])
                    multiplesCount.append(tempDeck.count(deck[x+deck_size]))
                skip = 1

            #If the card isnt a multiple
            if skip == 0:
                deck_to_return = deck_to_return + "1 "+ deck[x+deck_size] + "\n"

        #Multiples
        for x in range(len(multiples)):
            deck_to_return = deck_to_return + str(multiplesCount[x]) + " " + multiples[x] + "\n"
    return deck_to_return[:-1]
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard, deckSize):
    """Makes sure all passed in information is valid (correct typing, values, etc)

    Args:
        setsToInclude (list): A list of 0/1 values for including certain sets
        normal_rarity_percents (list): A list of percentages (ints) for each rarity (for normal cards - not lands or commanders)
        commander_rarity_percents (list): A list of percentages (ints) for each rarity for commanders
        land_rarity_percents (list): A list of percentages (ints) for each rarity for lands
        artifact_percents (int): An int for how often we want to pick an artifact if we randomly select one
        basic_land_percent (int): An int for how often we want to pick a basic land
        basic_land_percent_removal (int): An int for modifying basic_land_percent
        deck_mode (str): A string representing what type of format we want to use
        numberOfLands (list): A list containing the minimum number of lands you want in a deck, and the maximum number of lands you want in a deck
        possibleColorCombos (list): A list of 0/1 values for including certain colorCombos
        sideBoard (int): 0 is False, 1 is True
        deckSize (int): The deck size

    Returns:
        str: Either an error message on failure, or a string representation of the deck 
    """

    #Checking and transforming the information
    setsToInclude, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, deck_size, sideBoard, errorCode = parseInformation(setsToInclude, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, deckSize, sideBoard)
    if errorCode != "":
        return errorCode

    #Loads the JSONS
    normal = []
    commander = []
    land = []
    if deck_mode == "singleton":
        normal, commander, land = load_json_sets(setsToInclude, "standard")
    elif deck_mode == "friendly brawl":
        normal, commander, land = load_json_sets(setsToInclude, "all")
        deck_mode = "brawl"
    elif deck_mode == "direct game":
        normal, commander, land = load_json_sets(setsToInclude, "all")
        deck_mode = "historic"
    elif deck_mode == "limited":
        normal, commander, land = load_json_sets(setsToInclude, "all")
    else:
        normal, commander, land = load_json_sets(setsToInclude, deck_mode)

    colorCombo = ""
    deckCMC = [0, 0, 0, 0, 0, 0] #R, W, B, U, G, Colorless
    deck = []

    #If standard, pick a color combo
    if deck_mode == "standard" or deck_mode == "historic" or deck_mode == "limited" or deck_mode == "singleton":
        colorCombo = possibleColorCombos[randint(0, len(possibleColorCombos)-1)]

    #If commander, pick a commander that fits a color combo
    elif deck_mode == "brawl":
        attempts = 0
        while len(deck) < 1:
            deck, deckCMC, colorCombo = pick_a_card(commander, commander_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, 1, deck_mode)
            attempts = attempts + 1
            if colorCombo not in possibleColorCombos:
                deck = []
                deckCMC = [0, 0, 0, 0, 0, 0]
            if attempts > 1000:
                return("Warning! After 1000 attempts, a commander could not be found. Please change your rarity values to allow for more cards to be chosen")

    else:
        return("Error!")

    #The more colors in your deck, the less likely you are to get basics
    if len(colorCombo) > 1:
        basic_land_percent = float(basic_land_percent) - (len(colorCombo) * float(basic_land_percent_removal))

    #Remove all cards that are not part of the colorCombo
    normal = color_removal(normal, colorCombo, deck_mode)
    land = color_removal(land, colorCombo, deck_mode)

    #Start picking normal cards
    numberOfLoops = deck_size - numberOfLands[1] - len(deck)
    deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops, 1, deck_mode)
    if error != "":
        return(error)

    #Calculate the average cmc of the deck
    averageCMC = int(round(sum(deckCMC)/len(deck)))
    numLands = numberOfLands[0] + averageCMC - 1
    if numLands > numberOfLands[1]:
        numLands = numberOfLands[1]

    #Start picking lands
    numberOfLoops = len(deck) + numLands
    deck, deckCMC, colorCombo, error = pick_a_card_helper(land, land_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops, 0, deck_mode)
    if error != "":
        return(error)

    #Might need to pick more cards to fill the deck size
    deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, deck_size, 1, deck_mode)
    if error != "":
        return(error)

    #Sideboard
    if sideBoard == True:
        deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, deck_size+15, 1, deck_mode)
        if error != "":
            return(error) 

    #Print deck
    return(print_deck(deck, deck_size, sideBoard, deck_mode))
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
if __name__ == "__main__":

    #All of the TKinter GUI stuff is here
    class Checkbar(Frame):
        """A class to group a bunch of checkboxes together

        Attributes:
            vars: pointers to all the checkboxes
        """
        def __init__(self, parent=None, picks=[], toSelect=0, allBar=True, allBarToggle=True):
            """Inits the checkbar with len(picks) boxes"""
            Frame.__init__(self, parent)
            self.vars = []
            if allBar == True:
                var = IntVar()
                chk = Checkbutton(self, text='All', command=lambda: check_bar_toggle(self), variable=var)
                chk.pack(side=LEFT)
                if allBarToggle == True:
                    chk.select()
                self.vars.append(var)
            for pick in picks:
                var = IntVar()
                chk = Checkbutton(self, text=pick, variable=var)
                if toSelect == 0:
                    chk.select()
                chk.pack(side=LEFT)
                self.vars.append(var)

        def state(self):
            """Returns a list of 0/1s depending if a box is checked"""
            return map((lambda var: var.get()), self.vars)

        def all_on(self):
            for x in self.vars:
                x.set(True)

        def all_off(self):
            for x in self.vars:
                x.set(False)

    def generate_helper():
        """
        A helper method to call deck generation
        """
        setsToInclude = list(setCheckBar.state())[1:] + list(setCheckBar2.state())[1:]
        normal_rarity_percents = [normalList[0].get("1.0",END), normalList[1].get("1.0",END), normalList[2].get("1.0",END), normalList[3].get("1.0",END)]
        commander_rarity_percents = [commanderList[0].get("1.0",END), commanderList[1].get("1.0",END), commanderList[2].get("1.0",END), commanderList[3].get("1.0",END)]
        land_rarity_percents = [landList[0].get("1.0",END), landList[1].get("1.0",END), landList[2].get("1.0",END), landList[3].get("1.0",END)]
        artifact_percent = artifactPercent.get("1.0",END)
        basic_land_percent = landPercent.get("1.0",END)
        basic_land_percent_removal = landRPercent.get("1.0",END)
        deck_mode = gmVariable.get()
        numberOfLands = [minLand.get("1.0",END), maxLand.get("1.0",END)]
        possibleColorCombos = list(noColor.state()) + list(monoColor.state())[1:] + list(dualColor.state())[1:] + list(triColor.state())[1:] + list(quadColor.state())[1:] + list(allColor.state())
        sideBoard = sideBoardPointer.get()
        deckSize = deck_size.get("1.0",END)
        T.configure(state='normal')
        T.delete('1.0', END)
        T.insert(END, generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard, deckSize))
        T.configure(state='disabled')

    def copy_to_clipboard():
        """
        Copys the textbox to the clipboard
        """
        root.clipboard_clear()
        root.clipboard_append(T.get("1.0",END))

    def focus_next_widget(event):
        """
        Goes to the next text box on <Tab> or <Return>
        """
        event.widget.tk_focusNext().focus()
        return("break")

    def check_bar_toggle(checkbar):
        if sum(list(checkbar.state())[1:]) != len(list(checkbar.state()))-1:
            checkbar.all_on()
        else:
            checkbar.all_off()

    def reset_to_default():
        """
        Resets the GUI to the initial parameters
        """
        setCheckBar.all_on()
        setCheckBar2.all_on()
        noColor.all_on()
        monoColor.all_on()
        dualColor.all_on()
        triColor.all_on()
        quadColor.all_off()
        allColor.all_off()
        for x in range(len(normalList)):
            normalList[x].delete('1.0', END)
            normalList[x].insert(END, normalListVariable[x])
        for x in range(len(commanderList)):
            commanderList[x].delete('1.0', END)
            commanderList[x].insert(END, commanderListVariable[x])
        for x in range(len(landList)):
            landList[x].delete('1.0', END)
            landList[x].insert(END, landListVariable[x])
        for x in range(len(landsList)):
            landsList[x].delete('1.0', END)
            landsList[x].insert(END, landsListVariable[x])
        artifactPercent.delete('1.0', END)
        artifactPercent.insert(END, "25")
        deck_size.delete('1.0', END)
        deck_size.insert(END, "60")
        T.configure(state='normal')
        T.delete('1.0', END)
        T.insert(END, "Your deck will generate here!")
        T.configure(state='disabled')
        gmVariable.set("brawl")
        sideBoardPointer.set(False)

    #Root
    root = Tk()
    root.resizable(False, False)
    root.geometry("1000x870")
    root.title("MTGA Random Deck Generator")
    root.iconphoto(False, PhotoImage(file='icon.png'))

    #Sets
    setLabel = Label(root, text="Historic Sets")
    setLabel.place(x=10, y=10)
    setCheckBar = Checkbar(root, ["DOM","HA1","HA2","HA3","XLN","RIX","M19"])
    setCheckBar.place(x=10, y=30)
    setCheckBar.config(relief=GROOVE, bd=2)
    setLabel = Label(root, text="Standard Sets")
    setLabel.place(x=10, y=60)
    setCheckBar2 = Checkbar(root, ["GRN","RNA","WAR","M20","ELD","THB","IKO","M21"])
    setCheckBar2.place(x=10, y=80)
    setCheckBar2.config(relief=GROOVE, bd=2)

    #Mana Colors
    manaLabel = Label(root, text="Mana Colors")
    manaLabel.place(x=10, y=110)
    manaFrame = Frame(root)
    manaFrame.pack()
    manaFrame.place(x=10, y=130)
    noColor = Checkbar(manaFrame, ["Colorless"], allBar=False)
    noColor.pack()
    monoColor = Checkbar(manaFrame, ["R", "W", "G", "U", "B"])
    monoColor.pack()
    dualColor = Checkbar(manaFrame, ["RW", "GR", "RU", "BR", "GW", "UW", "BW", "GU", "BG", "BU"])
    dualColor.pack()
    triColor = Checkbar(manaFrame, ["BGR", "GUW", "BRU", "GRW", "BUW", "RUW", "BRW", "BGU", "GRU", "BGW"])
    triColor.pack()
    quadColor = Checkbar(manaFrame, ["BGRU", "BGRW", "GRUW", "BGUW", "BRUW"], toSelect=1, allBarToggle=False)
    quadColor.pack()
    allColor = Checkbar(manaFrame, ["BGRUW"], toSelect=1, allBar=False)
    allColor.pack()
    manaFrame.config(relief=GROOVE, bd=2)
 
    rarityLabels = ["Common", "Uncommon", "Rare", "Mythic"]

    #Normal Cards
    normalCard = Label(root, text="Normal Card Rarities")
    normalCard.place(x=10, y=290)
    normalFrame = Frame(root)
    normalFrame.pack()
    normalFrame.place(x=10, y=310)
    normalList = []
    normalListVariable = ["15", "75", "10", "0"]
    for x in range(4):
        Label(normalFrame, text=rarityLabels[x]).grid(row=x)
        normalList.append(Text(normalFrame, height=1, width=10))
        normalList[x].bind("<Tab>", focus_next_widget)
        normalList[x].bind("<Return>", focus_next_widget)
        normalList[x].insert(END, normalListVariable[x])
        normalList[x].grid(row=x, column=1)
        Label(normalFrame, text="%").grid(row=x, column=2)
    normalFrame.config(relief=GROOVE, bd=2)

    #Commander Cards
    commanderCard = Label(root, text="Commander Card Rarities")
    commanderCard.place(x=210, y=290)
    commanderFrame = Frame(root)
    commanderFrame.pack()
    commanderFrame.place(x=210, y=310)
    commanderList = []
    commanderListVariable = ["0", "25", "50", "25"]
    for x in range(4):
        Label(commanderFrame, text=rarityLabels[x]).grid(row=x)
        commanderList.append(Text(commanderFrame, height=1, width=10))
        commanderList[x].bind("<Tab>", focus_next_widget)
        commanderList[x].bind("<Return>", focus_next_widget)
        commanderList[x].insert(END, commanderListVariable[x])
        commanderList[x].grid(row=x, column=1)
        Label(commanderFrame, text="%").grid(row=x, column=2)
    commanderFrame.config(relief=GROOVE, bd=2)

    #Land Cards
    landCard = Label(root, text="Land Card Rarities")
    landCard.place(x=410, y=290)
    landFrame = Frame(root)
    landFrame.pack()
    landFrame.place(x=410, y=310)
    landList = []
    landListVariable = ["50", "50", "0", "0"]
    for x in range(4):
        Label(landFrame, text=rarityLabels[x]).grid(row=x)
        landList.append(Text(landFrame, height=1, width=10))
        landList[x].bind("<Tab>", focus_next_widget)
        landList[x].bind("<Return>", focus_next_widget)
        landList[x].insert(END, landListVariable[x])
        landList[x].grid(row=x, column=1)
        Label(landFrame, text="%").grid(row=x, column=2)
    landFrame.config(relief=GROOVE, bd=2)

    #Mana/Land Fixing
    landMana = Label(root, text="Lands")
    landMana.place(x=10, y=420)
    landManaFrame = Frame(root)
    landManaFrame.pack()
    landManaFrame.place(x=10, y=440)
    Label(landManaFrame, text="Basic Land Percentage").grid(row=0)
    Label(landManaFrame, text="Basic Land Removal Percentage").grid(row=1)
    Label(landManaFrame, text="Minimum Lands").grid(row=2)
    Label(landManaFrame, text="Maximum Lands").grid(row=3)
    landPercent = Text(landManaFrame, height=1, width=10)
    landRPercent = Text(landManaFrame, height=1, width=10)
    minLand = Text(landManaFrame, height=1, width=10)
    maxLand = Text(landManaFrame, height=1, width=10)
    landsList = [landPercent, landRPercent, minLand, maxLand]
    landsListVariable = ["90", "10", "23", "27"]
    for x in range(len(landsList)):
        landsList[x].bind("<Tab>", focus_next_widget)
        landsList[x].bind("<Return>", focus_next_widget)
        landsList[x].insert(END, landsListVariable[x])
        landsList[x].grid(row=x, column=1)
        if x == 0 or x == 1:
            Label(landManaFrame, text="%").grid(row=x, column=2)
    landManaFrame.config(relief=GROOVE, bd=2)

    #Misc
    misc = Label(root, text="Misc")
    misc.place(x=350, y=420)
    miscFrame = Frame(root)
    miscFrame.pack()
    miscFrame.place(x=350, y=440)
    Label(miscFrame, text="Artifact Percent").grid(row=0)
    Label(miscFrame, text="Deck Size").grid(row=1)
    Label(miscFrame, text="Game Mode").grid(row=2)
    artifactPercent = Text(miscFrame, height=1, width=16)
    artifactPercent.bind("<Tab>", focus_next_widget)
    artifactPercent.bind("<Return>", focus_next_widget)
    gmVariable = StringVar(miscFrame)
    gmVariable.set("brawl") # default value
    gameMode = OptionMenu(miscFrame, gmVariable, "artisan", "brawl", "direct game", "friendly brawl", "historic", "limited", "pauper", "singleton", "standard")
    gameMode.config(width=11)
    artifactPercent.insert(END, "25")
    artifactPercent.grid(row=0, column=1)
    Label(miscFrame, text="%").grid(row=0, column=2)
    deck_size = Text(miscFrame, height=1, width=16)
    deck_size.bind("<Tab>", focus_next_widget)
    deck_size.bind("<Return>", focus_next_widget)
    deck_size.insert(END, "60")
    deck_size.grid(row=1, column=1)
    gameMode.grid(row=2, column=1)
    sideBoardPointer = IntVar()
    sideBoard = Checkbutton(miscFrame, text="Sideboard?", variable=sideBoardPointer)
    sideBoard.grid(row=3, column=0)
    miscFrame.config(relief=GROOVE, bd=2)

    #Deck Output
    outFrame = Frame(root)
    outFrame.pack(side=RIGHT, fill=Y)
    S = Scrollbar(outFrame)
    S.pack(side=RIGHT, fill=Y)
    S2 = Scrollbar(outFrame, orient='horizontal')
    S2.pack(side=BOTTOM, fill=X)
    T = Text(outFrame, height=100, width=40, wrap=NONE)
    T.pack(side=RIGHT)
    S.config(command=T.yview)
    S2.config(command=T.xview)
    T.config(yscrollcommand=S.set)
    T.config(xscrollcommand=S2.set)
    T.insert(END, "Your deck will generate here!")
    T.configure(state='disabled')

    #Key
    keyFrame = Frame(root)
    keyFrame.pack(side=BOTTOM)
    keyLabel = Label(keyFrame, text="Key/Guide")
    keyLabel.pack(side=TOP)
    S3 = Scrollbar(keyFrame)
    S3.pack(side=RIGHT, fill=Y)
    T2 = Text(keyFrame, height=17, width=100, wrap=WORD)
    T2.pack(side=LEFT)
    S3.config(command=T2.yview)
    T2.config(yscrollcommand=S3.set)
    T2.insert(END, "Sets: Check the sets you want to play with\nDOM = Dominaria\nHA1 = Historic Anthology 1\nHA2 = Historic Anthology 2\nHA3 = Historic Anthology 3\nXLN = Ixalan\nRIX = Rivals of Ixalan\nM19 = Core 2019\nGRN = Guilds of Ravnica\nRNA = Ravnica Allegiance\nWAR = War of the Spark\nM20 = Core 2020\nELD = Throne of Eldraine\nTHB = Theros Beyond Death\nIKO = Ikoria\nM21 = Core 2021\n\nMana Colors: Check the mana colors you want your deck possibly being. If you have \"R\", \"W\", and \"RW\", theres a 33% chance your deck is only Red, a 33% chance your deck is only White, and a 33% chance your deck is Red and White\nR = Red\nW = White\nG = Green\nU = Blue\nB = Black\n\nRarities: The odds you want to get a card of a certain rarity. For example, normal common = .25 means there's a 25% chance, for each normal card in your deck, it will be a common\n\nBasic Land Percentage: The odds that for each land, it will be a basic land. This is applied before checking the rarity of each land\n\nBasic Land Removal Percentage: For each color in your deck past the first, this number will get subtracted from Basic Land Percentage so that the more colors in your deck, the more likely you will get non basic lands, which wil help with mana fixing\n\nArtifact Percentage: The odds that you will randomly select an artifact. This is here because artifacts can be run in any deck, so this will limit the amount that can be randomly generated in a deck\n\nHistoric and Traditional Historic - 60+ cards, historic legal, 4 similar card max\n\nStandard and Traditional Standard - 60+ cards, standard legal, 4 similar card max\n\nBrawl - 59 unique cards, 1 unique commander, standard legal\n\nFriendly Brawl - 59 unique cards, 1 unique commander, historic legal\n\nSingleton - 60 unique cards, standard legal\n\nArtisan - 60-250 cards, historic legal, commons or uncommons only, 4 similar card max\n\nPauper - 60+ cards, standard legal, commons only, 4 similar card max\n\nLimited - 40+ cards\n\nDirect Game - 60+ cards, historic legal, 4 similar card max")
    T2.configure(state='disabled')
    Button(root, text='Quit', command=root.quit, height = 2, width = 6).place(x=580, y=70)
    Button(root, text='Generate', command=generate_helper, height = 2, width = 6).place(x=500, y=10)
    Button(root, text='Copy\nDeck', command=copy_to_clipboard, height = 2, width = 6).place(x=580, y=10)
    Button(root, text='Reset', command=reset_to_default, height = 2, width = 6).place(x=500, y=70)
    root.mainloop() 
#----------------------------------------------------------
