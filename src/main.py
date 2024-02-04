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

    # Convert cover to PDF
    with Image.open(cover) as coverImg:
        coverImg.save(coverPdf, "pdf")

    # Add cover to new PDF
    merger.append(coverPdf)

    # Check for watermark
    if watermark in book.metadata:
        # Add all but first page to new PDF
        merger.append(book, None, PageRange("1:"))
    else:
        # Add all pages to new PDF
        merger.append(book)

    # Update watermark
    merger.add_metadata(
            {
                **book.metadata,
                watermark : "true"
            }
    )

    # Write new pdf
    merger.write(bookLocation)
    merger.close()
    
    #Delete PDF cover
    Path(coverPdf).unlink()
