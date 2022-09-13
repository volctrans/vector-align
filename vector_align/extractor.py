from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import zipfile
from math import ceil
from pathlib import Path
from typing import List

import numpy as np
import requests
from sentence_transformers import SentenceTransformer

from . import logger
from .dp_utils import yield_overlaps, make_alignment_types, make_doc_embedding, vecalign

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

home = os.path.expanduser('~')

DATA_DIR = os.path.join(home, f'.cache/transformers/')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)
MODEL_DIR = os.path.join(DATA_DIR, 'LaBSE')
MODEL_FILE = os.path.join(DATA_DIR, 'LaBSE.zip')

if not Path(MODEL_DIR).exists():
    model_url = 'http://tosv.byted.org/obj/lab-mt-data/sentence-transformers/LaBSE.zip'
    try:
        logger.info('= Begin download sentence-transformers model. =')
        response = requests.get(model_url, stream=True)
        total_length = int(response.headers.get('content-length'))
        with open(MODEL_FILE, "wb") as f:
            dl = 0
            for chunk in response.iter_content(chunk_size=20480):
                if chunk:
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(50 * dl / total_length)
                    logger.info(f"Download:[{'=' * done}{' ' * (50 - done)}]")
        with zipfile.ZipFile(MODEL_FILE, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        Path(MODEL_FILE).unlink()
    except Exception as ex:
        logger.exception(ex)

LaBSE_model = SentenceTransformer(model_name_or_path=MODEL_DIR)


def overlap(sentences_group: List[str], num_overlaps: int) -> List[str]:
    output = set()
    for out_line in yield_overlaps(sentences_group, num_overlaps):
        output.add(out_line)

    # for reproducibility
    output = list(output)
    output.sort()
    return output


def embedding(sentences_group: List[str]):
    return LaBSE_model.encode(sentences_group)


def clean(sentences_group: List[str]) -> List[str]:
    return [re.sub(re.compile(r"[\s]+"), " ", text).strip() for text in sentences_group]


def read_in_embeddings(sentences_group_overlap: List[str], embed: np.ndarray):
    """
    Given a text file with candidate sentences and a corresponing embedding file,
       make a maping from candidate sentence to embedding index, 
       and a numpy array of the embeddings
    """
    sent2line = dict()
    for ii, line in enumerate(sentences_group_overlap):
        if line.strip() in sent2line:
            raise Exception('got multiple embeddings for the same line')
        sent2line[line.strip()] = ii

    return sent2line, embed


def extract_parallel_pairs(src_sentences_group: List[str],
                           trg_sentences_group: List[str],
                           alignment_max_size: int = 4,
                           del_percentile_frac: float = 0.2,
                           max_size_full_dp: int = 300,
                           costs_sample_size: int = 20000,
                           num_samps_for_norm: int = 100,
                           search_buffer_size: int = 5) -> List:
    alignment_max_size = max(alignment_max_size, 2)

    src_sentences_group = clean(src_sentences_group)
    trg_sentences_group = clean(trg_sentences_group)

    src_sentences_group_overlap = overlap(src_sentences_group, num_overlaps=alignment_max_size)
    trg_sentences_group_overlap = overlap(trg_sentences_group, num_overlaps=alignment_max_size)

    src_sentences_group_emb = embedding(src_sentences_group_overlap)
    trg_sentences_group_emb = embedding(trg_sentences_group_overlap)

    src_sent2line, src_line_embeddings = read_in_embeddings(src_sentences_group_overlap,
                                                            src_sentences_group_emb)
    tgt_sent2line, tgt_line_embeddings = read_in_embeddings(trg_sentences_group_overlap,
                                                            trg_sentences_group_emb)

    width_over2 = ceil(alignment_max_size / 2.0) + search_buffer_size

    src_lines = src_sentences_group
    vecs0 = make_doc_embedding(src_sent2line, src_line_embeddings, src_lines, alignment_max_size)

    tgt_lines = trg_sentences_group
    vecs1 = make_doc_embedding(tgt_sent2line, tgt_line_embeddings, tgt_lines, alignment_max_size)

    final_alignment_types = make_alignment_types(alignment_max_size)

    stack = vecalign(vecs0=vecs0,
                     vecs1=vecs1,
                     final_alignment_types=final_alignment_types,
                     del_percentile_frac=del_percentile_frac,
                     width_over2=width_over2,
                     max_size_full_dp=max_size_full_dp,
                     costs_sample_size=costs_sample_size,
                     num_samps_for_norm=num_samps_for_norm)

    res = []
    for (x, y), s in zip(stack[0]['final_alignments'], stack[0]['alignment_scores']):
        if len(x) == 0 or len(y) == 0 or s >= 0.5:
            continue
        src = ''
        for i in x:
            src += src_sentences_group[i]
        tgt = ''
        for i in y:
            tgt += trg_sentences_group[i]
        res.append((src, tgt, s))
    return res
