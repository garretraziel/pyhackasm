import re

A_REGEX = re.compile(r"@((?P<symbol>[a-zA-Z_.$:][a-zA-Z0-9_.$:]*)|(?P<number>\d+))")
C_REGEX = re.compile(r"((?P<dest>A?M?D?)=)?(?P<comp>([DAM])?([-!+&|])?([DAM10]))(;("
                     r"?P<jump>JGT|JEQ|JGE|JLT|JNE|JLE|JMP))?")
L_REGEX = re.compile(r"\((?P<symbol>[a-zA-Z_.$:][a-zA-Z0-9_.$:]*)\)")


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, assembly):
        self.assembly = assembly.splitlines()
        self.current_line = -1
        self.symbol = None
        self.number = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.command_type = None

    def has_more_commands(self):
        next_line = self.current_line + 1
        while next_line < len(self.assembly):
            if self.assembly[next_line].strip() and not self.assembly[next_line].strip().startswith("//"):
                return True
            next_line += 1
        return False

    def advance(self):
        self.current_line += 1
        current_line = self.assembly[self.current_line].strip()
        while not current_line or current_line.startswith("//"):
            self.current_line += 1
            current_line = self.assembly[self.current_line].strip()

        m = A_REGEX.match(current_line)
        if m is not None:
            self.symbol = m.group("symbol")
            self.number = m.group("number")
            self.command_type = "A_COMMAND"
            return

        m = C_REGEX.match(current_line)
        if m is not None:
            self.dest = m.group("dest")
            self.comp = m.group("comp")
            self.jump = m.group("jump")
            self.command_type = "C_COMMAND"
            return

        m = L_REGEX.match(current_line)
        if m is not None:
            self.symbol = m.group("symbol")
            self.command_type = "L_COMMAND"
            return

        raise ParserError("Encountered non-assembly command:", current_line)
