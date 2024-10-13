import unicodedata

TITLE_LABEL = 'Title:'
DESC_LABEL = 'Description:'

class Paragraph:
    def __init__(self, path: str):
        self.__path = path
        self.__title = ''
        self.__desc = ''

    @property
    def path(self) -> str:
        return self.__path
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def desc(self) -> str:
        return self.__desc
    
    def __get_title_and_desc(self, s: str) -> tuple[str, str]:
        raw_title, raw_desc = s.split('\n')[:2]

        title = raw_title.replace(TITLE_LABEL, '').strip()
        desc = raw_desc.replace(DESC_LABEL, '').strip()

        return title, desc
    
    def load(self):
        path = self.__path
        with open(path, encoding='utf-8') as f:
            fcont = f.read()
            fcont_norm = unicodedata.normalize('NFC', fcont)

            title, desc = self.__get_title_and_desc(fcont_norm)

        self.__title = title
        self.__desc = desc