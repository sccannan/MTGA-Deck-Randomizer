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
import tkinter
from tkinter import *
#---------------------------------------------------------
#---------------------------------------------------------

#---------------------------------------------------------
#---------------------------------------------------------
class Checkbar(Frame):
    """A class to group a bunch of checkboxes together

    Attributes:
        vars: pointers to all the checkboxes
    """
    def __init__(self, parent=None, picks=[], toSelect=0):
        """Inits the checkbar with len(picks) boxes"""
        Frame.__init__(self, parent)
        self.vars = []
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
#---------------------------------------------------------
#---------------------------------------------------------

#---------------------------------------------------------
#---------------------------------------------------------
def verifyInformation(sets, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, deckSize):
    """Makes sure all passed in information is valid (correct typing, values, etc)

    Args:
        sets (list): A list of 0/1 values for including certain sets
        possibleColorCombos (list): A list of 0/1 values for including certain colorCombos
        normal_rarity_percents (list): A list of percentages (decimals) for each rarity (for normal cards - not lands or commanders)
        commander_rarity_percents (list): A list of percentages (decimals) for each rarity for commanders
        land_rarity_percents (list): A list of percentages (decimals) for each rarity for lands
        artifact_percents (float): A decimal for how often we want to pick an artifact if we randomly select one
        basic_land_percent (float): A decimal for how often we want to pick a basic land
        basic_land_removal_percent (float): A decimal for modifying basic_land_percent
        deck_mode (str): A string representing what type of format we want to use
        numberOfLands (list): A list containing the minimum number of lands you want in a deck, and the maximum number of lands you want in a deck
        deckSize (int): The deck size

    Returns:
        str: Either an error message on failure, or the deck mode
        list: The sets to include
        list: The possibleColorCombos
    """

    #The sets you want to draw cards from
    setsToInclude = []
    possibleSets = ["DOM", "HA1", "HA2", "HA3", "E02", "RIX", "M19", "GRN", "RNA", "WAR", "M20", "ELD", "THB", "IKO", "M21"]
    for x in range(len(sets)):
        if sets[x] == 1:
            setsToInclude.append(possibleSets[x])
        elif sets[x] == 0:
            pass

    #The possible color combinations
    ccToInclude = []
    possibleCC = ["", "R", "W", "G", "U", "B", "RW", "RG", "RU", "RB", "WG", "WU", "WB", "GU", "GB", "UB", "RGB", "WGU", "BRU", "GWR", "UWB", "URW", "RWB", "BGU", "RUG", "WGB", "RGBU", "RGBW", "RGWU", "WBUG", "WRBU", "WRBUG"]
    for x in range(len(possibleCC)):
        possibleCC[x] = "".join(sorted(possibleCC[x]))
    for x in range(len(possibleColorCombos)):
        if possibleColorCombos[x] == 1:
            ccToInclude.append(possibleCC[x])
        elif possibleColorCombos[x] == 0:
            pass

    #Make sure the normal/commander/land percentages are numbers, total 1, there are no negative values, and that there are only 4 values present
    if len(normal_rarity_percents) != 4:
        return("Error!\nThere are only 4 rarities in MTG - the provided normal rarities list has", len(normal_rarity_percents)), [], []
    if len(commander_rarity_percents) != 4:
        return("Error!\nThere are only 4 rarities in MTG - the provided commander rarities list has", len(commander_rarity_percents)), [], []
    if len(land_rarity_percents) != 4:
        return("Error!\nThere are only 4 rarities in MTG - the provided land rarities has", len(land_rarity_percents)), [], []
    for x in range(4):
        try:
            normal_rarity_percents[x] = float(normal_rarity_percents[x])
        except:
            return("Error!\nNon numeric value detected for normal rarity decimals"), [], []
        if normal_rarity_percents[x] < 0:
            return("Error!\nNegative value detected for normal rarity decimals"), [], []
        try:
            commander_rarity_percents[x] = float(commander_rarity_percents[x])
        except:
            return("Error!\nNon numeric value detected for commander rarity decimals"), [], []
        if commander_rarity_percents[x] < 0:
            return("Error!\nNegative value detected for commander rarity decimals"), [], []
        try:
            land_rarity_percents[x] = float(land_rarity_percents[x])
        except:
            return("Error!\nNon numeric value detected for land rarity decimals"), [], []
        if land_rarity_percents[x] < 0:
            return("Error!\nNegative value detected for land rarity decimals"), [], []
    if sum(normal_rarity_percents) != 1:
        return("Error!\nNormal rarity decimals dont equal 1"), [], []
    if sum(commander_rarity_percents) != 1:
        return("Error!\nCommander rarity decimals dont equal 1"), [], []
    if sum(land_rarity_percents) != 1:
        return("Error!\nLand rarity decimals dont equal 1"), [], []

    #Makes sure artifact percentage is 0<x<1 and is a number
    try:
        artifact_percent = float(artifact_percent)
    except:
        return("Error!\nNon numeric value detected for artifact percentage"), [], []
    if artifact_percent > 1 or artifact_percent < 0:
        return("Error!\nArtifact percentage decimal isnt between 0 and 1"), [], []

    #Makes sure basic lands percentage is 0<x<1 and is a number
    try:
        basic_land_percent = float(basic_land_percent)
    except:
        return("Error!\nNon numeric value detected for basic land percentage"), [], []
    if basic_land_percent > 1 or basic_land_percent < 0:
        return("Error!\nBasic land percentage decimal isnt between 0 and 1"), [], []

    #Makes sure basic lands removal percentage is 0<x<1 and is a number
    try:
        basic_land_percent_removal = float(basic_land_percent_removal)
    except:
        return("Error!\nNon numeric value detected for basic land removal percentage decimal"), [], []
    if basic_land_percent_removal > 1 or basic_land_percent_removal < 0:
        return("Error!\nBasic land removal percentage decimal isnt between 0 and 1"), [], []

    #Make sure the deck mode is supported
    deck_mode = deck_mode.lower().rstrip()
    possibleGameModes = ["brawl", "standard", "pauper", "artisan", "historic", "singleton", "friendly brawl"]
    if deck_mode not in possibleGameModes:
        return("Error!\nUnsupported deck mode! Current options are brawl and standard"), [], []

    try:
        deckSize = int(deckSize)
    except:
        return("Error!\nDeck size must me an int"), [], []

    if deck_mode == "brawl" or deck_mode == "friendly brawl":
        if deckSize < 60:
            return("Error!\nBrawl requires at least 60 cards"), [], []

    elif deck_mode == "standard":
        if deckSize < 60:
            return("Error!\nStandard requires at least 60 cards"), [], []

    elif deck_mode == "pauper":
        if normal_rarity_percents[0] != 1 or commander_rarity_percents[0] != 1 or land_rarity_percents[0] != 1:
            return("Error!\nPauper only supports commons"), [], []
        if deckSize != 60:
            return("Error!\nStandard requires 60 cards"), [], []
        deck_mode = "historic"

    elif deck_mode == "artisan":
        if ((normal_rarity_percents[0] + normal_rarity_percents[1] != 1) or (commander_rarity_percents[0] + commander_rarity_percents[1] != 1) or (land_rarity_percents[0] + land_rarity_percents[1] != 1)):
            return("Error!\nArtisan only supports commons or uncommons"), [], []
        if deckSize < 60 or deckSize > 250:
            return("Error!\nArtisan requires at least 60 cards and maximum 250 cards"), [], []
        deck_mode = "standard"

    elif deck_mode == "singleton":
        if deckSize < 60:
            return("Error!\nSingleton requires at least 60 cards"), [], []

    elif deck_mode == "historic":
        if deckSize < 60:
            return("Error!\nHistoric requires at least 60 cards"), [], []
        
    #Make sure the number of lands is valid
    try:
        min_lands = int(round(float(numberOfLands[0])))
        max_lands = int(round(float(numberOfLands[1])))
    except:
        return("Error!\nNon numeric value detected for minimum and/or maximum number of lands"), [], []
    if min_lands > max_lands:
        return("Error!\nMinimum lands must be less than or equal too maximum lands"), [], []
    if max_lands > int(deckSize):
        return("Error!\nMaximum lands must be less than or equal too the maximum deck size"), [], []
    return deck_mode, setsToInclude, ccToInclude
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
            try:
                legalResult = x["legalities"][deck_mode]
                manaCost = x["manaCost"]
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
                colorIdentity = "".join(sorted(colorIdentity)).replace("/", "")

                #If the card is a land card
                if x["types"][0] == "Land":
                    land[magic_number].append([cardName, colorIdentity, -1, -1])

                else:
                    normal[magic_number].append([cardName, colorIdentity, x["manaCost"].replace("/", ""), x["types"][0]])

                    #If the card is a legendary creature or planeswalker, mark it as a commander
                    if ((x["type"].find("Legendary Creature") != -1) or (x["type"].find("Legendary Planeswalker") != -1)):
                        commander[magic_number].append([cardName, colorIdentity, x["manaCost"].replace("{", "").replace("}", ""), x["types"][0]])

    return normal, commander, land
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
def color_removal(card_list, colorCombo):
    """Removes all cards that are not in the specified color

    Args:
        card_list (list): A list of cards
        colorCombo (str): The color combo you have

    Returns:
        list: A list of cards with colors now removed
    """

    for x in range(len(card_list)):
        markForDeletion = []
        for y in range(len(card_list[x])):
            if colorCombo.find(card_list[x][y][1]) == -1:
                markForDeletion.append(y)
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
        if ((deck_mode == "brawl" and card_list[mode][randomIndex][0] not in deck) or (deck_mode == "standard") or (deck_mode == "historic") or (deck_mode == "singleton" and card_list[mode][randomIndex][0] not in deck)):
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
                        except: #X costs
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
    basicLands = ["Mountain", "Plains", "Swamp", "Island", "Forest"]
    for x in range(deck_size):
        if x == 0 and deck_mode == "brawl":
            deck_to_return = deck_to_return + "Commander\n"
        elif (x == 1 and deck_mode == "brawl"):
            deck_to_return = deck_to_return + "\nDeck\n"
        elif (x == 0 and deck_mode != "brawl"):
            deck_to_return = deck_to_return + "Deck\n"
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

#----------------------------------------------------------
#----------------------------------------------------------
def generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard, deckSize):
    """Makes sure all passed in information is valid (correct typing, values, etc)

    Args:
        setsToInclude (list): A list of 0/1 values for including certain sets
        normal_rarity_percents (list): A list of percentages (decimals) for each rarity (for normal cards - not lands or commanders)
        commander_rarity_percents (list): A list of percentages (decimals) for each rarity for commanders
        land_rarity_percents (list): A list of percentages (decimals) for each rarity for lands
        artifact_percents (float): A decimal for how often we want to pick an artifact if we randomly select one
        basic_land_percent (float): A decimal for how often we want to pick a basic land
        basic_land_removal_percent (float): A decimal for modifying basic_land_percent
        deck_mode (str): A string representing what type of format we want to use
        numberOfLands (list): A list containing the minimum number of lands you want in a deck, and the maximum number of lands you want in a deck
        possibleColorCombos (list): A list of 0/1 values for including certain colorCombos
        sideBoard (int): 0 is False, 1 is True
        deckSize (int): The deck size

    Returns:
        str: Either an error message on failure, or a string representation of the deck 
    """

    #Checking the information
    retCode, setsToInclude, possibleColorCombos = verifyInformation(setsToInclude, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, deckSize)

    #Casting the information
    if setsToInclude == [] and possibleColorCombos == []:
        return retCode
    deck_size = int(deckSize)
    deck_mode = retCode.lower().rstrip()
    artifact_percent = float(artifact_percent)
    basic_land_percent = float(basic_land_percent)
    numberOfLands[0] = int(round(float(numberOfLands[0])))
    numberOfLands[1] = int(round(float(numberOfLands[1]))) 

    #Loads the JSONS
    if deck_mode == "singleton":
        normal, commander, land = load_json_sets(setsToInclude, "standard")
    elif deck_mode == "friendly brawl":
        normal, commander, land = load_json_sets(setsToInclude, "historic")
        deck_mode = "brawl"
    else:
        normal, commander, land = load_json_sets(setsToInclude, deck_mode)

    colorCombo = ""
    deckCMC = [0, 0, 0, 0, 0, 0] #R, W, B, U, G, Colorless
    deck = []

    #If standard, pick a color combo
    if deck_mode == "standard" or deck_mode == "historic":
        colorCombo = possibleColorCombos[randint(0, len(possibleColorCombos)-1)]

    #If commander, pick a commander that fits a color combo
    else:
        attempts = 0
        while len(deck) < 1:
            deck, deckCMC, colorCombo = pick_a_card(commander, commander_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, 1, deck_mode)
            attempts = attempts + 1
            if colorCombo not in possibleColorCombos:
                deck = []
                deckCMC = [0, 0, 0, 0, 0, 0]
            if attempts > 1000:
                return("Warning! After 1000 attempts, a commander could not be found. Please change your rarity values to allow for more cards to be chosen")

    #The more colors in your deck, the less likely you are to get basics
    if len(colorCombo) > 1:
        basic_land_percent = float(basic_land_percent) - (len(colorCombo) * float(basic_land_percent_removal))

    #Remove all cards that are not part of the colorCombo
    normal = color_removal(normal, colorCombo)
    land = color_removal(land, colorCombo)

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

    #Might need to pick more cards
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

    #Root
    root = Tk()
    root.resizable(False, False)
    root.geometry("950x850")
    root.title("MTGA Random Deck Generator")
    root.iconphoto(False, PhotoImage(file='icon.png'))

    #Sets
    setLabel = Label(root, text="Historic Sets")
    setLabel.place(x=10, y=10)
    setCheckBar = Checkbar(root, ["DOM","HA1","HA2","HA3","E02","RIX","M19"])
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
    noColor = Checkbar(manaFrame, ["Colorless"])
    noColor.pack()
    monoColor = Checkbar(manaFrame, ["R", "W", "G", "U", "B"])
    monoColor.pack()
    dualColor = Checkbar(manaFrame, ["RW", "RG", "RU", "RB", "WG", "WU", "WB", "GU", "GB", "UB"])
    dualColor.pack()
    triColor = Checkbar(manaFrame, ["RGB", "WGU", "BRU", "GWR", "UWB", "URW", "RWB", "BGU", "RUG", "WGB"])
    triColor.pack()
    quadColor = Checkbar(manaFrame, ["RGBU", "RGBW", "RGWU", "WBUG", "WRBU"], toSelect=1)
    quadColor.pack()
    allColor = Checkbar(manaFrame, ["WRBUG"], toSelect=1)
    allColor.pack()
    manaFrame.config(relief=GROOVE, bd=2)
  
    #Normal Cards
    normalCard = Label(root, text="Normal Card Rarities")
    normalCard.place(x=10, y=280)
    normalFrame = Frame(root)
    normalFrame.pack()
    normalFrame.place(x=10, y=300)
    Label(normalFrame, text="Common").grid(row=0)
    Label(normalFrame, text="Uncommon").grid(row=1)
    Label(normalFrame, text="Rare").grid(row=2)
    Label(normalFrame, text="Mythic").grid(row=3)
    normalC = Text(normalFrame, height=1, width=10)
    normalUC = Text(normalFrame, height=1, width=10)
    normalR = Text(normalFrame, height=1, width=10)
    normalM = Text(normalFrame, height=1, width=10)
    normalC.insert(END, ".15")
    normalUC.insert(END, ".75")
    normalR.insert(END, ".10")
    normalM.insert(END, ".00")
    normalC.grid(row=0, column=1)
    normalUC.grid(row=1, column=1)
    normalR.grid(row=2, column=1)
    normalM.grid(row=3, column=1)
    normalFrame.config(relief=GROOVE, bd=2)

    #Commander Cards
    commanderCard = Label(root, text="Commander Card Rarities")
    commanderCard.place(x=200, y=280)
    commanderFrame = Frame(root)
    commanderFrame.pack()
    commanderFrame.place(x=200, y=300)
    Label(commanderFrame, text="Common").grid(row=0)
    Label(commanderFrame, text="Uncommon").grid(row=1)
    Label(commanderFrame, text="Rare").grid(row=2)
    Label(commanderFrame, text="Mythic").grid(row=3)
    commanderC = Text(commanderFrame, height=1, width=10)
    commanderUC = Text(commanderFrame, height=1, width=10)
    commanderR = Text(commanderFrame, height=1, width=10)
    commanderM = Text(commanderFrame, height=1, width=10)
    commanderC.insert(END, ".00")
    commanderUC.insert(END, ".25")
    commanderR.insert(END, ".50")
    commanderM.insert(END, ".25")
    commanderC.grid(row=0, column=1)
    commanderUC.grid(row=1, column=1)
    commanderR.grid(row=2, column=1)
    commanderM.grid(row=3, column=1)
    commanderFrame.config(relief=GROOVE, bd=2)

    #Land Cards
    landCard = Label(root, text="Land Card Rarities")
    landCard.place(x=390, y=280)
    landFrame = Frame(root)
    landFrame.pack()
    landFrame.place(x=390, y=300)
    Label(landFrame, text="Common").grid(row=0)
    Label(landFrame, text="Uncommon").grid(row=1)
    Label(landFrame, text="Rare").grid(row=2)
    Label(landFrame, text="Mythic").grid(row=3)
    landC = Text(landFrame, height=1, width=10)
    landUC = Text(landFrame, height=1, width=10)
    landR = Text(landFrame, height=1, width=10)
    landM = Text(landFrame, height=1, width=10)
    landC.insert(END, ".50")
    landUC.insert(END, ".50")
    landR.insert(END, ".00")
    landM.insert(END, ".00")
    landC.grid(row=0, column=1)
    landUC.grid(row=1, column=1)
    landR.grid(row=2, column=1)
    landM.grid(row=3, column=1)
    landFrame.config(relief=GROOVE, bd=2)

    #Mana/Land Fixing
    landMana = Label(root, text="Lands")
    landMana.place(x=10, y=400)
    landManaFrame = Frame(root)
    landManaFrame.pack()
    landManaFrame.place(x=10, y=420)
    Label(landManaFrame, text="Basic Land Percentage").grid(row=0)
    Label(landManaFrame, text="Basic Land Removal Percentage").grid(row=1)
    Label(landManaFrame, text="Minimum Lands").grid(row=2)
    Label(landManaFrame, text="Maxmimum").grid(row=3)
    landPercent = Text(landManaFrame, height=1, width=10)
    landRPercent = Text(landManaFrame, height=1, width=10)
    minLand = Text(landManaFrame, height=1, width=10)
    maxLand = Text(landManaFrame, height=1, width=10)
    landPercent.insert(END, ".90")
    landRPercent.insert(END, ".10")
    minLand.insert(END, "23")
    maxLand.insert(END, "27")
    landPercent.grid(row=0, column=1)
    landRPercent.grid(row=1, column=1)
    minLand.grid(row=2, column=1)
    maxLand.grid(row=3, column=1)
    landManaFrame.config(relief=GROOVE, bd=2)

    #Misc
    misc = Label(root, text="Misc")
    misc.place(x=350, y=400)
    miscFrame = Frame(root)
    miscFrame.pack()
    miscFrame.place(x=350, y=420)
    Label(miscFrame, text="Artifact Percent").grid(row=0)
    Label(miscFrame, text="Deck Size").grid(row=1)
    Label(miscFrame, text="Game Mode").grid(row=2)
    artifactPercent = Text(miscFrame, height=1, width=10)
    gmVariable = StringVar(miscFrame)
    gmVariable.set("brawl") # default value
    gameMode = OptionMenu(miscFrame, gmVariable, "artisan", "brawl", "friendly brawl", "historic", "pauper", "singleton", "standard")
    gameMode.config(width=11)
    artifactPercent.insert(END, ".25")
    artifactPercent.grid(row=0, column=1)
    deck_size = Text(miscFrame, height=1, width=10)
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
    keyLabel = Label(keyFrame, text="Key")
    keyLabel.pack(side=TOP)
    S3 = Scrollbar(keyFrame)
    S3.pack(side=RIGHT, fill=Y)
    T2 = Text(keyFrame, height=17, width=100, wrap=WORD)
    T2.pack(side=LEFT)
    S3.config(command=T.yview)
    T2.config(yscrollcommand=S3.set)
    T2.insert(END, "Sets: Check the sets you want to play with\nDOM = Domanaria\nHA1 = Historic Anthology 1\nHA2 = Historic Anthology 2\nHA3 = Historic Anthology 3\nE02 = Ixalan\nRIX = Rivals of Ixalan\nM19 = Core 2019\nGRN = Guilds of Ravnica\nRNA = Ravnica Allegiance\nWAR = War of the Spark\nM20 = Core 2020\nELD = Throne of Eldraine\nTHB = Theros Beyond Death\nIKO = Ikoria\nM21 = Core 2021\n\nMana Colors: Check the mana colors you want your deck possibly being\nR = Red\nW = White\nG = Green\nU = Blue\nB = Black\n\nRarities: The odds you want to get a card of a certain rarity. For example, normal common = .25 means there's a 25% chance, for each normal card in your deck, it will be a common\n\nBasic Land Percentage: The odds that for each land, it will be a basic land. This is applied before checking the rarity of each land\n\nBasic Land Removal Percentage: For each color in your deck past the first, this number will get subtracted from Basic Land Percentage so that the more colors in your deck, the more likely you will get non basic lands, which wil help with mana fixing\n\nArtifact Percentage: The odds that you will randomly select an artifact. This is here because artifacts can be run in any deck, so this will limit the amount that can be randomly generated in a deck")
    T2.configure(state='disabled')

    def generate_helper():
        """
        A helper method to call deck generation
        """
        setsToInclude = list(setCheckBar.state()) + list(setCheckBar2.state())
        normal_rarity_percents = [normalC.get("1.0",END), normalUC.get("1.0",END), normalR.get("1.0",END), normalM.get("1.0",END)]
        commander_rarity_percents = [commanderC.get("1.0",END), commanderUC.get("1.0",END), commanderR.get("1.0",END), commanderM.get("1.0",END)]
        land_rarity_percents = [landC.get("1.0",END), landUC.get("1.0",END), landR.get("1.0",END), landM.get("1.0",END)]
        artifact_percent = artifactPercent.get("1.0",END)
        basic_land_percent = landPercent.get("1.0",END)
        basic_land_percent_removal = landRPercent.get("1.0",END)
        deck_mode = gmVariable.get()
        numberOfLands = [minLand.get("1.0",END), maxLand.get("1.0",END)]
        possibleColorCombos = list(noColor.state()) + list(monoColor.state()) + list(dualColor.state()) + list(triColor.state()) + list(quadColor.state()) + list(allColor.state())
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

    Button(root, text='Quit', command=root.quit, height = 2, width = 5).place(x=460, y=10)
    Button(root, text='Generate', command=generate_helper, height = 2, width = 5).place(x=460, y=70)
    Button(root, text='Copy\nTo\nClipboard', command=copy_to_clipboard, height = 6, width = 5).place(x=540, y=10)

    root.mainloop()
        
#----------------------------------------------------------
