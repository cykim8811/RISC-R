
instructions = {
    "NOP": 0x00,
    "ADD": 0x01,
    "SUB": 0x02,
    "XOR": 0x03,
    "ROL": 0x04,
    "ROR": 0x05,
    "SWP": 0x08,
    "HLT": 0x0F,
    "ADDI": 0x21,
    "SUBI": 0x22,
    "XORI": 0x23,
    "ROLI": 0x24,
    "RORI": 0x25,
    "MSWP": 0x29,
    "JEQ": 0x30,
    "JNE": 0x31,
    "JLT": 0x32,
    "JGT": 0x33,
    "JLE": 0x34,
    "JGE": 0x35,
    "JMP": 0x36,
}

registers = {
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6,
    "t2": 7,
    "s0": 8,
    "s1": 9,
    "a0": 10,
    "a1": 11,
    "a2": 12,
    "a3": 13,
    "s2": 14,
    "s3": 15,
}


def parse_instruction(line):
    line = line.replace(",", " ")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.split()
    line = [x for x in line if x]
    line[0] = line[0].upper()
    line = [int(x[2:], 16) if x.startswith("0x") else x for x in line]

    if line[0] not in instructions:
        raise ValueError(f"Invalid instruction: {line[0]}")
    
    if line[0] in ["NOP", "HLT"]:
        return [instructions[line[0]], 0x00]
    elif line[0] in ["ADD", "SUB", "XOR", "ROL", "ROR", "SWP"]:
        return [instructions[line[0]], registers[line[1]] + (registers[line[2]] << 4)]
    elif line[0] in ["ADDI", "SUBI", "XORI", "ROLI", "RORI"]:
        imm = int(line[2])
        if imm > 0xFFFF: raise ValueError(f"Immediate value too large: {imm}")
        return [instructions[line[0]], registers[line[1]], imm & 0xFF, (imm >> 8) & 0xFF]
    elif line[0] == "MSWP":
        offset = int(line[2])
        if offset > 0xFFFF: raise ValueError(f"Offset value too large: {offset}")
        return [instructions[line[0]], registers[line[1]] + (registers[line[3]] << 4), offset & 0xFF, (offset >> 8) & 0xFF]
    elif line[0] in ["JEQ", "JNE", "JLT", "JGT", "JLE", "JGE"]:
        return [instructions[line[0]], registers[line[1]] + (registers[line[2]] << 4), line[3]]
    elif line[0] == "JMP":
        return [instructions[line[0]], 0x00, line[1]]
    

import argparse

parser = argparse.ArgumentParser(description="RISCR Assembler")
parser.add_argument("input", help="Input file")
parser.add_argument("-o", "--output", help="Output file", default=None)

args = parser.parse_args()


with open(args.input, "r") as f:
    source = f.read()

source = source.split("\n")
source = [x.split(";")[0].strip() for x in source]
source = [x for x in source if x]
source = [parse_instruction(x) for x in source]

labels = {}

idx = 0
for line in source:
    if len(line) > 2 and type(line[2]) == str:
        if line[2] in labels:
            labels[line[2]] = idx - labels[line[2]] - 4
        else:
            labels[line[2]] = idx
    idx += 2 + ((line[0] >> 5) & 1) * 2

for line in source:
    if len(line) > 2 and type(line[2]) == str:
        lb = line.pop()
        line.append(labels[lb]&0xFF)
        line.append((labels[lb]>>8)&0xFF)
        labels[lb] = -labels[lb]

for i in range(1, len(source)):
    if len(source[i-1]) == 4:
        source[i][0] = source[i][0] + 0x40

source = [" ".join([f"{x:02X}" for x in line]) for line in source]
source = "\n".join(source)

output_file = args.output if args.output else args.input.replace(".asm", ".b")

with open(output_file, "w") as f:
    f.write(source)

print(f"Output written to {output_file}")
