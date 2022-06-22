import logging

from pygls.lsp import HoverParams, InitializeParams
from pygls.lsp.methods import \
    TEXT_DOCUMENT_DID_OPEN, \
    TEXT_DOCUMENT_DID_CLOSE, \
    TEXT_DOCUMENT_DID_CHANGE, \
    HOVER, INITIALIZE, WORKSPACE_DID_CHANGE_WATCHED_FILES
from pygls.lsp.types import \
    DidOpenTextDocumentParams, \
    DidCloseTextDocumentParams, \
    DidChangeTextDocumentParams
from pygls.server import LanguageServer

from language_description.describe_position import describe_position
from mappings import to_change, to_position, to_hover
from processing_listener import ProcessingListener
from project_manager import ProjectManager
from theorems_manager import TheoremsManager

server = LanguageServer()

project_manager: ProjectManager

theorems_manager = TheoremsManager()


@server.feature(INITIALIZE)
async def did_init(ls, params: InitializeParams):
    global project_manager
    project_manager = ProjectManager(theorems_manager, params.root_uri)


@server.feature(WORKSPACE_DID_CHANGE_WATCHED_FILES)
async def did_change_watched_files(ls, params):
    pass


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    uri = params.text_document.uri
    text = params.text_document.text

    logging.debug(f"Opened {uri}")

    file_manager = project_manager.init_file_manager(uri, text)
    listener = ProcessingListener(ls)
    await file_manager.process(listener)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls, params: DidChangeTextDocumentParams):
    uri = params.text_document.uri

    logging.debug(f"Edited {uri}")

    changes = map(to_change, params.content_changes)
    file_manager = project_manager.get_file_manager(uri)
    file_manager.update_text(changes)
    listener = ProcessingListener(ls)
    await file_manager.process(listener)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
async def did_close(ls, params: DidCloseTextDocumentParams):
    uri = params.text_document.uri

    logging.debug(f"Closed {uri}")

    file_manager = project_manager.remove_file_manager(uri)
    file_manager.clear()


@server.feature(HOVER)
async def hover(ls, params: HoverParams):
    uri = params.text_document.uri

    logging.debug(f"Hovered in {uri}")

    position = to_position(params.position)
    file_manager = project_manager.get_file_manager(uri)

    parse_result = file_manager.parse_result

    if parse_result is None:
        return

    description = describe_position(parse_result.tree, position)
    if description is not None:
        return to_hover(description)


def start_server(host, port):
    print(f'Entail Language Server listening on {host}:{port}')
    server.start_tcp(host, port)
