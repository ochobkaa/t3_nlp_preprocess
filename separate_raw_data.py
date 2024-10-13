import os
import os.path as pt
import random as rnd
from hashlib import md5

import paths

def separate_paragraphs(fcont: str) -> list[str]:
    paragraphs = fcont.split('\n\n')
    return paragraphs

def train_test_splitter(pars: list[str], ratio = 0.8) -> tuple[list[str], list[str]]:
    train = []
    test = []
    for par in pars:
        rnd_val = rnd.uniform(0, 1)
        if rnd_val > ratio:
            test.append(par)

        else:
            train.append(par)

    return train, test

def paragraph_fn(paragraph: str) -> str:
    pbytes = paragraph.encode()
    phash = md5(pbytes)
    hasht = phash.hexdigest()
    
    fn = f'{hasht}.txt'
    return fn

def save_paragraphs(path: str, paragraphs: list[str]):
    for p in paragraphs:
        fn = paragraph_fn(p)
        fpath = pt.join(path, fn)

        while pt.exists(fpath):
            fn = paragraph_fn(fn)
            fpath = pt.join(path, fn)
        
        with open(fpath, mode='w', encoding='utf8') as f:
            f.write(p)

def separate_raw_data():
    fn_list = os.listdir(paths.RAW_DATA_PATH)
    for fn in fn_list:
        fpath = pt.join(paths.RAW_DATA_PATH, fn)
        with open(fpath, encoding='utf8') as f:
            fcont = f.read()

            paragraphs = separate_paragraphs(fcont)
            ptrain, ptest = train_test_splitter(paragraphs)

        save_paragraphs(paths.CLU_PATH, ptrain)
        save_paragraphs(paths.CLASSF_PATH, ptest)

if __name__ == '__main__':
    separate_raw_data()