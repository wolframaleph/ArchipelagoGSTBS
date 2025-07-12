# import Archipelago libraries
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World

# If imported names pile up, it may be easier to use from . import options
# and access the variable as options.MyGameOptions. - From the API docs
from .globals import GSTBS_ROOT_DIR, GSTBS_DEBUG, GAME_NAME
from .options.options import GSTBSOptions
from .regions import create_regions, connect_entrances
from .locations import location_data_table, location_name_to_id
from .items import create_item, create_items, item_name_to_id
from .rules import set_rules
# from .utils import draw_puml  # not needed until logic implementation


class GSTBSWebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Golden Sun: The Broken Seal with Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Various"]
    )

    tutorials = [setup_en]
    game_info_languages = ["en"]
    # bug_report_page = ""  # we can link to the github issues page once we publish
    # rich_text_options_doc = True  # we can write the options documentation as reStructuredText


class GSTBSWorld(World):
    """
    Save the world!
    """

    # set world metadata
    game = GAME_NAME  # The name of the game info page must match this string, prefixed by language
    web = GSTBSWebWorld()
    options_dataclass = GSTBSOptions
    options: GSTBSOptions
    # required_client_version = (0, 5, 0)  # upcoming version no longer requires unique ids
    # origin_region_name = "Menu"  # use this to set an alternate starting region name

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    # For more information on what can be defined in the GSTBSWorld class and how it is called by AP, visit
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#implementation

    # called per player before any items or locations are created
    # we could use this to choose the rules if we have different goal modes down
    # def generate_early(self) -> None: pass

    # called to place player’s regions and their locations into the MultiWorld’s regions list
    create_regions = create_regions

    # called to place player’s items into the MultiWorld’s itempool. By the end of this step all regions, locations
    # and items have to be in the MultiWorld’s regions and itempool
    create_items = create_items

    # # called to set access and item rules on locations and entrances
    # set_rules = set_rules

    # by the end of this step, all entrances must exist and be connected to their source and target regions.
    connect_entrances = connect_entrances

    # # this is just the last of the fucntions to be called, so the draw puml is placed here for now
    # def post_fill(self) -> None:
    #     if GSTBS_DEBUG:
    #         draw_puml(self, GSTBS_ROOT_DIR / "debug" / "world.puml")

    # required for generation, see
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#generation
    create_item = create_item
