from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions


class Goal(Choice):
    """
    Test Mode: Self explanatory. Will be removed on first alpha release
    Classic Mode: Progress through the game normally.
    """
    auto_display_name = True
    display_name = "Goal"
    option_test = -1
    # option_normal = 0
    default = -1  # test is only set as default for now.

    def get_event_name(self) -> str:
        return {
            self.option_test: "Test Cleared!",
            # self.option_normal: "Victory!"
        }[self.value]


@dataclass
class GSTBSOptions(PerGameCommonOptions):
    goal: Goal
    # for information on what other common options are present in this class's parent class subclass, please visit
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/Options.py#L1616
    # if the line number has changed, ctrl+f for "class PerGameCommonOptions"
