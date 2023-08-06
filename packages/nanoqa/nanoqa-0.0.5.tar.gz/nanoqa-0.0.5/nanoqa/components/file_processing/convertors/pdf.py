import subprocess
from pathlib import Path
from typing import Union, Optional, List

from ..utils import iso639_to_nltk


class PDFConvertor:

    def __init__(self):
        verify_installation = subprocess.run(["pdftotext -v"], shell=True)
        if verify_installation.returncode == 127:
            raise Exception(
                """pdftotext is not installed. It is part of xpdf or poppler-utils software suite.
                    Installation on Linux:
                    wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.03.tar.gz &&
                    tar -xvf xpdf-tools-linux-4.03.tar.gz && sudo cp xpdf-tools-linux-4.03/bin64/pdftotext /usr/local/bin

                    Installation on MacOS:
                    brew install xpdf

                    You can find more details here: https://www.xpdfreader.com
                """
            )

    @staticmethod
    def convert(
            path: Union[str, Path], layout: bool = False, language: str = iso639_to_nltk.get("en"),
            encoding: Optional[str] = "UTF-8"
    ) -> List[str]:
        if layout:
            command = ["pdftotext", "-enc", encoding, "-layout", str(path), "-"]
        else:
            command = ["pdftotext", "-enc", encoding, str(path), "-"]
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=False)
        document = output.stdout.decode(errors="ignore")
        pages = document.split("\f")[:-1]
        return pages
