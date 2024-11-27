import json
import sys


class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.accumulator = 0

    def execute(self, instructions):
        for opcode, operand in instructions:
            if opcode == 13:  # LOAD_CONST
                self.accumulator = operand
            elif opcode == 41:  # LOAD_MEM
                self.accumulator = self.memory[self.accumulator + operand]
            elif opcode == 50:  # STORE_MEM
                self.memory[operand] = self.accumulator
            elif opcode == 24:  # GREATER_EQ
                comparison_result = int(self.memory[operand] >= self.accumulator)
                self.accumulator = comparison_result

            else:
                raise ValueError(f"Unknown opcode: {opcode}")


def load_binary(file_path):
    instructions = []
    with open(file_path, "rb") as f:
        while True:
            opcode = f.read(1)
            if not opcode:
                break
            operand = f.read(4)
            instructions.append((int.from_bytes(opcode, "little"), int.from_bytes(operand, "little")))
    return instructions


def save_result(file_path, memory, start, end):
    result = {str(i): memory[i] for i in range(start, end + 1)}
    with open(file_path, "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py <binary_file> <result_file> <start> <end>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    vm = VirtualMachine()
    instructions = load_binary(binary_file)
    vm.execute(instructions)
    save_result(result_file, vm.memory, start, end)
