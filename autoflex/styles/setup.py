import shutil
import pathlib


def copy_autoflex_styles_to_static(app, exception):
    # Define source directory where your styles are located
    source_dir = pathlib.Path(__file__).parent / "css"

    # Define destination directory in the build output's _static folder
    build_static_dir = pathlib.Path(app.outdir) / '_static' / "css"

    # Ensure the destination directory exists
    build_static_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files from the source to the destination
    for item in source_dir.iterdir():
        if item.is_file():
            shutil.copy(item, build_static_dir / item.name)
        elif item.is_dir():
            # Copy directories recursively
            shutil.copytree(item, build_static_dir / item.name, dirs_exist_ok=True)
