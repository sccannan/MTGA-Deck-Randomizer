#!/usr/bin/env python3
import json
from random import randint
import tkinter
from tkinter import *

#---------------------------------------------------------
#---------------------------------------------------------
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], toSelect=0):
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
        return map((lambda var: var.get()), self.vars)
#---------------------------------------------------------
#---------------------------------------------------------

#---------------------------------------------------------
#---------------------------------------------------------
"""Makes sure all passed in information is valid (correct typing, values, etc)
   Should be captured by html code, but now we can double check and catch from a command line run

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

Returns:
    str: Either an error message on failure, or a string representation of the deck size
    list: The sets to include
    list: The possibleColorCombos
"""
def verifyInformation(sets, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands):

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
        return("Error! There are only 4 rarities in MTG - the provided normal rarities list has", len(normal_rarity_percents)), [], []
    if len(commander_rarity_percents) != 4:
        return("Error! There are only 4 rarities in MTG - the provided commander rarities list has", len(commander_rarity_percents)), [], []
    if len(land_rarity_percents) != 4:
        return("Error! There are only 4 rarities in MTG - the provided land rarities has", len(land_rarity_percents)), [], []
    for x in range(4):
        try:
            normal_rarity_percents[x] = float(normal_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for normal rarity decimals"), [], []
        if normal_rarity_percents[x] < 0:
            return("Error! Negative value detected for normal rarity decimals"), [], []
        try:
            commander_rarity_percents[x] = float(commander_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for commander rarity decimals"), [], []
        if commander_rarity_percents[x] < 0:
            return("Error! Negative value detected for commander rarity decimals"), [], []
        try:
            land_rarity_percents[x] = float(land_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for land rarity decimals"), [], []
        if land_rarity_percents[x] < 0:
            return("Error! Negative value detected for land rarity decimals"), [], []
    if sum(normal_rarity_percents) != 1:
        return("Error! Normal rarity decimals dont equal 1"), [], []
    if sum(commander_rarity_percents) != 1:
        return("Error! Commander rarity decimals dont equal 1"), [], []
    if sum(land_rarity_percents) != 1:
        return("Error! Land rarity decimals dont equal 1"), [], []

    #Makes sure artifact percentage is 0<x<1 and is a number
    try:
        artifact_percent = float(artifact_percent)
    except:
        return("Error! Non numeric value detected for artifact percentage"), [], []
    if artifact_percent > 1 or artifact_percent < 0:
        return("Error! Artifact percentage decimal isnt between 0 and 1"), [], []

    #Makes sure basic lands percentage is 0<x<1 and is a number
    try:
        basic_land_percent = float(basic_land_percent)
    except:
        return("Error! Non numeric value detected for basic land percentage"), [], []
    if basic_land_percent > 1 or basic_land_percent < 0:
        return("Error! Basic land percentage decimal isnt between 0 and 1"), [], []

    #Makes sure basic lands removal percentage is 0<x<1 and is a number
    try:
        basic_land_percent_removal = float(basic_land_percent_removal)
    except:
        return("Error! Non numeric value detected for basic land removal percentage decimal"), [], []
    if basic_land_percent_removal > 1 or basic_land_percent_removal < 0:
        return("Error! Basic land removal percentage decimal isnt between 0 and 1"), [], []

    #Make sure the deck mode is supported
    if deck_mode.lower() != "brawl" and deck_mode.lower() != "standard":
        return("Error! Unsupported deck mode! Current options are brawl and standard"), [], []
    
    #Set the deck size
    deck_size = 0
    if deck_mode.lower() == "brawl" or deck_mode.lower() == "standard":
        deck_size = "60"

    #Make sure the number of lands is valid
    try:
        min_lands = int(round(float(numberOfLands[0])))
        max_lands = int(round(float(numberOfLands[1])))
    except:
        return("Error! Non numeric value detected for minimum and/or maximum number of lands"), [], []
    if min_lands > max_lands:
        return("Error! Minimum lands must be less than or equal too maximum lands"), [], []
    if max_lands > int(deck_size):
        return("Error! Maximum lands must be less than or equal too the maximum deck size"), [], []
    return deck_size, setsToInclude, ccToInclude
#----------------------------------------------------------
#----------------------------------------------------------

#----------------------------------------------------------
#----------------------------------------------------------
"""Loads the JSONs and returns a list for normal cards, commanders, and lands

Args:
    setsToInclude (list): A list of sets you want to pull from
    
Returns:
    list: A list of normal cards
    list: A list of commander cards
    list: A list of land cards
"""
def load_json_sets(setsToInclude, deck_mode):
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
"""Removes all cards that are not in the specified color

Args:
    card_list (list): A list of cards
    colorCombo (str): The color combo you have

Returns:
    list: A list of cards with colors now removed
"""
def color_removal(card_list, colorCombo):
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
def pick_a_card(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, landFlag, deck_mode):
    
    #See if you are picking a basic land -- we check the first uncommon card, all card types have uncommons


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
        if ((deck_mode == "brawl" and card_list[mode][randomIndex][0] not in deck) or (deck_mode == "standard")):
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
"""A helper function for picking a card

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
def pick_a_card_helper(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops, landFlag, deck_mode):
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
"""Turns the deck into an MTGA formatted string

Args:
    deck (list): A list of each card in the deck
    deck_size (int): How large the deck is, not including the sideboard
    sideBoard (bool): True if there is a sideBoard present
    deck_mode (str): The deck mode

Returns:
    str: The MTGA formatted string of the deck
"""
def print_deck(deck, deck_size, sideBoard, deck_mode):
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

#----------------------------------------------------------
#Main method, used for generating a deck
#----------------------------------------------------------
def generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard):

    retCode, setsToInclude, possibleColorCombos = verifyInformation(setsToInclude, possibleColorCombos, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands)

    deck_size = 0
    try:
        deck_size = int(retCode)
    except:
        return retCode
    deck_mode = deck_mode.lower()
    artifact_percent = float(artifact_percent)
    basic_land_percent = float(basic_land_percent)
    numberOfLands[0] = int(round(float(numberOfLands[0])))
    numberOfLands[1] = int(round(float(numberOfLands[1]))) 

    normal, commander, land = load_json_sets(setsToInclude, deck_mode)
    colorCombo = ""
    deckCMC = [0, 0, 0, 0, 0, 0] #R, W, B, U, G, Colorless
    deck = []

    #If standard, pick a color combo
    if deck_mode == "standard":
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
#Main
#----------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    root.geometry("1500x520")

    #Sets
    setLabel = Label(root, text="Sets")
    setLabel.place(x=10, y=10)
    setCheckBar = Checkbar(root, ["DOM","HA1","HA2","HA3","E02","RIX","M19","GRN","RNA","WAR","M20","ELD","THB","IKO","M21"])
    setCheckBar.place(x=10, y=30)
    setCheckBar.config(relief=GROOVE, bd=2)

    #Mana Colors
    manaLabel = Label(root, text="Mana Colors")
    manaLabel.place(x=10, y=60)
    manaFrame = Frame(root)
    manaFrame.pack()
    manaFrame.place(x=10, y=80)
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
    normalCard.place(x=10, y=230)
    normalFrame = Frame(root)
    normalFrame.pack()
    normalFrame.place(x=10, y=250)
    Label(normalFrame, text="Common").grid(row=0)
    Label(normalFrame, text="Uncommon").grid(row=1)
    Label(normalFrame, text="Rare").grid(row=2)
    Label(normalFrame, text="Mythic").grid(row=3)
    normalC = Entry(normalFrame)
    normalUC = Entry(normalFrame)
    normalR = Entry(normalFrame)
    normalM = Entry(normalFrame)
    normalC.insert(10, ".15")
    normalUC.insert(10, ".75")
    normalR.insert(10, ".10")
    normalM.insert(10, ".00")
    normalC.grid(row=0, column=1)
    normalUC.grid(row=1, column=1)
    normalR.grid(row=2, column=1)
    normalM.grid(row=3, column=1)
    normalFrame.config(relief=GROOVE, bd=2)

    #Commander Cards
    commanderCard = Label(root, text="Commander Card Rarities")
    commanderCard.place(x=270, y=230)
    commanderFrame = Frame(root)
    commanderFrame.pack()
    commanderFrame.place(x=270, y=250)
    Label(commanderFrame, text="Common").grid(row=0)
    Label(commanderFrame, text="Uncommon").grid(row=1)
    Label(commanderFrame, text="Rare").grid(row=2)
    Label(commanderFrame, text="Mythic").grid(row=3)
    commanderC = Entry(commanderFrame)
    commanderUC = Entry(commanderFrame)
    commanderR = Entry(commanderFrame)
    commanderM = Entry(commanderFrame)
    commanderC.insert(10, ".00")
    commanderUC.insert(10, ".25")
    commanderR.insert(10, ".50")
    commanderM.insert(10, ".25")
    commanderC.grid(row=0, column=1)
    commanderUC.grid(row=1, column=1)
    commanderR.grid(row=2, column=1)
    commanderM.grid(row=3, column=1)
    commanderFrame.config(relief=GROOVE, bd=2)

    #Land Cards
    landCard = Label(root, text="Land Card Rarities")
    landCard.place(x=10, y=350)
    landFrame = Frame(root)
    landFrame.pack()
    landFrame.place(x=10, y=370)
    Label(landFrame, text="Common").grid(row=0)
    Label(landFrame, text="Uncommon").grid(row=1)
    Label(landFrame, text="Rare").grid(row=2)
    Label(landFrame, text="Mythic").grid(row=3)
    landC = Entry(landFrame)
    landUC = Entry(landFrame)
    landR = Entry(landFrame)
    landM = Entry(landFrame)
    landC.insert(10, ".50")
    landUC.insert(10, ".50")
    landR.insert(10, ".00")
    landM.insert(10, ".00")
    landC.grid(row=0, column=1)
    landUC.grid(row=1, column=1)
    landR.grid(row=2, column=1)
    landM.grid(row=3, column=1)
    landFrame.config(relief=GROOVE, bd=2)

    #Mana/Land Fixing
    landMana = Label(root, text="Lands")
    landMana.place(x=270, y=350)
    landManaFrame = Frame(root)
    landManaFrame.pack()
    landManaFrame.place(x=270, y=370)
    Label(landManaFrame, text="Basic Land Percentage").grid(row=0)
    Label(landManaFrame, text="Basic Land Removal Percentage").grid(row=1)
    Label(landManaFrame, text="Minimum Lands").grid(row=2)
    Label(landManaFrame, text="Maxmimum").grid(row=3)
    landPercent = Entry(landManaFrame)
    landRPercent = Entry(landManaFrame)
    minLand = Entry(landManaFrame)
    maxLand = Entry(landManaFrame)
    landPercent.insert(10, ".90")
    landRPercent.insert(10, ".10")
    minLand.insert(10, "23")
    maxLand.insert(10, "27")
    landPercent.grid(row=0, column=1)
    landRPercent.grid(row=1, column=1)
    minLand.grid(row=2, column=1)
    maxLand.grid(row=3, column=1)
    landManaFrame.config(relief=GROOVE, bd=2)

    #Misc
    misc = Label(root, text="Misc")
    misc.place(x=530, y=230)
    miscFrame = Frame(root)
    miscFrame.pack()
    miscFrame.place(x=530, y=250)
    Label(miscFrame, text="Artifact Percent").grid(row=0)
    Label(miscFrame, text="Game Mode").grid(row=1)
    artifactPercent = Entry(miscFrame)
    gameMode = Entry(miscFrame)
    artifactPercent.insert(10, ".25")
    gameMode.insert(10, "Brawl")
    artifactPercent.grid(row=0, column=1)
    gameMode.grid(row=1, column=1)
    sideBoardPointer = IntVar()
    sideBoard = Checkbutton(miscFrame, text="Sideboard?", variable=sideBoardPointer)
    sideBoard.grid(row=2, column=0)
    miscFrame.config(relief=GROOVE, bd=2)

    #Deck Output
    S = Scrollbar(root)
    T = Text(root, height=50, width=70)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=RIGHT)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(END, "Your deck will generate here!")

    def allstates():
        setsToInclude = list(setCheckBar.state())
        normal_rarity_percents = [normalC.get(), normalUC.get(), normalR.get(), normalM.get()]
        commander_rarity_percents = [commanderC.get(), commanderUC.get(), commanderR.get(), commanderM.get()]
        land_rarity_percents = [landC.get(), landUC.get(), landR.get(), landM.get()]
        artifact_percent = artifactPercent.get()
        basic_land_percent = landPercent.get()
        basic_land_percent_removal = landRPercent.get()
        deck_mode = gameMode.get()
        numberOfLands = [minLand.get(), maxLand.get()]
        possibleColorCombos = list(noColor.state()) + list(monoColor.state()) + list(dualColor.state()) + list(triColor.state()) + list(quadColor.state()) + list(allColor.state())
        sideBoard = sideBoardPointer.get()
        T.delete('1.0', END)
        T.insert(END, generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard))

    Button(root, text='Quit', command=root.quit).place(x=10, y=470)
    Button(root, text='Generate', command=allstates).place(x=80, y=470)
    
    root.mainloop()
        
#----------------------------------------------------------
