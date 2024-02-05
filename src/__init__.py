from calibre.customize import InterfaceActionBase

class PDFCoverActionBase(InterfaceActionBase):
    '''
    This class is a simple wrapper that provides information about the actual
    plugin class. The actual interface plugin class is called PDFCoverPlugin
    and is defined in the ui.py file, as specified in the actual_plugin field
    below.

    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    '''
    name                = 'PDF Cover'
    description         = 'A Plugin that Prepends a Cover Image to the beginning of a PDF'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'C Warren Dale'
    file_types          = set(['pdf'])
    version             = (0, 1, 0)
    minimum_calibre_version = (0, 7, 53)

    #: This field defines the GUI plugin class that contains all the code
    #: that actually does something. Its format is module_path:class_name
    #: The specified class must be defined in the specified module.
    actual_plugin       = 'calibre_plugins.pdf_cover.action:PDFCoverAction'

    def is_customizable(self):
        '''
        This method must return True to enable customization via
        Preferences->Plugins
        '''
        return False
