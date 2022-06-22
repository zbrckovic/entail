from entail_file_manager import ProcessingListener as \
    ProcessingListenerABC
from mappings import error_to_diagnostic


class ProcessingListener(ProcessingListenerABC):
    def __init__(self, language_server):
        self._server = language_server
        self._accumulated_diagnostics = []

    def on_parsed(self, file_manager, errors=None):
        if errors is None:
            errors = []

        uri = file_manager.uri
        self._report_errors(uri, errors)

    def on_processed_ast(self, file_manager, errors=None):
        if errors is None:
            errors = []

        uri = file_manager.uri
        self._report_errors(uri, errors)

    def on_validated(self, file_manager, errors=None):
        if errors is None:
            errors = []

        uri = file_manager.uri
        self._report_errors(uri, errors)

    def on_validated_imports(self, file_manager, errors=None):
        if errors is None:
            errors = []

        uri = file_manager.uri
        self._report_errors(uri, errors)

    def _report_errors(self, uri, errors):
        self._accumulated_diagnostics.extend(
            error_to_diagnostic(error, uri) for error in errors)
        self._server.publish_diagnostics(uri, self._accumulated_diagnostics)
