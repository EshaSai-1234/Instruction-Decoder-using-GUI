import tkinter as tk
from tkinter import messagebox, scrolledtext

# Register dictionary
registers = {
    0: "$zero", 1: "$at", 2: "$v0", 3: "$v1",
    4: "$a0", 5: "$a1", 6: "$a2", 7: "$a3",
    8: "$t0", 9: "$t1", 10: "$t2", 11: "$t3",
    12: "$t4", 13: "$t5", 14: "$t6", 15: "$t7",
    16: "$s0", 17: "$s1", 18: "$s2", 19: "$s3",
    20: "$s4", 21: "$s5", 22: "$s6", 23: "$s7",
    24: "$t8", 25: "$t9", 26: "$k0", 27: "$k1",
    28: "$gp", 29: "$sp", 30: "$fp", 31: "$ra"
}

funct_map = {
    32: "add", 34: "sub", 36: "and", 37: "or", 42: "slt"
}
.
opcode_map = {
    35: "lw", 43: "sw", 4: "beq", 5: "bne", 2: "j", 3: "jal"
}

# Decode MIPS instruction
def decode_instruction(bin_str):
    if len(bin_str) != 32:
        return "Error: Instruction must be 32 bits."
    opcode = int(bin_str[0:6], 2)
    if opcode == 0:  # R-type
        rs = int(bin_str[6:11], 2)
        rt = int(bin_str[11:16], 2)
        rd = int(bin_str[16:21], 2)
        funct = int(bin_str[26:32], 2)
        instr = funct_map.get(funct, "unknown")
        return f"{instr} {registers[rd]}, {registers[rs]}, {registers[rt]}"
    elif opcode in [2, 3]:  # J-type
        addr = int(bin_str[6:], 2) << 2
        instr = opcode_map[opcode]
        return f"{instr} {hex(addr)}"
    else:  # I-type
        rs = int(bin_str[6:11], 2)
        rt = int(bin_str[11:16], 2)
        imm = int(bin_str[16:], 2)
        instr = opcode_map.get(opcode, "unknown")
        if instr in ["lw", "sw"]:
            return f"{instr} {registers[rt]}, {imm}({registers[rs]})"
        elif instr in ["beq", "bne"]:
            return f"{instr} {registers[rs]}, {registers[rt]}, {imm}"
        return "Unsupported instruction."

# GUI Functionality
def decode_input():
    user_input = entry.get().strip().replace(" ", "")
    if user_input.lower() == "exit":
        root.destroy()
        return
    if user_input.startswith("0x"):
        try:
            user_input = bin(int(user_input, 16))[2:].zfill(32)
        except:
            messagebox.showerror("Invalid Input", "Hex input is invalid.")
            return
    if len(user_input) != 32:
        result = "Instruction must be 32 bits."
    else:
        result = decode_instruction(user_input)

    history.insert(tk.END, f"Input: {user_input}\nOutput: {result}\n\n")
    history.yview(tk.END)

# Main App Window
root = tk.Tk()
root.title("MIPS Instruction Decoder")
root.geometry("600x400")

# Input field
entry_label = tk.Label(root, text="Enter Binary or Hex Instruction:")
entry_label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Decode button
decode_btn = tk.Button(root, text="Decode", command=decode_input, bg="lightblue")
decode_btn.pack(pady=5)

# History/output box
history = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
history.pack(padx=10, pady=10)

# Run GUI loop
root.mainloop()
