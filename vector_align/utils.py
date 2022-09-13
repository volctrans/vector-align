# -*- coding: utf-8 -*-
# create@ 2022-04-08 19:44

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from typing import Tuple

import pycld2 as cld2
from polyglot.text import Text

line_break_regex = re.compile(r'(\\n)+\*?')


def group_sentences(content: str, language: str = None, do_split: bool = True) -> Tuple:
    """
    split content into sentences filtered with language, if provided
    :param content:
    :param language:
    :param do_split:
    :return:
    """
    content = normalize(content)

    if language is None:
        reliable, _, top_3_choices = cld2.detect(content, bestEffort=False)
        language = top_3_choices[0][1]

    if do_split:

        collection = []
        lines = content.split('\n')
        for line in lines:
            t = Text(line, language)
            for sent in t.sentences:
                raw = sent.raw
                reliable, _, top_3_choices = cld2.detect(raw, bestEffort=False)
                if top_3_choices:
                    top_lang, top_lang_percent = top_3_choices[0][1], top_3_choices[0][2]
                    if top_lang_percent > 80:
                        if top_lang == language:
                            collection.append(raw)
                else:
                    collection.append(raw)
    else:
        collection = content.split('\n')
    return collection, language


def group_sentences_in_pair(content: str, src_lang: str = None, trg_lang: str = None,
                            do_split: bool = False) -> Tuple:
    """
    split content into sentences filtered with language, if provided
    :param content:
    :param src_lang:
    :param trg_lang:
    :param do_split:
    :return:
    """
    content = normalize(content)
    reliable, _, top_3_choices = cld2.detect(content, bestEffort=False)
    src_collection = []
    trg_collection = []
    if len(top_3_choices) >= 2:
        top_1_lang, top_2_lang = min(top_3_choices[0][1], top_3_choices[1][1]), \
                                 max(top_3_choices[0][1], top_3_choices[1][1])

        if src_lang and trg_lang:
            assert (top_1_lang, top_2_lang) == (min(src_lang, trg_lang), max(src_lang, trg_lang))

        else:
            src_lang, trg_lang = top_1_lang, top_2_lang
        lines = content.split('\n')
        for line in lines:
            if do_split:
                t = Text(line)
                sentences = [sent.raw for sent in t.sentences]
            else:
                sentences = [line]
            for raw in sentences:
                reliable, _, top_3_choices = cld2.detect(raw, bestEffort=False)
                if top_3_choices:
                    top_lang, top_lang_percent = top_3_choices[0][1], top_3_choices[0][2]
                    if top_lang_percent > 80:
                        if top_lang == src_lang:
                            src_collection.append(raw)
                        else:
                            trg_collection.append(raw)
    return src_collection, trg_collection, src_lang, trg_lang


def normalize(text):
    # remove multiple line break character
    doc = line_break_regex.sub('\n', text)
    lines = []
    for line in doc.split('\n'):
        line = line.strip().lstrip('*').lstrip('-')
        if len(line) > 1:
            lines.append(line)
    doc = "\n".join(lines)
    return doc
