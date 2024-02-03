from pypdf import PdfWriter, PdfReader, PageRange
from PIL import Image
from pathlib import Path
import sys


watermark = "/HasPDFCustomCover"


def prependCover(bookLocation, coverLocation):
    merger = PdfWriter()

    book = PdfReader(bookLocation)
    cover = coverLocation
    coverPdf = cover + ".pdf"

    # Load cover
    with Image.open(cover) as coverImg:
        coverImg.save(coverPdf, "pdf")

    #merge cover and pdf
    merger.append(coverPdf)

    #check for watermark
    if watermark in book.metadata:
        merger.append(book, None, PageRange("1:"))
    else:
        merger.append(book)

    #update watermark
    merger.add_metadata(
            {
                **book.metadata,
                watermark : "true"
            }
    )

    #write new pdf
    merger.write(bookLocation)
    Path(coverPdf).unlink()
    merger.close()


prependCover(sys.argv[1], sys.argv[2])
