from pathlib import Path
import re


def main():
    root_dir = Path(r"./")

    py_files = list(root_dir.glob("*.py"))
    # ref: https://stackoverflow.com/questions/
    # 17140886/how-to-search-and-replace-text-in-a-file
    
    for pyf in py_files:
        # loop through and read in the file
        with open(pyf, "r") as f:
            lines = f.read()
        
        # replace all occurrance
        if pyf.stem != "find_replace_pysoil":
            lines = lines.replace("pysoil", "pyvstress")
        
        # write the replaced data to the same file
        with open(pyf, "w") as f:
            f.write(lines)

if __name__ == "__main__":
    main()
