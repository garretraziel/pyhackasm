import sys
from os import path
from pyhackasm.parser import Parser, ParserError
from pyhackasm.code import comp, dest, jump
from pyhackasm.symboltable import SymbolTable


def asm_first_pass(parser, symbol_table):
    address = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type in ("A_COMMAND", "C_COMMAND"):
            address += 1
        if parser.command_type == "L_COMMAND":
            symbol_table.add_entry(parser.symbol, address)


def asm_second_pass(parser, symbol_table):
    output = ""
    parser.current_line = -1
    vars_address = 16
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type == "A_COMMAND":
            if parser.number is not None:
                output += f"0{int(parser.number):015b}\n"
            elif parser.symbol is not None:
                if not symbol_table.contains(parser.symbol):
                    symbol_table.add_entry(parser.symbol, vars_address)
                    vars_address += 1
                output += f"0{symbol_table.get_address(parser.symbol):015b}\n"
            else:
                raise ParserError("Undefined number or symbol in A-command on line:", parser.current_line)
        elif parser.command_type == "C_COMMAND":
            (a, compbin) = comp(parser.comp)
            destbin = dest(parser.dest)
            jumpbin = jump(parser.jump)
            output += f"111{a}{compbin}{destbin}{jumpbin}\n"
    return output


def main(input_filename, output_filename):
    with open(input_filename) as f:
        assembly = f.read()

    p = Parser(assembly)
    st = SymbolTable()

    asm_first_pass(p, st)
    output = asm_second_pass(p, st)

    with open(output_filename, "w") as f:
        f.write(output)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} program.asm")
        exit(1)
    main(sys.argv[1], path.splitext(sys.argv[1])[0] + '.hack')
