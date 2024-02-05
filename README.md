PDF Cover Plugin for Calibre
============================

PDFs do not support meta-tag cover files like HTML-based ebook formats such as ePub. Ebook library and reading software usually displays the first page of the PDF as the cover, but for many PDFs, such as those of out-of-print, public domain books - have unclear, unhelpful, unattractive, or even blank first pages.

This plugin takes the cover set in the Calibre metadata and inserts it as a new first page of the book's PDF. If you change the cover later, subsequent operations will replace the first page instead of prepending indefinitely.

Errors will be raised if either the PDF format or the cover image are absent.

ROADMAP, LIMITATIONS, & CONTRIBUTNG
---------------------
- Errors will display serially. If many operations fail in a row, you will have a heck of a time clearing each error dialog.
- On some PDFs, the inserted cover image sits smaller on the page in some ereaders than I would expect, but I don't know understand the PDF format enough to guess what the cause of this is, and it seems relatively uncommon.
- There are no options, though perhaps some users would like to configure, say, the DPI, or whether the cover fits to height or width.

I made this plugin primarily for myself, and in its current state it suits my needs. Feel free to leave a GitHub issue if you encounter bugs or desire new features, but tasks of real complexity will probably require contributions from someone else.


LICENSE INFORMATION
-------------------

This software is distributed uner the WTFPL. See LICENSE.TXT for details.

The source of [pypdf](https://github.com/py-pdf/pypdf) is bundled. See PYPDF_LICENSE.TXT for license information for that project.
