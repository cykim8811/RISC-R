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

| Opcode | Mnemonic | Syntax              | Description                                                               |
| ------ | -------- | ------------------- | ------------------------------------------------------------------------- |
| 0x00   | NOP      | `nop`               | No operation                                                              |
| 0x01   | ADD      | `add rd, rs`        | Add: rd = rd + rs                                                         |
| 0x02   | SUB      | `sub rd, rs`        | Subtract: rd = rd - rs                                                    |
| 0x03   | XOR      | `xor rd, rs`        | Bitwise XOR: rd = rd ^ rs                                                 |
| 0x04   | ROL      | `rol rd, rs`        | Rotate left: rd = rd rotated left by value in rs                          |
| 0x05   | ROR      | `ror rd, rs`        | Rotate right: rd = rd rotated right by value in rs                        |
| 0x08   | SWP      | `swp rd, rs`        | Swap contents of rd and rs                                                |
| 0x0F   | HLT      | `hlt`               | Halt the program                                                          |
| 0x21   | ADDI     | `addi rd, imm`      | Add immediate: rd = rd + imm                                              |
| 0x22   | SUBI     | `subi rd, imm`      | Subtract immediate: rd = rd - imm                                         |
| 0x23   | XORI     | `xori rd, imm`      | Bitwise XOR with immediate: rd = rd ^ imm                                 |
| 0x24   | ROLI     | `roli rd, imm`      | Rotate left by immediate: rd = rd rotated left by imm                     |
| 0x25   | RORI     | `rori rd, imm`      | Rotate right by immediate: rd = rd rotated right by imm                   |
| 0x29   | MSWP     | `mswp rd, imm(rs)`  | Memory-register swap: Swap contents of rd with memory at address rs + imm |
| 0x30   | JEQ      | `jeq rs, rt, delta` | Jump if equal: if (rs == rt) step += delta                                |
| 0x31   | JNE      | `jne rs, rt, delta` | Jump if not equal: if (rs != rt) step += delta                            |
| 0x32   | JLT      | `jlt rs, rt, delta` | Jump if less than: if (rs < rt) step += delta                             |
| 0x33   | JGT      | `jgt rs, rt, delta` | Jump if greater than: if (rs > rt) step += delta                          |
| 0x34   | JLE      | `jle rs, rt, delta` | Jump if less than or equal: if (rs <= rt) step += delta                   |
| 0x35   | JGE      | `jge rs, rt, delta` | Jump if greater than or equal: if (rs >= rt) step += delta                |
| 0x36   | JMP      | `jmp delta`         | Unconditional jump: step += delta                                         |

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
