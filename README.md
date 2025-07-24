# Archipelago Extension - Golden Sun: The Broken Seal

Golden Sun is an RPG released by Camelot Software Planning in 2001. This project aims to add it to the list of games
compatible with [Archipelago](https://github.com/ArchipelagoMW/Archipelago).

Inspiration has been drawn from [GS-Randomizer](https://github.com/Valyssa/GS-Randomizer),
[gs2-randomiser2](https://github.com/Karanum/gs2-randomiser2), and
[the archiplago integration for Golden Sun: The Lost Age](https://github.com/cjmang/Archipelago). The eventual goal is
to reach feature parity with these projects as much as is reasonable.

Here's the tentative roadmap for the next few releases:

### alpha0.1
The initial release targets a minimal subset of the intended features.
* Archipelago multiworld integration
* Bizhawk client connection
* all chest and inspect locations in the randomization pool
* djinn location randomized amongst themselves, sorted by difficulty (from GS-Randomizer 2.0)
* optional removal of strength check to skew the Tolbi-bound ship off course
* consistent access to Crossbone Isle once it has been accessed with teleport
* optional altered Avoid functionality (from GS-Randomizer 2.0)
* optional altered Retreat functionality (from GS-Randomizer 2.0)
* optional cutscene skipping patch
* ROM patching (provided a legal English Language copy of Golden Sun by the user)

### alpha0.2
This release targets increased completion path variety.
* add reveal to the randomization pool
* add characters to the randomization pool (from GSTLA Randomizer)
* add consistend access to crossbone isle from Tolbi Docks
* provide a toggleable setting for fixing the Kalay Bridge Early
* provide a toggleable setting for moving the Gondowan Cave final move pillar one tile to the east, which will allow
  an alternative access path to Tolbi
* add the reverse Lamakan adventure to the randomization logic

### alpha0.3
This release targets the first alternative completion setting
* alternative win condition: defeat DeadBeard

### alpha0.4
This release targets the inclusion of many of the remaining features of the standalone randomizer into the project.
* psynergy learning curve rebalancing (from GS-Randomizer 2.0)
* challenge options like changing prices of inns and consumable (from GS-Randomizer 2.0)
* additional options like changing summon cost and damage (from GS-Randomizer 2.0)
* enemy moveset randomization (from GS-Randomizer 2.0)
* optional luck stat growth (from GS-Randomizer 2.0)
* random psynergy for psynergy consumables like Oil Drop (from GS-Randomizer 2.0)
* separate coin/exp scaling for bosses (from GS-Randomizer 2.0)
* character name, portrait, *etc.* randomization (from GS-Randomizer 2.0)
* option to learn psynergy to characters instead of equip items (from GSTLA Randomizer)
* add djinn to the archipelago randomization pool

### subsequent versions
* "offically" supported tracker integration
* option to enable different battle songs depending on the party leader
* equipment stats randomization
* weapon unleash randomization
* Iron Sun ruleset compatibility (from GS-Randomizer 2.0)
* "offically" supported tracker integration
* entrance and door randomization at a later date

&nbsp;

---

# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

Archipelago provides a generic framework for developing multiworld capability for game randomizers. In all cases,
presently, Archipelago is also the randomizer itself.

Currently, the following games are supported:

* The Legend of Zelda: A Link to the Past
* Factorio
* Subnautica
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
* ArchipIDLE
* Hollow Knight
* The Witness
* Sonic Adventure 2: Battle
* Starcraft 2
* Donkey Kong Country 3
* Dark Souls 3
* Super Mario World
* Pokémon Red and Blue
* Hylics 2
* Overcooked! 2
* Zillion
* Lufia II Ancient Cave
* Blasphemous
* Wargroove
* Stardew Valley
* The Legend of Zelda
* The Messenger
* Kingdom Hearts 2
* The Legend of Zelda: Link's Awakening DX
* Adventure
* DLC Quest
* Noita
* Undertale
* Bumper Stickers
* Mega Man Battle Network 3: Blue Version
* Muse Dash
* DOOM 1993
* Terraria
* Lingo
* Pokémon Emerald
* DOOM II
* Shivers
* Heretic
* Landstalker: The Treasures of King Nole
* Final Fantasy Mystic Quest
* TUNIC
* Kirby's Dream Land 3
* Celeste 64
* Castlevania 64
* A Short Hike
* Yoshi's Island
* Mario & Luigi: Superstar Saga
* Bomb Rush Cyberfunk
* Aquaria
* Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006
* A Hat in Time
* Old School Runescape
* Kingdom Hearts 1
* Mega Man 2
* Yacht Dice
* Faxanadu
* Saving Princess
* Castlevania: Circle of the Moon
* Inscryption
* Civilization VI
* The Legend of Zelda: The Wind Waker
* Jak and Daxter: The Precursor Legacy
* Super Mario Land 2: 6 Golden Coins
* shapez
* Paint

For setup and instructions check out our [tutorials page](https://archipelago.gg/tutorial/).
Downloads can be found at [Releases](https://github.com/ArchipelagoMW/Archipelago/releases), including compiled
windows binaries.

## History

Archipelago is built upon a strong legacy of brilliant hobbyists. We want to honor that legacy by showing it here.
The repositories which Archipelago is built upon, inspired by, or otherwise owes its gratitude to are:

* [bonta0's MultiWorld](https://github.com/Bonta0/ALttPEntranceRandomizer/tree/multiworld_31)
* [AmazingAmpharos' Entrance Randomizer](https://github.com/AmazingAmpharos/ALttPEntranceRandomizer)
* [VT Web Randomizer](https://github.com/sporchia/alttp_vt_randomizer)
* [Dessyreqt's alttprandomizer](https://github.com/Dessyreqt/alttprandomizer)
* [Zarby89's](https://github.com/Ijwu/Enemizer/commits?author=Zarby89)
  and [sosuke3's](https://github.com/Ijwu/Enemizer/commits?author=sosuke3) contributions to Enemizer, which make up the
  vast majority of Enemizer contributions.

We recognize that there is a strong community of incredibly smart people that have come before us and helped pave the
path. Just because one person's name may be in a repository title does not mean that only one person made that project
happen. We can't hope to perfectly cover every single contribution that lead up to Archipelago, but we hope to honor
them fairly.

### Path to the Archipelago

Archipelago was directly forked from bonta0's `multiworld_31` branch of ALttPEntranceRandomizer (this project has a
long legacy of its own, please check it out linked above) on January 12, 2020. The repository was then named to
_MultiWorld-Utilities_ to better encompass its intended function. As Archipelago matured, then known as
"Berserker's MultiWorld" by some, we found it necessary to transform our repository into a root level repository
(as opposed to a 'forked repo') and change the name (which came later) to better reflect our project.

## Running Archipelago

For most people, all you need to do is head over to
the [releases page](https://github.com/ArchipelagoMW/Archipelago/releases), then download and run the appropriate
installer, or AppImage for Linux-based systems.

If you are a developer or are running on a platform with no compiled releases available, please see our doc on
[running Archipelago from source](docs/running%20from%20source.md).

## Related Repositories

This project makes use of multiple other projects. We wouldn't be here without these other repositories and the
contributions of their developers, past and present.

* [z3randomizer](https://github.com/ArchipelagoMW/z3randomizer)
* [Enemizer](https://github.com/Ijwu/Enemizer)
* [Ocarina of Time Randomizer](https://github.com/TestRunnerSRL/OoT-Randomizer)

## Contributing

To contribute to Archipelago, including the WebHost, core program, or by adding a new game, see our
[Contributing guidelines](/docs/contributing.md).

## FAQ

For Frequently asked questions, please see the website's [FAQ Page](https://archipelago.gg/faq/en/).

## Code of Conduct

Please refer to our [code of conduct](/docs/code_of_conduct.md).
