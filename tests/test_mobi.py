import os
import shutil
from os.path import abspath, dirname, exists, join, splitext

import mobi
from mobi.extract import ExtractionType

TEST_DIR = dirname(abspath(__file__))


def test_extract():
    for fname in os.listdir(TEST_DIR):
        ext = splitext(fname)[-1].upper()
        if ext in [".MOBI", ".PRC", ".AZW", ".AZW3", ".AZW4"]:
            tempdir, filepath = mobi.extract(join(TEST_DIR, fname))
            assert exists(tempdir)
            assert exists(filepath)
            shutil.rmtree(tempdir)

def test_extract_file_like():
    with open(join(TEST_DIR, "demo.mobi"), "rb") as infile:
        tempdir, filepath = mobi.extract(infile)
        assert exists(tempdir)
        assert exists(filepath)
        shutil.rmtree(tempdir)

def test_extract_specific_output():

    extractiontypetofileextention = [
        [ExtractionType.EPUB, ".epub"],
        [ExtractionType.HTML, ".html"],
    ]

    with open(join(TEST_DIR, "demo.mobi"), "rb") as infile:
        for ext in extractiontypetofileextention:
            tempdir, filepath = mobi.extract(infile, extractable=ext[0])
            assert exists(tempdir)
            assert exists(filepath)
            assert (ext[1] in filepath)
            shutil.rmtree(tempdir)
