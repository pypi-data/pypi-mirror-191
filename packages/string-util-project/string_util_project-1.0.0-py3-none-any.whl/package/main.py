def convert_to_bold(input_str):
    """
        Converts given input string into bold string
    Args:
        input_str (str): input string
    Returns:
        str: bold converted string of input string.
    """
    UNICODE_BOLD_CODE_OF_A = 0x1D400
    UNICODE_BOLD_CODE_OF_a = 0x1D41A
    UNICODE_BOLD_CODE_OF_0 = 0x1D7CE

    bold_str = ""
    for char in input_str:
        if char >= "a" and char <= "z":
            bold_char = chr(ord(char) - ord("a") + UNICODE_BOLD_CODE_OF_a)
        elif char >= "A" and char <= "Z":
            bold_char = chr(ord(char) - ord("A") + UNICODE_BOLD_CODE_OF_A)
        elif char >= "0" and char <= "9":
            bold_char = chr(ord(char) - ord("0") + UNICODE_BOLD_CODE_OF_0)
        else:
            bold_char = char
        bold_str += bold_char
    return bold_str
