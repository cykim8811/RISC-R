
instructions = {
    0x00: "NOP",
    0x01: "ADD",
    0x02: "SUB",
    0x03: "XOR",
    0x04: "ROL",
    0x05: "ROR",
    0x08: "SWP",
    0x0F: "HLT",
    0x21: "ADDI",
    0x22: "SUBI",
    0x23: "XORI",
    0x24: "ROLI",
    0x25: "RORI",
    0x29: "MSWP",
    0x30: "JEQ",
    0x31: "JNE",
    0x32: "JLT",
    0x33: "JGT",
    0x34: "JLE",
    0x35: "JGE",
    0x36: "JMP",
}

class RISCRSimulator:
    def __init__(self, program: bytearray, debug=False):
        self.memory = bytearray(2**20)  # 1MB
        self.reg = [bytearray(4) for _ in range(16)]
        self.pc = 0     # program counter
        self.ofs = 2    # jump offset
        self.debug = debug

        self.memory[:len(program)] = program

    def step(self):
        inst    = int.from_bytes(self.memory[self.pc:self.pc+2], 'little')
        
        opcode  = inst & 0x3F
        ext     = (inst >> 5) & 1
        r_ext   = (inst >> 6) & 1
        reg1    = (inst >> 8) & 0xF
        reg2    = (inst >> 12) & 0xF
        
        if ext:
            ext_data = int.from_bytes(self.memory[self.pc+2:self.pc+4], 'little', signed=True)
            self.ofs += 2
        else:
            ext_data = 0

        if r_ext:
            self.ofs -= 2


        if self.debug:
            print(f"[{self.pc:04X}] {instructions[opcode]:4} {reg1:1X} {reg2:1X} {(ext_data):04X}", end="    ")
            print(f"stack({int.from_bytes(self.reg[6], 'little'):04X}):", ", ".join([f"{int.from_bytes(self.memory[0xFC-i*4:0xFC-i*4+4], 'big'):08X}" for i in range(4)]))


        if opcode == 0x00:      # nop
            pass

        elif opcode == 0x01:    # add
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            res = (v1 + v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x21:    # addi
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = ext_data
            res = (v1 + v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x02:    # sub
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            res = (v1 - v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x22:    # subi
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = ext_data
            res = (v1 - v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x03:    # xor
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            res = (v1 ^ v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x23:    # xori
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = ext_data
            res = (v1 ^ v2) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x04:    # rol
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little') % 32
            res = ((v1 << v2) | (v1 >> (32 - v2))) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x24:    # roli
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = ext_data % 32
            res = ((v1 << v2) | (v1 >> (32 - v2))) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x05:    # ror
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little') % 32
            res = ((v1 >> v2) | (v1 << (32 - v2))) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x25:    # rori
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = ext_data % 32
            res = ((v1 >> v2) | (v1 << (32 - v2))) & 0xFFFFFFFF
            self.reg[reg1] = bytearray(res.to_bytes(4, 'little'))

        elif opcode == 0x08:    # swp
            rs1, rs2 = self.reg[reg1], self.reg[reg2]
            self.reg[reg1], self.reg[reg2] = rs2, rs1

        elif opcode == 0x29:    # mswp
            rs1 = self.reg[reg1]
            rs2 = int.from_bytes(self.reg[reg2], 'little')
            rsp = rs2 + ext_data
            rs2 = self.memory[rsp:rsp+4]
            v1 = int.from_bytes(rs1)
            v2 = int.from_bytes(rs2)
            self.reg[reg1] = bytearray(v2.to_bytes(4, 'little'))
            memoryview(self.memory)[rsp:rsp+4] = bytearray(v1.to_bytes(4, 'little'))

        elif opcode == 0x30:    # jeq
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 == v2:
                self.ofs += ext_data

        elif opcode == 0x31:    # jne
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 != v2:
                self.ofs += ext_data

        elif opcode == 0x32:    # jlt
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 < v2:
                self.ofs += ext_data

        elif opcode == 0x33:    # jgt
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 > v2:
                self.ofs += ext_data

        elif opcode == 0x34:    # jle
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 <= v2:
                self.ofs += ext_data

        elif opcode == 0x35:    # jge
            v1 = int.from_bytes(self.reg[reg1], 'little')
            v2 = int.from_bytes(self.reg[reg2], 'little')
            if v1 >= v2:
                self.ofs += ext_data
        
        elif opcode == 0x36:    # jmp
            self.ofs += ext_data
        
        elif opcode == 0x0F:    # hlt
            return False

        
        self.pc += self.ofs

        return True

    
    def run(self):
        while self.step(): pass
    


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RISCR Simulator")
    parser.add_argument("program", type=str, help="Program file")
    args = parser.parse_args()

    with open(args.program, "r") as f:
        program = bytearray([int(x, 16) for x in f.read().replace("\n", " ").replace("  ", " ").split()])

    p = RISCRSimulator(program, debug=True)

    p.run()
