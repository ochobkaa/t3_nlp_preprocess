from typing import Iterable

class TokenizedParagraph:
    def __init__(self, title: str, tokens: list[str]) -> None:
        self.__title = title
        self.__tokens = tokens

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def tokens(self) -> Iterable[str]:
        for t in self.__tokens:
            yield t

    @property
    def tokens_str(self) -> str:
        return ', '.join(self.__tokens)

    def __str__(self) -> str:
        return f'Title: {self.__title} Tokens: {self.tokens_str}'

    def __repr__(self) -> str:
        return f'{self.__title} / {self.tokens_str}'