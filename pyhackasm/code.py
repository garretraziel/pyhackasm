from .parser import ParserError

COMP_TABLE = {
    '0': ("0", "101010"),
    '1': ("0", "111111"),
    '-1': ("0", "111010"),
    'D': ("0", "001100"),
    'A': ("0", "110000"),
    'M': ("1", "110000"),
    '!D': ("0", "001101"),
    '!A': ("0", "110001"),
    '!M': ("1", "110001"),
    '-D': ("0", "001111"),
    '-A': ("0", "110011"),
    '-M': ("1", "110011"),
    'D+1': ("0", "011111"),
    'A+1': ("0", "110111"),
    'M+1': ("1", "110111"),
    'D-1': ("0", "001110"),
    'A-1': ("0", "110010"),
    'M-1': ("1", "110010"),
    'D+A': ("0", "000010"),
    'D+M': ("1", "000010"),
    'D-A': ("0", "010011"),
    'D-M': ("1", "010011"),
    'A-D': ("0", "000111"),
    'M-D': ("1", "000111"),
    'D&A': ("0", "000000"),
    'D&M': ("1", "000000"),
    'D|A': ("0", "010101"),
    'D|M': ("1", "010101")
}

DEST_TABLE = {
    'M': "001",
    'D': "010",
    'MD': "011",
    'A': "100",
    'AM': "101",
    'AD': "110",
    'AMD': "111"
}

JUMP_TABLE = {
    'JGT': "001",
    'JEQ': "010",
    'JGE': "011",
    'JLT': "100",
    'JNE': "101",
    'JLE': "110",
    'JMP': "111"
}


def dest(mnemonic):
    if mnemonic is None:
        return "000"
    if mnemonic not in DEST_TABLE:
        raise ParserError("Unknown dest:", mnemonic)
    return DEST_TABLE[mnemonic]


def comp(mnemonic):
    if mnemonic not in COMP_TABLE:
        raise ParserError("Unknown comp:", mnemonic)
    return COMP_TABLE[mnemonic]


def jump(mnemonic):
    if mnemonic is None:
        return "000"
    if mnemonic not in JUMP_TABLE:
        raise ParserError("Unknown jump:", mnemonic)
    return JUMP_TABLE[mnemonic]
