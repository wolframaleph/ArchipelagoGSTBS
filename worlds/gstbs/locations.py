from typing import TypedDict


# Typed dictionaryies are much more performant than dataclasses
class GSTBSLocationDict(TypedDict, total=False):
    name: str
    region: str
    locked_item: str


gstbs_events: dict[str, str] = {}

# storing the item data directly in python is the most efficient way for AP worlds
# refer to the Subnautica implementation to see how this format was laid out
location_data_table: dict[int, GSTBSLocationDict] = {}  # TODO Set up jinja

locked_locations_addresses: list[int] = [addr for addr, data in location_data_table.items() if data.get("locked_item")]

location_name_to_id: dict[str, int] = {data["name"]: address for address, data in location_data_table.items()}

# create_location() and create_locations() do not need to be defined, as location creation is
# handled in the `create_regions` method in the `GSTBSRegionHandler` in `regions.py`
