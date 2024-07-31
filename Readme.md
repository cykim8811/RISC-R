# RISC-R: Reduced Instruction Set Computer - Reversible

RISC-R is an innovative computer architecture designed to implement reversible computing principles. It is inspired by the RISC-V architecture but adapted to ensure all operations are reversible.

## Repository Contents

This repository contains the following files:

1. `assembler.py`: The RISC-R assembler that converts RISC-R assembly code into machine code.
2. `sim.py`: A simulator for the RISC-R architecture, allowing you to run and test RISC-R programs.
3. `test.asm`: A sample RISC-R assembly program for testing and demonstration purposes.

## RISC-R Architecture

RISC-R (Reduced Instruction Set Computer - Reversible) is designed with the following key features:

- All instructions are reversible, allowing for bidirectional execution of programs.
- Uses a jump offset mechanism for reversible control flow.
- Implements memory-register swaps (MSWP) for reversible data movement.
- Utilizes XOR for reversible data manipulation.

## Instruction Set

| Opcode | Syntax              | Description                                                               |
| ------ | ------------------- | ------------------------------------------------------------------------- |
| 0x00   | `nop`               | No operation                                                              |
| 0x01   | `add rd, rs`        | Add: rd = rd + rs                                                         |
| 0x02   | `sub rd, rs`        | Subtract: rd = rd - rs                                                    |
| 0x03   | `xor rd, rs`        | Bitwise XOR: rd = rd ^ rs                                                 |
| 0x04   | `rol rd, rs`        | Rotate left: rd = rd rotated left by value in rs                          |
| 0x05   | `ror rd, rs`        | Rotate right: rd = rd rotated right by value in rs                        |
| 0x08   | `swp rd, rs`        | Swap contents of rd and rs                                                |
| 0x0F   | `hlt`               | Halt the program                                                          |
| 0x21   | `addi rd, imm`      | Add immediate: rd = rd + imm                                              |
| 0x22   | `subi rd, imm`      | Subtract immediate: rd = rd - imm                                         |
| 0x23   | `xori rd, imm`      | Bitwise XOR with immediate: rd = rd ^ imm                                 |
| 0x24   | `roli rd, imm`      | Rotate left by immediate: rd = rd rotated left by imm                     |
| 0x25   | `rori rd, imm`      | Rotate right by immediate: rd = rd rotated right by imm                   |
| 0x29   | `mswp rd, imm(rs)`  | Memory-register swap: Swap contents of rd with memory at address rs + imm |
| 0x30   | `jeq rs, rt, delta` | Jump if equal: if (rs == rt) step += delta                                |
| 0x31   | `jne rs, rt, delta` | Jump if not equal: if (rs != rt) step += delta                            |
| 0x32   | `jlt rs, rt, delta` | Jump if less than: if (rs < rt) step += delta                             |
| 0x33   | `jgt rs, rt, delta` | Jump if greater than: if (rs > rt) step += delta                          |
| 0x34   | `jle rs, rt, delta` | Jump if less than or equal: if (rs <= rt) step += delta                   |
| 0x35   | `jge rs, rt, delta` | Jump if greater than or equal: if (rs >= rt) step += delta                |
| 0x36   | `jmp delta`         | Unconditional jump: step += delta                                         |

Note: rd, rs, and rt represent registers. imm represents an immediate value. step is the value added to pc after each instruction. delta represents the change in step for jump instructions.

## RISC-R Jump Mechanism

RISC-R implements a unique, reversible jump mechanism:

1. Instead of directly modifying the program counter (pc), jump instructions modify a step value.
2. After every instruction, pc is updated as: pc = pc + step
3. The default step value is typically the size of one instruction (e.g., 2 for 16-bit instructions).
4. Jump instructions add a delta value to step, effectively changing the next instruction to be executed.
5. This mechanism allows for reversible execution, as the jump can be undone by subtracting the same delta value from step.

6. To ensure reversibility, jump instructions are typically used in pairs:
   - At the jump source: `JMP +n` (or conditional jump) increases step by n.
   - At the jump destination: `JMP -n` decreases step by n, restoring the original flow.
7. This pairing mechanism allows for perfect reversibility of program flow:
   - Forward execution: JMP +n → [jumped code] → JMP -n
   - Reverse execution: JMP +n ← [jumped code] ← JMP -n

This approach ensures that all operations, including control flow changes, are reversible, maintaining the fundamental principle of reversible computing in RISC-R.


## Binary Instruction Format
RISC-R uses a variable-length instruction format:

### 2-byte Instruction Format:
```
|0 1 2 3 4 5|6|7| 8  9 10 11 |12 13 14 15|
|  opcode   |f|u|     rd     |    rs     |
```
- Bits 0-5: opcode
- Bit 5: extension flag (1 if instruction is extended to 4 bytes)
- Bit 6: previous instruction extension flag (used for reverse execution)
- Bit 7: unused
- Bits 8-11: rd (destination register)
- Bits 12-15: rs (source register)

### 4-byte Instruction Format:
For instructions that require more information (e.g., immediate values or jump offsets), an additional 2 bytes are appended to the basic 2-byte format.

Example: `addi rd, imm`
```
|0 1 2 3 4 5|6|7| 8  9 10 11 |12 13 14 15| 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 |
|  opcode   |1|u|     rd     |   0000    |                    imm                          |
```


## Getting Started

To use this RISC-R implementation:

1. Write your RISC-R assembly code in a `.asm` file.
2. Use `assembler.py` to convert your assembly code into machine code.
3. Run the resulting machine code through `sim.py` to execute your program.

Example usage:

```
python assembler.py test.asm -o test.bin
python sim.py test.bin
```

## Contributing

We welcome contributions to improve the RISC-R architecture, assembler, or simulator. Please feel free to submit issues or pull requests.

## License

[Specify your chosen license here]

## Contact

cykim8811@snu.ac.kr





