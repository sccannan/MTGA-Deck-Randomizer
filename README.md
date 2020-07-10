# MTGA Deck Randomizer
A random deck maker for MTGA

## What is this?
This application is a way for a user to randomly generate a Magic the Gathering Arena. Based on the settings from the GUI, a random deck will be generated. All cards have equal % of being chosen, regardless if how many sets they have been in (the odds of getting the card "Opt" is the same as any other card, even though it's in multiple sets) Additionally, split mana cards are only put into decks with BOTH of the colors for simiplicities sake.

![Alt text](gui.png?raw=true "Title")

## Supported Game Modes
* Historic and Traditional Historic
	* 60+ cards, historic legal
* Standard and Traditional Standard
	* 60+ cards, standard legal
* Brawl
	* 59 unique cards, 1 unique commander, standard legal
* Friendly Brawl
	* 59 unique cards, 1 unique commander, historic legal
* Singleton
	* 60 unique cards, standard legal
* Artisan
	* 60-250 cards, historic legal, commons or uncommons only
* Pauper 
	* 60+ cards, standard legal, commons only

## Usage
### Installation
* This program requires python3, which a guide for installation can be downloaded [HERE](https://wiki.python.org/moin/BeginnersGuide/Download)
* This program requires tkinter, which a guide for installation can be downloaded [HERE](https://tkdocs.com/tutorial/install.html)

### Running the program
* To run the program in Windows, simply double click on "randomizer.py". For Linux/MacOS, in the terminal navigate to the directory where "randomizer.py" is and do "python3 randomizer.py"

## Key
* Sets: Check the sets you want to play with
	* DOM = Domanaria
	* HA1 = Historic Anthology 1
	* HA2 = Historic Anthology 2
	* HA3 = Historic Anthology 3
	* E02 = Ixalan
	* RIX = Rivals of Ixalan
	* M19 = Core 2019
	* GRN = Guilds of Ravnica
	* RNA = Ravnica Allegiance
	* WAR = War of the Spark
	* M20 = Core 2020
	* ELD = Throne of Eldraine
	* THB = Theros Beyond Death
	* IKO = Ikoria
	* M21 = Core 2021
* Mana Colors: Check the mana colors you want your deck possibly being
	* R = Red
	* W = White
	* G = Green
	* U = Blue
	* B = Black
* Rarities: The odds you want to get a card of a certain rarity. For example, normal common = .25 means there's a 25% chance, for each normal card in your deck, it will be a common
* Basic Land Percentage: The odds that for each land, it will be a basic land. This is applied before checking the rarity of each land
* Basic Land Removal Percentage: For each color in your deck past the first, this number will get subtracted from Basic Land Percentage so that the more colors in your deck, the more likely you will get non basic lands, which wil help with mana fixing
* Artifact Percentage: The odds that you will randomly select an artifact. This is here because artifacts can be run in any deck, so this will limit the amount that can be randomly generated in a deck

## Link for JSONS
All credit for the JSON files that list all the cards go to [MTGJSON](https://mtgjson.com/)

## Pydocs
To generate HTML documentation for this program issue the command: pydoc3 -w randomizer

## TODO
* Make Unit Tests?
* Supports All MTGA Games Modes
	* Direct Game
	* Limited
* Need to make sure all the cards are in each set
