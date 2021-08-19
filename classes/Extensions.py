from collections import defaultdict
from json import load, dump


class Extensions:
    def __init__(self, json_file_path, directory_for_extensions=None, extensions=None):
        """
        Loads the extensions file.
        If "directory_for_extensions" and "extensions" were specified, we save them to the json file.
        """

        self._extensions_file_path = json_file_path
        self.extensions = {}
        self.__get_existing_extensions()

        if directory_for_extensions and extensions:
            extensions = set(extensions)

            self.add_extensions(directory_for_extensions, extensions)
            self.write_json_file()

    def __get_existing_extensions(self):
        """Load extensions from json file to the extensions_file dictionary"""
        try:
            with open(self._extensions_file_path, 'r') as extensions:
                x = load(extensions)
                self.extensions = {directory: set(extension) for directory, extension in x.items()}
        except FileNotFoundError:
            pass

    def add_extensions(self, directory: str, extensions: set):
        """Adds the extensions to the json object"""
        self.extensions = defaultdict(set, self.extensions)
        self.extensions[directory] = self.extensions[directory] | extensions

    def remove_extensions(self, directory: str, extensions: set):
        extensions = set(extensions)
        self.extensions[directory] = self.extensions[directory] - extensions

    def remove_directory(self, directory: str):
        if self.extensions.get(directory):
            del self.extensions[directory]

    def write_json_file(self):
        """Writes the json object to the json __file_path"""

        # turns all the extension sets into lists since json doesn't work with sets
        extensions_list = {directory: list(extensions) for directory, extensions in self.extensions.items()}

        with open(self._extensions_file_path, 'w') as extensions:
            dump(extensions_list, extensions)
