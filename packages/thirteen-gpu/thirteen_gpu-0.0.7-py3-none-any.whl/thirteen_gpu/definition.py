from enum import Enum, auto
import os


# workspace directory 지정
WORKSPACE_DIR = f"{os.environ['HOME']}/workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

class JobStatus(Enum):
    """Job status enum."""
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    STOPPED = auto()
    CRASHED = auto()
    UNKNOWN = auto()
    
class ProjectStatus(Enum):
    LIVE = auto()
    DEAD = auto()