# ⚡ RISC-V RV32I Assembler ⚡

<div align="center">

### 🔧 A Custom Python Assembler for the RISC-V RV32I ISA  
Convert Assembly Code ➜ 32-bit Machine Code

<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/RISC--V-RV32I-red?style=for-the-badge">

</div>

---

# 🚀 What is this?

This project is a **custom-built RISC-V RV32I Assembler** written in Python.  
It reads assembly instructions from a file, validates them, resolves labels, checks for errors, and converts everything into proper **32-bit binary machine code**.

Think of it as a mini version of what real assemblers do inside actual processors.

---

# 🧠 What This Assembler Supports

## ✅ Instruction Types

| Type | Instructions |
|------|--------------|
| 🔹 R-Type | `add`, `sub`, `xor`, `or`, `and`, `sll`, `srl`, `slt`, `sltu` |
| 🔹 I-Type | `lw`, `addi`, `sltiu`, `jalr` |
| 🔹 S-Type | `sw` |
| 🔹 B-Type | `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu` |
| 🔹 U-Type | `lui`, `auipc` |
| 🔹 J-Type | `jal` |

---

# ✨ Features

✅ Converts RISC-V assembly into binary  
✅ Handles labels and branching  
✅ PC-relative jump calculations  
✅ Two’s complement immediate conversion  
✅ ABI + standard register support  
✅ Detects syntax and semantic errors  
✅ Validates immediates and memory limits  
✅ Enforces Virtual Halt instruction  
✅ Generates clean 32-bit binary output  
✅ Prints the error line number according to the input file

---

# 📂 Project Structure

```bash
📦 RISC-V-Assembler
 ┣ 📜 Assembler.py
 ┣ 📜 input.txt
 ┣ 📜 output.txt
 ┗ 📜 README.md
```

---

# ▶️ Running the Assembler

## 🔹 Command

```bash
python3 Assembler.py input.txt output.txt
```

---

# 📝 Example Input

```assembly
start:
addi sp,zero,380
addi s2,zero,21
add s1,s2,s3
beq zero,zero,0
```

---

# ⚙️ Generated Output

```text
00010111110000000000000100010011
00000001010100000000100100010011
00000001001110010000010010110011
00000000000000000000000001100011
```

---

# 🔥 How the Assembler Works

## 1️⃣ Parsing Phase
- Reads assembly code line by line
- Removes empty lines
- Identifies labels and instructions

---

## 2️⃣ Label Resolution
Labels are stored with their memory addresses:

```python
labels["loop"] = 16
```

Used later for branch/jump offset calculations.

---

## 3️⃣ Validation Phase

The assembler checks for:

❌ Invalid instructions  
❌ Invalid registers  
❌ Duplicate labels  
❌ Immediate overflow  
❌ Syntax errors  
❌ Undefined labels  
❌ Missing Virtual Halt  

---

## 4️⃣ Binary Encoding

Each instruction type has a dedicated encoder function:

| Function | Purpose |
|----------|---------|
| `R_type_to_Binary()` | R-Type Encoding |
| `Iinstruction()` | I-Type Encoding |
| `btype()` | Branch Encoding |
| `sw()` | Store Encoding |
| `J()` | Jump Encoding |

The assembler combines:
- opcode
- funct3
- funct7
- registers
- immediates

to generate final machine code.

---

# 🧮 Concepts Used

<div align="center">

| Concept | Used For |
|---------|-----------|
| ISA Design | Instruction encoding |
| Two’s Complement | Negative immediates |
| Parsing | Instruction processing |
| Bit Manipulation | Binary generation |
| PC-relative Addressing | Branch/jump calculation |
| Memory Layout | Instruction mapping |

</div>

---

# ⚠️ Assumptions Taken

- Maximum instruction memory = **64 instructions**
- Labels:
  - Must start with an alphabet
  - Must end with `:`
  - Must be unique
- Empty lines are ignored
- Branch offsets are PC-relative
- Final instruction MUST be:

```assembly
beq zero,zero,0
```

or

```assembly
beq zero,zero,0x00000000
```

---

# 🚀 Future Improvements

- 🔲 Full RISC-V Simulator
- 🔲 Hexadecimal immediate support
- 🔲 Bonus instructions:
  - `mul`
  - `halt`
  - `rvrs`
- 🔲 GUI/Web visualizer
- 🔲 Unit testing
- 🔲 Modular parser redesign

---

<div align="center">

### ⭐ If you like this project, give it a star ⭐

</div>
