# MTGA Deck Randomizer
A random deck generator for MTGA

## What is this?
This application is a way for a user to randomly generate a Magic the Gathering Arena deck. Based on the settings from the GUI, a random deck will be generated. From there, launch MTGA and go to the "Deck" tab. Then hit import deck. All cards have equal chance of being chosen, regardless if how many sets they have been in (the odds of getting the card "Opt" is the same as any other card, even though it's in multiple sets). Additionally, split mana cards are only put into decks with BOTH of the colors for simiplicities sake.

![Example GUI](GUI.png?raw=true "GUI")

## Supported Game Modes
* Historic and Traditional Historic
	* 60+ cards, historic legal, 4 similar card max
* Standard and Traditional Standard
	* 60+ cards, standard legal, 4 similar card max
* Brawl
	* 59 unique cards, 1 unique commander, standard legal
* Friendly Brawl
	* 59 unique cards, 1 unique commander, historic legal
* Singleton
	* 60 unique cards, standard legal
* Artisan
	* 60-250 cards, historic legal, commons or uncommons only, 4 similar card max
* Pauper 
	* 60+ cards, standard legal, commons only, 4 similar card max
* Limited
	* 40+ cards
* Direct Game
	* 60+ cards, historic legal, 4 similar card max

## Usage
### Installation
* This program requires python3, which a guide for installation can be downloaded [HERE](https://wiki.python.org/moin/BeginnersGuide/Download)

### Running the program
* To run the program in Windows, simply double click on "randomizer.py". For Linux/MacOS, in the terminal navigate to the directory where "randomizer.py" is and do "python3 randomizer.py"

## Key
* Sets: Check the sets you want to play with
	* DOM = Domanaria
	* HA1 = Historic Anthology 1
	* HA2 = Historic Anthology 2
	* HA3 = Historic Anthology 3
	* XLN = Ixalan
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
* Mana Colors: Check the mana colors you want your deck possibly being. If you have "R", "W", and "RW", theres a 33% chance your deck is only Red, a 33% chance your deck is only White, and a 33% chance your deck is Red and White
	* R = Red
	* W = White
	* G = Green
	* U = Blue
	* B = Black
* Rarities: The odds you want to get a card of a certain rarity. For example, normal common = .25 means there's a 25% chance, for each normal card in your deck, it will be a common. Normal cards are all non land cards, commanders are all legendary creatures/planeswalkers, and lands are all non basic land cards.
* Basic Land Percentage: The odds that for each land, it will be a basic land. This is applied before checking the rarity of each land
* Basic Land Removal Percentage: For each color in your deck past the first, this number will get subtracted from Basic Land Percentage so that the more colors in your deck, the more likely you will get non basic lands, which will help with mana fixing
* Artifact Percentage: The odds that you will randomly select an artifact. This is here because artifacts can be run in any deck, so this will limit the amount that can be randomly generated in a deck

## Link for JSONS
All credit for the JSON files that list all the cards goes to [MTGJSON](https://mtgjson.com/)

## Pydocs
To generate HTML documentation for this program issue the command: pydoc3 -w randomizer

##TODO
* Clear button for each block
* Reset button for entire thing (brings everything back to default)
