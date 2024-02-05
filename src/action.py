from calibre.gui2.actions import InterfaceAction
from pathlib import Path
import sys
import math
import numbers

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

        icon = get_icons("images/icon.png", "Insert PDF Cover")

        # Assign our menu to this action and an icon
        self.qaction.setIcon(icon)

        # The qaction is automatically created from the action_spec defined
        # above
        self.qaction.triggered.connect(self.insert_covers)

    def insert_covers(self):
        from calibre.gui2 import error_dialog

        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, _('No rows selected'),
                                _('You must select one or more books to perform this action.'), show=True)
        book_ids = self.gui.library_view.get_selected_ids()
        db = self.gui.current_db.new_api

        for book_id in book_ids:
            cover = db.cover(book_id, as_path=True)
            book = db.format(book_id, "pdf", as_path=True)
            metadata = db.get_metadata(book_id)
    
            if cover == None:
                error_dialog(self.gui, 'Cannot Insert Cover', f' \"{metadata.title}\" does not have a cover', show=True)
                continue
                
            if book == None:
                error_dialog(self.gui, 'Cannot Insert Cover', f' \"{metadata.title}\" is not in the PDF format', show=True)
                continue
                

            self.prepend_cover(book, cover)

            db.add_format(book_id, "pdf", book, replace=True)

            Path(cover).unlink()
            Path(book).unlink()


    
    def prepend_cover(self, book_location, cover_location):
        with self.interface_action_base_plugin:
            from pypdf import PdfWriter, PdfReader, PageRange
            from PIL import Image

            new_pdf = PdfWriter()

            book = PdfReader(book_location)
            cover = cover_location
            cover_pdf = cover + ".pdf"
            
            reference_page = book.pages[-1]
            book_pdf_units = reference_page.user_unit / 72
            book_box = reference_page.mediabox
            book_width = book_box.width
            book_height = book_box.height

            with Image.open(cover) as cover_img:
                # Resize cover image to fix in book_box
                cover_width = cover_img.width
                cover_height = cover_img.height
                (cover_dpi_x, cover_dpi_y) = cover_img.info.get("dpi", (96, 96))

                cover_width_pdf_units = cover_width * (1/book_pdf_units / cover_dpi_x)
                cover_height_pdf_units = cover_height * (1/book_pdf_units / cover_dpi_y)

                scale = max(book_width/cover_width_pdf_units, book_height/cover_height_pdf_units)
                scaled_width_pdf_units = cover_width_pdf_units * scale
                scaled_height_pdf_units = cover_height_pdf_units * scale

                # Convert cover to PDF
                cover_img.save(cover_pdf, format="pdf")

                cover_pdf_page = PdfReader(cover_pdf).pages[0]
                cover_pdf_page.scale_to(width=scaled_width_pdf_units,height=scaled_height_pdf_units)
                
                # Add cover to new PDF
                new_pdf.add_page(cover_pdf_page)

                # Check for watermark
                if self.watermark in book.metadata:
                    # Add all but first page to new PDF
                    new_pdf.append(book, None, PageRange("1:"))
                else:
                    # Add all pages to new PDF
                    new_pdf.append(book)

                # Update watermark
                new_pdf.add_metadata(
                        {
                            **book.metadata,
                            self.watermark : "true"
                        }
                )

                # Write new pdf
                new_pdf.write(book_location)
    
                #Delete PDF cover
                Path(cover_pdf).unlink()


        new_pdf.close()
