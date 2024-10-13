import multiprocessing as mul
import os
import os.path as pt
import spacy
import json
from typing import Iterable
import paths
from paragraph import Paragraph
from tokenized_paragraph import TokenizedParagraph
from tokenizer import Tokenizer

nlp = spacy.load('ru_core_news_sm')

F_CHUNK_SIZE = 32

def get_chunks(plist: list[str], ch_size: int) -> list[list[str]]:
    chunk = []
    chunks = []
    for i, fpath in enumerate(plist):
        chunk.append(fpath)

        if (i > 0 and i % ch_size == 0) or i == len(plist) - 1:
            chunks.append(chunk)
            chunk = []

    return chunks

def paragraph_from_file(fpath: str) -> Paragraph:
    p = Paragraph(fpath)
    p.load()
    return p

def tokenize_paragraph(p: Paragraph) -> TokenizedParagraph:
    tokenizer = Tokenizer(nlp)
    tokenized_p = tokenizer.tokenize(p)
    return tokenized_p

def preprocess_chunk(plist_ch: list[str]) -> list[TokenizedParagraph]:
    tokenized_ps = []
    for fpath in plist_ch:
        p = paragraph_from_file(fpath)
        tok_p = tokenize_paragraph(p)

        tokenized_ps.append(tok_p)

    return tokenized_ps

def preprocess(plist: list[str]) -> Iterable[TokenizedParagraph]:
    p_chunks = get_chunks(plist, F_CHUNK_SIZE)

    with mul.Pool(processes=mul.cpu_count()) as pool:
        tp_chunks = pool.map(preprocess_chunk, p_chunks)

    for tp_chunk in tp_chunks:
        for tp in tp_chunk:
            yield tp

def serialize_tp(tp: TokenizedParagraph) -> dict:
    ser_tp = {
        'title': tp.title, 
        'tokens': [t for t in tp.tokens]
    }
    return ser_tp

def preprocess_files_and_save(path: str, fn_out: str):
    flist = os.listdir(path)
    plist = list(map(lambda fn: pt.join(path, fn), flist))

    tps = [serialize_tp(tp) for tp in preprocess(plist)]

    with open(fn_out, mode='w', encoding='utf-8') as out_f:
        json.dump(obj=tps, fp=out_f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    print('Preprocessing files for clustering...')
    preprocess_files_and_save(paths.CLU_PATH, 'tokenized-clu.json')

    print('Preprocessing files for classification...')
    preprocess_files_and_save(paths.CLASSF_PATH, 'tokenized-classf.json')

    print('Done!')