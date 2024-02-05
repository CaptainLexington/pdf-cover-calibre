from calibre.gui2.actions import InterfaceAction
from pathlib import Path
import sys

class PDFCoverAction(InterfaceAction):
    
    name = 'Insert PDF Cover'

    action_spec = ('Insert PDF Cover', None,
            'Insert Calibre-Defined Cover as Page 1 of PDF', None)
    
    action_type = 'current'
    
    watermark = "/HasPDFCustomCover"

    def genesis(self):
        # This method is called once per plugin, do initial setup here

        # Set the icon for this interface action
        # The get_icons function is a builtin function defined for all your
        # plugin code. It loads icons from the plugin zip file. It returns
        # QIcon objects, if you want the actual data, use the analogous
        # get_resources builtin function.
        #
        # Note that if you are loading more than one icon, for performance, you
        # should pass a list of names to get_icons. In this case, get_icons
        # will return a dictionary mapping names to QIcons. Names that
        # are not found in the zip file will result in null QIcons.

        # The qaction is automatically created from the action_spec defined
        # above
        self.qaction.triggered.connect(self.insert_covers)

    def insert_covers(self):
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, _('No rows selected'),
                                _('You must select one or more books to perform this action.'), show=True)
        book_ids = self.gui.library_view.get_selected_ids()
        db = self.gui.current_db.new_api

        for book_id in book_ids:
            print(book_id)
            cover = db.cover(book_id, as_path=True)
            book = db.format(book_id, "pdf", as_path=True)

            self.prepend_cover(book, cover)

            db.add_format(book_id, "pdf", book, replace=True)

            Path(cover).unlink()
            Path(book).unlink()


    
    def prepend_cover(self, book_location, cover_location):
        with self.interface_action_base_plugin:
            from pypdf import PdfWriter, PdfReader, PageRange
            from PIL import Image

            merger = PdfWriter()

            book = PdfReader(book_location)
            cover = cover_location
            cover_pdf = cover + ".pdf"

            # Convert cover to PDF
            with Image.open(cover) as coverImg:
                coverImg.save(cover_pdf, "pdf")
    
            # Add cover to new PDF
            merger.append(cover_pdf)

            # Check for watermark
            if self.watermark in book.metadata:
                # Add all but first page to new PDF
                merger.append(book, None, PageRange("1:"))
            else:
                # Add all pages to new PDF
                merger.append(book)

            # Update watermark
            merger.add_metadata(
                    {
                        **book.metadata,
                        self.watermark : "true"
                    }
            )

            # Write new pdf
            merger.write(book_location)
            merger.close()
    
            #Delete PDF cover
            Path(cover_pdf).unlink()
