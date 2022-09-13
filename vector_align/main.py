# -*- coding: utf-8 -*-
# create@ 2022-04-08 19:18

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs
import json
from pathlib import Path

from vector_align.extractor import extract_parallel_pairs
from vector_align.utils import group_sentences, group_sentences_in_pair


def main():
    parser = argparse.ArgumentParser("Vector Align Tool")

    parser.add_argument("--left-doc",
                        type=str,
                        required=True)

    parser.add_argument("--right-doc",
                        type=str,
                        required=True)

    parser.add_argument("--left-lang",
                        type=str,
                        required=False)

    parser.add_argument("--right-lang",
                        type=str,
                        required=False)

    parser.add_argument("--method",
                        type=str,
                        required=False,
                        choices=['labse', 'laser'],
                        default="labse")

    parser.add_argument("--output",
                        type=str,
                        required=False)

    args = parser.parse_args()

    left_doc = Path(args.left_doc)
    right_doc = Path(args.right_doc)

    assert left_doc.is_file() and right_doc.is_file(), "Provided left doc/right doc is invalid."

    if args.left_doc == args.right_doc:
        with codecs.open(args.left_doc, errors='ignore') as f:
            content = f.read()
            left_sentences, right_sentences, left_lang, right_lang = \
                group_sentences_in_pair(content,
                                        args.left_lang,
                                        args.right_lang)
    else:
        with codecs.open(args.left_doc, errors='ignore') as lf, \
                codecs.open(args.right_doc, errors='ignore') as rf:
            left_content, right_content = lf.read(), rf.read()
            left_sentences, left_lang = group_sentences(left_content, args.left_lang)
            right_sentences, right_lang = group_sentences(right_content, args.right_lang)
    extracted_pairs = extract_parallel_pairs(left_sentences, right_sentences)

    with open(args.output or 'output.txt', 'w') as f:
        for sentence_pair in extracted_pairs:
            line = {
                'src_text': sentence_pair[0],
                'trg_text': sentence_pair[1],
                'src_lang': left_lang,
                'trg_lang': right_lang,
                'score': round(1 - sentence_pair[2], 2)
            }
            f.write(json.dumps(line, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
