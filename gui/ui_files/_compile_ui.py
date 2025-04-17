import subprocess
from pathlib import Path


def main():
    """
    Compile all .ui files in the current directory into Python files using pyuic6.

    This function scans the directory containing the script for Qt Designer `.ui` files,
    then uses `pyuic6` to compile each one into a `.py` file. If a `.ui` file's name does
    not already start with `ui_`, the prefix is added to the output filename.

    For example:
        - 'main_window.ui' becomes 'ui_main_window.py'
        - 'ui_settings.ui' remains 'ui_settings.py'

    The output `.py` files are written to the same directory as the input `.ui` files.
    Compilation errors are caught and logged to the console.
    """
    current_dir = Path(__file__).parent
    ui_files = list(current_dir.glob("*.ui"))

    for ui_file in ui_files:
        filename_stem = ui_file.stem

        # ensure a 'ui_' prefix if added
        if filename_stem.startswith("ui_"):
            output_name = f"{filename_stem}.py"
        else:
            output_name = f"ui_{filename_stem}.py"

        output_py = current_dir / output_name
        command = ['pyuic6', '-x', str(ui_file), '-o', str(output_py)]

        try:
            subprocess.run(command, check=True)
            print(f"Success: {output_py.name}")

        except subprocess.CalledProcessError as e:
            print(f"Failed to compile {ui_file.name}: {e}")


if __name__ == "__main__":
    main()
