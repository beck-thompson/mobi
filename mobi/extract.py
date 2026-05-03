import shutil
import tempfile
from os.path import basename, exists, join, splitext
from enum import IntFlag, auto

from loguru import logger

from mobi.kindleunpack import unpackBook

class ExtractionType(IntFlag):
    """The type of file format we will try to extract to. If ALL is chosen, the order will be: EPUB first, HTML second, PDF last."""
    EPUB = auto()
    HTML = auto()
    PDF = auto()
    ALL = EPUB | HTML | PDF

def extract(infile, extractable=ExtractionType.ALL):
    """Extract mobi file and return path to ePub, HTML, or PDF file"""

    tempdir = tempfile.mkdtemp(prefix="mobiex")
    if hasattr(infile, "fileno"):
        tempname = next(tempfile._get_candidate_names()) + ".mobi"
        pos = infile.tell()
        infile.seek(0)
        with open(join(tempdir, tempname), "wb") as outfile:
            shutil.copyfileobj(infile, outfile)
        infile.seek(pos)
        infile = join(tempdir, tempname)

    logger.debug("file: %s" % infile)
    fname_in = basename(infile)
    base, ext = splitext(fname_in)
    fname_out_epub = base + ".epub"
    fname_out_html = "book.html"
    fname_out_pdf = base + ".001.pdf"
    unpackBook(infile, tempdir, epubver="A")
    epub_filepath = join(tempdir, "mobi8", fname_out_epub)
    html_filepath = join(tempdir, "mobi7", fname_out_html)
    pdf_filepath = join(tempdir, fname_out_pdf)
    if exists(epub_filepath) and ExtractionType.EPUB in extractable:
        return tempdir, epub_filepath
    elif exists(html_filepath) and ExtractionType.HTML in extractable:
        return tempdir, html_filepath
    elif exists(pdf_filepath) and ExtractionType.PDF in extractable:
        return tempdir, pdf_filepath
    raise ValueError("Coud not extract from %s" % infile)


if __name__ == "__main__":
    print(extract("../tests/demo.mobi"))
