from entail_file_manager import EntailFileManager
from text.text_document import TextDocument


class ProjectManager:
    def __init__(self, theorems_manager, uri):
        self.theorems_manager = theorems_manager

        self._uri = uri
        """Uri of the root folder."""

        self._file_managers = {}

    def init_file_manager(self, uri, text):
        txt_doc = TextDocument(text)

        # TODO: think about giving self as the first argument. Then self can
        #  try to handle this before delegating this task to theorems_manager.
        file_manager = EntailFileManager(self.theorems_manager, uri, txt_doc)
        self._file_managers[uri] = file_manager
        return file_manager

    def get_file_manager(self, uri):
        return self._file_managers[uri]

    def remove_file_manager(self, uri):
        return self._file_managers.pop(uri)
