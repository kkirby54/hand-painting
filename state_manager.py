import json
from pathlib import Path
from datetime import datetime

class StateManager:
    """Manages the persistence of the job state."""
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error decoding state file. Starting fresh.")
        return {"last_processed_index": -1, "last_run_date": None}

    def save(self, index: int, date_str: str):
        state = {
            "last_processed_index": index,
            "last_run_date": date_str
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def can_run_today(self) -> bool:
        """Checks if the job has already run today."""
        state = self._load()
        last_run_date = state.get("last_run_date")
        today_str = datetime.now().strftime("%Y-%m-%d")
        return last_run_date != today_str

    def get_next_index(self, total_items: int) -> int:
        """Calculates the next index to process, handling looping."""
        state = self._load()
        last_index = state.get("last_processed_index", -1)
        next_index = last_index + 1
        
        if next_index >= total_items:
            print("Reached end of list. Looping back to start.")
            return 0
        return next_index
