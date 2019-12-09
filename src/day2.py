
class Intcode:
    EXIT_CODE=99
    ADD_CODE = 1
    MULTI_CODE = 2

    def __init__(self, program):
        self.memory = program
        self.pointer = 0

    def start_code(self, noun, verb):
        # noun = int(code[0:2])
        # verb = int(code[2:4])
        self.memory[1] = noun
        self.memory[2] = verb

    def start(self):
        self.step();

    def execute(self, instruction):
        opcode = instruction[0]

        if opcode == self.EXIT_CODE:
            return False

        left = self.memory[instruction[1]]
        right = self.memory[instruction[2]]

        if opcode == self.ADD_CODE:
            value = left + right
        elif opcode == self.MULTI_CODE:
            value = left * right
        else:
            raise Exception("Invalid opcode", opcode)

        self.memory[instruction[3]] = value
        return True

    def step(self):
        start = self.pointer
        end = self.pointer+4
        instruction = self.memory[start:end]
        out = self.execute(instruction)
        if out == False:
            return
        self.pointer = end
        self.step()

def runCode(noun, verb, program):
    intcode = Intcode(program)

    print(f"Code {100 * noun + verb}")

    intcode.start_code(noun, verb)
    intcode.start()

    print(f"Value is {intcode.memory[0]}")

def runIt(target, program):
    for noun in range(100):
        for verb in range(100):
            intcode = Intcode(program[:])

            print(f"Code {noun} + {verb}")

            intcode.start_code(noun, verb)

            try:
                intcode.start()
            except Exception as inst:
                message, code = inst.args
                print(f"{message}: {code}")

            if intcode.memory[0] == target:
                return noun, verb

    raise Exception("Target not found", target)


if __name__ == "__main__":
    data = open("./data/day2.txt")
    lines = data.readlines()
    program = [int(i) for line in lines for i in line.rstrip().split(',')]

    # runCode(12,2,program)

    try:
        target = 19690720
        noun, verb = runIt(target, program)
        print(f"Code {100 * noun + verb}")

    except Exception as inst:
            message, code = inst.args
            print(f"{message}: {code}")
