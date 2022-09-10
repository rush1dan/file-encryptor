

def get_file_name(filepath: str, with_extension: bool = True):
    filename_rev = ""
    for i in range(len(filepath) - 1, -1, -1):
        ch = filepath[i]
        if ch == "/" or ch == "\\":
            break
        filename_rev += ch

        filename = filename_rev[::-1]
    return filename if with_extension else filename.replace(get_file_extension(filename), "")


def get_file_extension(filename: str):
    extension_rev = ""
    for i in range(len(filename) - 1, -1, -1):
        ch = filename[i]
        extension_rev += ch
        if ch == ".":
            break
    return extension_rev[::-1]


def get_original_file_extension(encrypted_filepath: str) -> str:
    with open(encrypted_filepath, "rb") as file:
        file_content = file.read()
        extension_rev = b""
        for i in range(len(file_content) - 1, -1, -1):
            ch = file_content[i]
            extension_rev += ch
            if ch == b".":
                break
        return extension_rev[::-1].decode()


def remove_file_extension(text: str | bytes) -> str | bytes:
    for i in range(len(text) - 1, -1, -1):
        ch = text[i]
        if ch == (b"." if type(text) == bytes else "."):
            return text[:i]
