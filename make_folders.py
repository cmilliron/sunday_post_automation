import shutil
from pathlib import Path
import datetime

OUTPATH = "/Users/codymilliron/repos/sunday_post_automation/Resources"
SUNDAY_PATH = '/Users/codymilliron/Documents/Reeds UMC Temp/Reeds Current Sunday'

new_folders = ['01 - Notes',
               "02 - Media",
               "03 - Slides",
               "04 - Other Files",
               "05 - Library"]


def get_sunday():
    current_date = datetime.date.today()
    while True:
        day = current_date.weekday()
        if day == 6:
            break
        current_date += datetime.timedelta(1)
    return current_date


if __name__ == "__main__":
    sunday = f"Worship - {get_sunday()}"
    current_sunday_path = Path(Path(SUNDAY_PATH) / sunday)
    current_sunday_path.mkdir()
    folder: str
    for folder in new_folders:
        Path(current_sunday_path / folder).mkdir()