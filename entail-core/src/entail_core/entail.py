import asyncio
from entail_core.cli import cli
from entail_core.file_manager import FileManager
from entail_core.project_manager import ProjectManager


async def main():
    result = cli()

    file_manager = FileManager()
    project_manager = ProjectManager(file_manager)

    # TODO: Call validation with a file or a set of files depending on
    #  whether `result.file` is a file or a directory.

    await project_manager.validate(result.file)


asyncio.run(main())
