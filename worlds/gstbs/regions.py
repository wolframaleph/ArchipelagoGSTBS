from typing import TYPE_CHECKING

from BaseClasses import Region, ItemClassification

from .subclasses import GSTBSLocation
from .locations import location_data_table, locked_locations_addresses, gstbs_events
from .items import GSTBSItem, create_item

if TYPE_CHECKING:
    from . import GSTBSWorld
    # from .options import Goal  # not currently needed

region_data_table: dict[str, list[str]] = {
    # The starting region default name is "Menu", but it can be renamed
}


def create_regions(world: "GSTBSWorld") -> None:
    # Create regions and store until end of function call
    gstbs_regions: dict[str, Region] = dict()
    for region_name in region_data_table.keys():
        # Create region
        region = Region(region_name, world.player, world.multiworld)
        # Create locations in regions
        # locations: dict[str, int] = dict()  # currently unused
        for location_addr, location_data in location_data_table.items():
            if location_data["region"] == region_name:
                location: GSTBSLocation = GSTBSLocation(world.player, location_data["name"], location_addr, region)
                if location_data.get("locked_item"):
                    location.place_locked_item(create_item(world, location_data["locked_item"]))
                region.locations.append(location)
        gstbs_regions.update({region_name: region})

    # Create events
    goal_event_name = world.options.goal.get_event_name()
    for event_name, event_region in gstbs_events.items():
        target_region = gstbs_regions[event_region]
        event_loc = GSTBSLocation(world.player, event_name, None, target_region)
        event_loc.place_locked_item(
            GSTBSItem(event_name, ItemClassification.progression, None, player=world.player))
        if event_name == goal_event_name:
            # make the goal event the victory "item"
            event_loc.item.name = "Victory!"
        target_region.locations.append(event_loc)

    # Add regions to multiworld
    for region in gstbs_regions.values():
        world.multiworld.regions.append(region)


def connect_entrances(world: "GSTBSWorld") -> None:
    for region_name, connecting_regions in region_data_table.items():
        region = world.get_region(region_name)
        for conn_name in connecting_regions:
            region.connect(world.get_region(conn_name))
