# MTGA Deck Randomizer
A random deck generator for MTGA

## What is this?
This application is a way for a user to randomly generate a Magic the Gathering Arena deck. Based on the settings from the GUI, a random deck will be generated. From there, launch MTGA and go to the "Deck" tab. Then hit import deck. All cards have equal chance of being chosen, regardless if how many sets they have been in (the odds of getting the card "Opt" is the same as any other card, even though it's in multiple sets). Companions are disabled for simplicities sake.

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
	* DOM = Dominaria
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

## Algorithm 
* 1) Verify all the information the user has entered and translate it to the format the program wants. If the user entered bad information, error and tell them.
* 2) Based on the sets and the game mode the user specified, load all the cards from those sets that are legal, keeping track of the name, color identity, converted mana cost (CMC), and type (Land, Creature, etc).
* 3) If the game mode is brawl or friendly brawl, randomly select a commander based on the commander rarities that fits one of the user specified color combinations. If the game mode is not brawl, randomly choose a user specified color combination for the deck.
* 4) Remove all cards that are not of the color combination we chose, leaving only usable cards of the colors we want. All colorless cards (things like artifacts), will not be removed.
* 5) Start randomly selecting non lands from the pool of remaining cards, based on the normal rarities. You choose (deck size specified) - (maximum number of lands) non land cards.
* 6) Start randomly selecting lands. First, see if you want a basic, and if you do count the colored mana symbols for every card in your deck. Then, based on the colors (more symbols of one color means better odds of selecting the corresponding basic land), choose a land. If you don’t pick a basic see what rarity land you want and choose from the pool. In both cases, keep track of the colors the land produces so next time you pick a land, you can subtract the symbols you already have from the symbols counted from the deck (this way you should get a mixture of lands based off the colors and amounts you need). You choose (minimum number of lands + average CMC of cards in your deck) lands, or the maximum number of lands if the previous number is bigger.
* 7) Fill in the rest of your deck (if needed) with more non land cards (same as 5). You choose (deck size) - (number of cards already in your deck) non land cards.
* 8) Possibly select a sideboard of 15 non land cards (same as 5).
* 9) Print the deck.

## Link for JSONS
All credit for the JSON files that list all the cards goes to [MTGJSON](https://mtgjson.com/)

## Pydocs
To generate HTML documentation for this program issue the command: pydoc3 -w randomizer
