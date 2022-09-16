# Vector Align

This is a production-ready tool for align parallel documents to sentences without the need for a machine translation system or lexicon.
[Vecalign](https://github.com/thompsonb/vecalign) - an accurate sentence alignment algorithm is used, which is fast even for very long documents.

Instead of [LASER](https://github.com/facebookresearch/LASER), we use [LaBSE](https://arxiv.org/abs/2007.01852) from [sentence-transformers](https://github.com/UKPLab/sentence-transformers) pre-trained models for its better performance in parallel text mining task.

To support the specific African languages in WMT22, we fork from [laserembeddings](https://github.com/yannvgn/laserembeddings) and integrate sentence pieces tokenizer in [this repository](https://github.com/volctrans/laserembeddings).

# Installation (Recommend)
```Bash
pip3 setup.py install 
```


# Example
1. two separate docs
```bash
vector-align \
    --left-doc tests/zh.file \
    --right-doc tests/en.file \
    --output output.txt
```

2. 1 bilingual doc
```bash
vector-align \
    --left-doc tests/bilingual.file \
    --right-doc tests/bilingual.file \
    --output output.txt
```

# Reference
Please cite the [paper](https://www.aclweb.org/anthology/D19-1136.pdf) if you use this tool:

```
@inproceedings{thompson-koehn-2019-vecalign,
    title = "{V}ecalign: Improved Sentence Alignment in Linear Time and Space",
    author = "Thompson, Brian and Koehn, Philipp",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1136",
    doi = "10.18653/v1/D19-1136",
    pages = "1342--1348",
}
```
