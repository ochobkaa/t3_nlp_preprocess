import re
from spacy.tokens import Doc, Token
from typing import Callable
from paragraph import Paragraph
from tokenized_paragraph import TokenizedParagraph

class Tokenizer:
    def __init__(self, pipeline: Callable[[str], Doc]) -> None:
        self.__pipeline = pipeline

    def tokenize(self, p: Paragraph) -> TokenizedParagraph:
        # Description's raw text processing pipeline

        def remove_punctuation(s: str) -> str:
            new_s = re.sub(r'[^\w\s]', ' ', s)
            return new_s
        
        def remove_digits(s: str) -> str:
            new_s = re.sub(r'\d', '', s)
            return new_s

        def remove_multispaces(s: str) -> str:
            new_s = re.sub(r'\s+', ' ', s).strip()
            return new_s
    
        def lower(s: str) -> str:
            new_s = s.lower()
            return new_s
        
        t_proc_chain = [
            remove_punctuation, 
            remove_digits, 
            remove_multispaces, 
            lower
        ]

        # Description's tokenized Doc container processing

        def del_stop_words(d: Doc) -> list[Token]:
            new_l = [token for token in d if not token.is_stop]
            return new_l
        
        def lemm(d: list[Token]) -> list[str]:
            new_l = [token.lemma_ for token in d]
            return new_l

        # Run all procesing

        title = p.title
        desc = p.desc

        desc_p = desc
        for fproc in t_proc_chain:
            desc_p = fproc(desc_p)

        desc_doc = self.__pipeline(desc_p)

        fil_tok = del_stop_words(desc_doc)
        tokens = lemm(fil_tok)

        tp = TokenizedParagraph(title, tokens)
        return tp