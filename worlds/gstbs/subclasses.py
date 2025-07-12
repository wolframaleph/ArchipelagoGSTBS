"""Module extending BaseClasses.py for Golden Sun The Broken Seal"""
from BaseClasses import Location, Item, Region

from .globals import GAME_NAME


class GSTBSLocation(Location):
    game: str = GAME_NAME


class GSTBSItem(Item):
    game: str = GAME_NAME


class GSTBSRegion(Region):
    game: str = GAME_NAME
