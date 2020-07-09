#!/usr/bin/env python3
import json
from random import randint

#---------------------------------------------------------
#---------------------------------------------------------
"""Makes sure all passed in information is valid (correct typing, values, etc)
   Should be captured by html code, but now we can double check and catch from a command line run

Args:
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
"""
def verifyInformation(normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands):

    #Make sure the normal/commander/land percentages are numbers, total 1, there are no negative values, and that there are only 4 values present
    if len(normal_rarity_percents) != 4:
        return("Error! There are only 4 rarities in MTG - the provided normal rarities list has", len(normal_rarity_percents))
    if len(commander_rarity_percents) != 4:
        return("Error! There are only 4 rarities in MTG - the provided commander rarities list has", len(commander_rarity_percents))
    if len(land_rarity_percents) != 4:
        return("Error! There are only 4 rarities in MTG - the provided land rarities has", len(land_rarity_percents))
    for x in range(4):
        try:
            normal_rarity_percents[x] = float(normal_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for normal rarity decimals")
        if normal_rarity_percents[x] < 0:
            return("Error! Negative value detected for normal rarity decimals")
        try:
            commander_rarity_percents[x] = float(commander_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for commander rarity decimals")
        if commander_rarity_percents[x] < 0:
            return("Error! Negative value detected for commander rarity decimals")
        try:
            land_rarity_percents[x] = float(land_rarity_percents[x])
        except:
            return("Error! Non numeric value detected for land rarity decimals")
        if land_rarity_percents[x] < 0:
            return("Error! Negative value detected for land rarity decimals")
    if sum(normal_rarity_percents) != 1:
        return("Error! Normal rarity decimals dont equal 1")
    if sum(commander_rarity_percents) != 1:
        return("Error! Commander rarity decimals dont equal 1")
    if sum(land_rarity_percents) != 1:
        return("Error! Land rarity decimals dont equal 1")

    #Makes sure artifact percentage is 0<x<1 and is a number
    try:
        artifact_percent = float(artifact_percent)
    except:
        return("Error! Non numeric value detected for artifact percentage")
    if artifact_percent > 1 or artifact_percent < 0:
        return("Error! Artifact percentage decimal isnt between 0 and 1")

    #Makes sure basic lands percentage is 0<x<1 and is a number
    try:
        basic_land_percent = float(basic_land_percent)
    except:
        return("Error! Non numeric value detected for basic land percentage")
    if basic_land_percent > 1 or basic_land_percent < 0:
        return("Error! Basic land percentage decimal isnt between 0 and 1")

    #Makes sure basic lands removal percentage is 0<x<1 and is a number
    try:
        basic_land_percent_removal = float(basic_land_percent_removal)
    except:
        return("Error! Non numeric value detected for basic land removal percentage decimal")
    if basic_land_percent_removal > 1 or basic_land_percent_removal < 0:
        return("Error! Basic land removal percentage decimal isnt between 0 and 1")

    #Make sure the deck mode is supported
    if deck_mode != "brawl" and deck_mode != "standard":
        return("Error! Unsupported deck mode! Current options are brawl and standard")
    
    #Set the deck size
    deck_size = 0
    if deck_mode == "brawl" or deck_mode == "standard":
        deck_size = "60"

    #Make sure the number of lands is valid
    try:
        min_lands = int(round(numberOfLands[0]))
        max_lands = int(round(numberOfLands[1]))
    except:
        return("Error! Non numeric value detected for minimum and/or maximum number of lands")
    if min_lands > max_lands:
        return("Error! Minimum lands must be less than or equal too maximum lands")
    if max_lands > int(deck_size):
        return("Error! Maximum lands must be less than or equal too the maximum deck size")
    return deck_size
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
            if (x["legalities"][deck_mode] == "Legal" and cardName not in all_card_names):

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

Returns:
    list: A list of card names in the deck after the new card has been picked
    list: A list of the number of colored and colorless mana symbols after the new card has been picked
    str: The color identity of the card that was just added
"""
def pick_a_card(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent):
    
    #See if you are picking a basic land -- we check the first uncommon card, all card types have uncommons
    if card_list[1][0][2] == -1 and card_list[1][0][3] == -1 and randint(0, 100) < 100*basic_land_percent:

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

Returns:
    list: A list of card names in the deck after the new card has been picked
    list: A list of the number of colored and colorless mana symbols after the new card has been picked
    str: The color identity of the card that was just added
    str: Null if correct, error message if error
"""
def pick_a_card_helper(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops):
    attempts = 0
    while len(deck) < numberOfLoops:
        deck, deckCMC, color = pick_a_card(card_list, rarityPercents, deckCMC, deck, artifact_percent, basic_land_percent)
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

Returns:
    str: The MTGA formatted string of the deck
"""
def print_deck(deck, deck_size, sideBoard):
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

    retCode = verifyInformation(normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands)

    deck_size = 0
    try:
        deck_size = int(retCode)
    except:
        return retCode

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
            deck, deckCMC, colorCombo = pick_a_card(commander, commander_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent)
            attempts = attempts + 1
            if colorCombo not in possibleColorCombos:
                deck = []
                deckCMC = [0, 0, 0, 0, 0, 0]
            if attempts > 1000:
                return("Warning! After 1000 attempts, a commander could not be found. Please change your rarity values to allow for more cards to be chosen")

    #The more colors in your deck, the less likely you are to get basics
    if len(colorCombo) > 1:
        basic_land_percent = basic_land_percent - (len(colorCombo) * basic_land_percent_removal)

    #Remove all cards that are not part of the colorCombo
    normal = color_removal(normal, colorCombo)
    land = color_removal(land, colorCombo)

    #Start picking normal cards
    numberOfLoops = deck_size - numberOfLands[1] - len(deck)
    deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops)
    if error != "":
        return(error)

    #Calculate the average cmc of the deck
    averageCMC = int(round(sum(deckCMC)/len(deck)))
    numLands = numberOfLands[0] + averageCMC - 1
    if numLands > numberOfLands[1]:
        numLands = numberOfLands[1]

    #Start picking lands
    numberOfLoops = len(deck) + numLands
    deck, deckCMC, colorCombo, error = pick_a_card_helper(land, land_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, numberOfLoops)
    if error != "":
        return(error)

    #Might need to pick more cards
    deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, deck_size)
    if error != "":
        return(error)

    #Sideboard
    if sideBoard == True:
        deck, deckCMC, colorCombo, error = pick_a_card_helper(normal, normal_rarity_percents, deckCMC, deck, artifact_percent, basic_land_percent, deck_size+15)
        if error != "":
            return(error) 

    #Print deck
    return(print_deck(deck, deck_size, sideBoard))
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

    #Sort all the color combos
    for x in range(len(possibleColorCombos)):
        possibleColorCombos[x] = "".join(sorted(possibleColorCombos[x]))

    #TODO -- should be a checkbox
    sideBoard = False

    print(generateDeck(setsToInclude, normal_rarity_percents, commander_rarity_percents, land_rarity_percents, artifact_percent, basic_land_percent, basic_land_percent_removal, deck_mode, numberOfLands, possibleColorCombos, sideBoard))    
#----------------------------------------------------------
