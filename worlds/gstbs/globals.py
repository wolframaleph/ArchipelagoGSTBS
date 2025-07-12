from pathlib import Path

GSTBS_ROOT_DIR: Path = Path(__file__).parent
GAME_NAME: str = "Golden Sun The Broken Seal"
GSTBS_DEBUG: bool = False

try:
    from .debug import env
    GSTBS_DEBUG = env.GSTBS_DEBUG
except (ImportError, ModuleNotFoundError):
    pass  # fail gracefully
