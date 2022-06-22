import * as path from 'path';
import * as net from "net";
import { ExtensionContext, ExtensionMode, workspace, commands } from 'vscode';

import { Executable, LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    context.subscriptions.push(commands.registerCommand('entail.applyRule', (name: string) => {
        console.log('hello ' + name)
    }))

    if (context.extensionMode === ExtensionMode.Development) {
        // Development - Run the server manually
        client = connectToExistingLanguageServerTCP(8080);
    } else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        const cwd = path.join(__dirname, "..", "..");
        const pythonPath = workspace
            .getConfiguration("python")
            .get<string>("pythonPath");

        if (!pythonPath) {
            throw new Error("`python.pythonPath` is not set");
        }

        client = startLangServer(pythonPath, ["-m", "server"], cwd);
    }

    // Start the client. This will also launch the server
    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

function connectToExistingLanguageServerTCP(addr: number): LanguageClient {
    const serverOptions: ServerOptions = () => {
        return new Promise(resolve => {
            const clientSocket = new net.Socket();
            clientSocket.connect(addr, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };

    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        getClientOptions()
    );
}

function startLangServer(command: string, args: string[], cwd: string): LanguageClient {
    const serverOptions: ServerOptions = {
        args,
        command,
        options: { cwd },
    };

    return new LanguageClient(command, serverOptions, getClientOptions());
}

function getClientOptions(): LanguageClientOptions {
    return {
        documentSelector: [{ scheme: 'file', language: 'entail' }],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher("**/.clientrc"),
        },
    };
}