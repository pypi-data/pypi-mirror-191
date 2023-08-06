from pathlib import Path
from typing import Union, List

import docx


class DocxConvertor:

    @staticmethod
    def convert(path: Union[str, Path]) -> List[str]:
        file = docx.Document(path)
        units = [paragraph.text for paragraph in file.paragraphs]
        return units
