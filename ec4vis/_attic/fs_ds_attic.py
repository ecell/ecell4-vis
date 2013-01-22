def is_hdf5_file(filepath):
    """Returns True if filepath points hdf5 (at least be opend as h5py.File).
    """
    try:
        File(self.file_path, 'r')
        return True
    except IOError:
        pass
    return False


class Hdf5LogicalFileBundle(object):
    """Logical hdf5 bundle.
    """
    def __init__(self, path):
        """Initializer.
        """
        self._data = None
        if not os.path.exists(path):
            return ValueError('Path does not exist.')
        if os.path.isfile(path):
            # will raise IOError if file is invalid.
            self._data = File(path, 'r')
        elif os.path.isdir(path):
            self._data = []
            for fn in glob.glob(os.path.join(path, '*.*')):
                try:
                    head, tail = os.path.split(fn)
                    body, ext = os.path.splitext(tail)
                    d = File(fn, 'r')
                    self._data.append((body, d))
                except:
                    pass
        else: # invalid path
            return ValueError('Not a file or directory.')
        self.path = path

    @property
    def data(self):
        """Returns data as a single block.
        """
        if isinstance(self._data, list):
            return None
        else:
            return self._data
        
    @property
    def data_sequence(self):
        """Returns data as a sequence of blocks.
        """
        if isinstance(self._data, list):
            return self._data
        else:
            return self._data.items()


    def set_file_path(self, path):
        """Setter for _file_path.
        """
        self._file_path = path
        self._data_bundle = None

    # property bindings
    file_path = property(get_file_path, set_file_path)
    
    def is_valid(self):
        """Returns if datasource is valid.
        """
        if self._data_bundle is None:
            if self._file_path is None:
                return False
            try:
                self._data_bundle = Hdf5LogicalFileBundle(self._file_path)
                return True
            except (ValueError, IOError):
                pass
        return False

    def can_provide_sequence(self):
        """Always true if is_valid().
        """
        return self.is_valid()

    def get_data_identifier(self):
        """Returns file path as the identity.
        """
        if self.file_path is None:
            return '[None]'
        return self.file_path

    def get_data(self):
        """Returns data as a single block.
        """
        if self.is_valid():
            return self._data_bundle.data

    def get_data_sequence(self):
        """Returns data as a sequence of blocks.
        """
        if self.is_valid():
            return self._data_bundle.data_sequence
