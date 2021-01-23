import os


# create database file
def createdb(dirpath : str, name : str):
    """
    Create db in dirpath with name {name}
    """
    if os.path.exists(dirpath):
        pass
    else:
        return 1
    with open(f"{dirpath}{name}.vm", "w") as db:
        db.write("# syntax - value:key\n# true automatically convert to True in python\n# false automatically convert to False in python")
        db.close()


def readdb(path : str) -> (int, dict):
    """
    read db and return as dict {"key":"value"...}
    """
    dict = {}
    if os.path.exists(path):
        pass
    else:
        raise FileNotFoundError(2, f"file {path} not found!")
    with open(path, "r") as db:
        content_lines = db.readlines()
        for line in content_lines:
            if line == "\n" or line[0] == "#":
                continue
            try:
                value = line.split(":")[1].replace("\n", "")
                if value == "true":
                    value = "True"
                elif value == "false":
                    value = "False"
                
                dict[line.split(":")[0]] = value
            except IndexError:
                print(f"Error on line {content_lines.index(line)} with content '{line}'")
    return dict

#write to db
def writedb(path, key, value) -> int:
    """
    write to db on path {path} name {key} with value {value}
    """
    if key == "" or value == "":
        return 1
    if os.path.exists(path):
        pass 
    else:
        return 1
    with open(path, "a") as db:
        db.write(f"\n{key}:{value}")
    return 0

if __name__ == "__main__":
    print(readdb("./tests/db.vm"))
    writedb("./tests/db.vm", "acpi", "false")
    print(readdb("./tests/db.vm"))
    createdb("./tests/", "test")