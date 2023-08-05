from pathlib import Path
from reportpl.types import ValidationError
from typing import TYPE_CHECKING
from reportpl.widgets.pics_subfolder_widget import PicFolder

if TYPE_CHECKING:
    from reportpl.base_web_form import BaseWebForm


class PicsFolderConverter:
    def __init__(self, storage: str | Path) -> None:
        self.storage = Path(storage)

    def __call__(self, form: 'BaseWebForm', value: str) -> list[PicFolder]:
        value = value.strip()
        path = self.storage / value
        if not path.is_dir():
            raise ValidationError(f"pasta não encontrada")
        data: list[PicFolder] = []
        if value:
            for entry in path.iterdir():
                if entry.is_dir():
                    item: PicFolder = {"folder": entry.name, "files": []}
                    for entry2 in entry.iterdir():
                        if entry2.is_file():
                            item['files'].append(str(entry2.absolute()))
                    data.append(item)
        return data
