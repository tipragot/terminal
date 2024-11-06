#!/usr/bin/env python3

import logging
from os import environ
from subprocess import getoutput, check_output
from pygls.server import LanguageServer
from pygls.workspace import TextDocument
from tempfile import NamedTemporaryFile
from lsprotocol import types
from pygls.uris import to_fs_path
from norminette_fmt import generate_header

user_login = environ.get("LOGIN", "tcezard")
norminette_version = check_output(["norminette", "--version"]).decode("utf-8").split(" ")[-1]
server = LanguageServer("norminette-server", norminette_version)

def analyze(path: str) -> list[types.Diagnostic]:
    diagnostics: list[types.Diagnostic] = []
    output = getoutput(f"norminette {path}", encoding="utf-8")
    for line in output.split("\n")[1:]:
        if not line.startswith("Error: "): continue
        error_type = line.split(" ")[1]
        line_index = int(line.split("line:")[1].split(",")[0].strip()) - 1
        message = line.split("):")[1].strip()
        diagnostics.append(
            types.Diagnostic(
                code=error_type,
                message=message,
                range=types.Range(
                    start=types.Position(line=line_index, character=0),
                    end=types.Position(line=line_index, character=0),
                )
            )
        )
    return diagnostics

def update_header_filename(server: LanguageServer, document: TextDocument):
    header = generate_header(document.filename, document.source, update_time=False)
    if not document.source.startswith(header):
        text_edit = types.TextEdit(
            range=types.Range(
                start=types.Position(line=0, character=0),
                end=types.Position(
                    line=0 if not document.source.startswith("/* ") else 10,
                    character=0 if not document.source.startswith("/* ") else 800,
                ),
            ),
            new_text=header + ("\n\n" if not document.source.startswith("/* ") else ""),
        )
        server.apply_edit(types.WorkspaceEdit(changes={document.uri: [text_edit]}))

@server.thread()
@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(server: LanguageServer, params: types.DidOpenTextDocumentParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    update_header_filename(server, document)

    try: diagnostics = analyze(to_fs_path(params.text_document.uri))
    except Exception as error:
        logging.error(error)
        return
    server.publish_diagnostics(params.text_document.uri, diagnostics)

@server.thread()
@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(server: LanguageServer, params: types.DidChangeTextDocumentParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    try:
        with NamedTemporaryFile(prefix="norminette_", suffix=".c") as file:
            file.write(document.source.encode("utf-8"))
            file.flush()
            diagnostics = analyze(file.name)
    except Exception as error:
        logging.error(error)
        return
    server.publish_diagnostics(params.text_document.uri, diagnostics, params.text_document.version)

logging.basicConfig(level=logging.INFO, format="%(message)s")
server.start_io()