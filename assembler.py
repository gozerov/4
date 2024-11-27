import json
import sys


COMMANDS = {
    "LOAD_CONST": 13,
    "LOAD_MEM": 41,
    "STORE_MEM": 50,
    "GREATER_EQ": 24,
}


def assemble(input_path, output_path, log_path):
    instructions = []
    log = []

    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            command = parts[0]
            operand = int(parts[1])

            if command not in COMMANDS:
                raise ValueError(f"Unknown command: {command}")

            opcode = COMMANDS[command]
            instructions.append((opcode, operand))
            log.append({"command": command, "opcode": opcode, "operand": operand})

    with open(output_path, "wb") as f:
        for opcode, operand in instructions:
            f.write(opcode.to_bytes(1, "little"))
            f.write(operand.to_bytes(4, "little"))

    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
