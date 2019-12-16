import sys

class Attribute:
    def __init__(self, location, value):
        self.location = location
        self.value = value

class Intcode:
    EXIT_CODE       = '99'
    ADD_CODE        = '01'
    MULTI_CODE      = '02'
    INPUT_CODE      = '03'
    OUTPUT_CODE     = '04'
    JUMP_TRUE_CODE  = '05'
    JUMP_FALSE_CODE = '06'
    LESS_THAN_CODE  = '07'
    EQUALS_CODE     = '08'

    POINTER_STEPS = {
        ADD_CODE:   4,
        MULTI_CODE: 4,
        INPUT_CODE: 2,
        OUTPUT_CODE:  2,
        EXIT_CODE:  1,
        JUMP_TRUE_CODE: 3,
        JUMP_FALSE_CODE: 3,
        LESS_THAN_CODE: 4,
        EQUALS_CODE: 4
    }

    def __init__(self, program, inputs=[]):
        self.memory = program
        self.pointer = 0
        self.inputs = inputs

    def start_code(self, code):
        code = code.rjust(4, '0')

        noun = int(code[0:2])
        verb = int(code[2:4])

        self.memory[1] = noun
        self.memory[2] = verb

    @property
    def result(self):
        return self.memory[0]

    def start(self):
        self.step()

        return self.result

    def read_opcode(self, code):
        self.a = self.b = self.c = self.d = self.e = '0'

        try:
            code = str(code)
            self.d, self.e = code[-2:]
            self.c   = code[-3]
            self.b   = code[-4]
            self.a   = code[-5]

        except Exception as inst:
            print(inst.args)

        self.opcode = self.d + self.e

        return self.a, self.b, self.c, self.d, self.e

    def parameter(self, value, mode='0'):
        if mode == '0':
            return self.memory[value]
        else:
            return value

    def store_value(self, value, location):
        self.memory[location] = value

    def log(self, value):
        print(value)

    @property
    def param_1(self):
        location = self.memory[self.pointer + 1]
        value = self.parameter(location, self.c)
        return Attribute(location, value)

    @property
    def param_2(self):
        location = self.memory[self.pointer + 2]
        value = self.parameter(location, self.b)
        return Attribute(location, value)

    @property
    def param_3(self):
        location = self.memory[self.pointer + 3]
        value = self.parameter(location, self.a)
        return Attribute(location, value)

    def execute(self):
        if self.opcode == self.EXIT_CODE:
            return False

        move_pointer_to = self.pointer + self.POINTER_STEPS[self.opcode]

        if self.opcode == self.ADD_CODE:
            value = self.param_1.value + self.param_2.value
            self.store_value(value, self.param_3.location)
        elif self.opcode == self.MULTI_CODE:
            value = self.param_1.value * self.param_2.value
            self.store_value(value, self.param_3.location)
        elif self.opcode == self.INPUT_CODE:
            self.store_value(int(self.inputs.pop()), self.param_1.location)
        elif self.opcode == self.OUTPUT_CODE:
            self.log(self.param_1.value)
        elif self.opcode == self.JUMP_TRUE_CODE:
            if self.param_1.value != 0:
                move_pointer_to = self.param_2.value
        elif self.opcode == self.JUMP_FALSE_CODE:
            if self.param_1.value == 0:
                move_pointer_to = self.param_2.value
        elif self.opcode == self.LESS_THAN_CODE:
            if self.param_1.value < self.param_2.value:
                self.store_value(1, self.param_3.location)
            else:
                self.store_value(0, self.param_3.location)
        elif self.opcode == self.EQUALS_CODE:
            if self.param_1.value == self.param_2.value:
                self.store_value(1, self.param_3.location)
            else:
                self.store_value(0, self.param_3.location)
        else:
            raise Exception("Invalid opcode", self.opcode)

        return move_pointer_to

    def step(self):
        instruction_code = str(self.memory[self.pointer]).rjust(5,"0")
        self.read_opcode(instruction_code)

        move_to = self.execute()

        if move_to == False:
            return

        self.pointer = move_to
        self.step()

def runCode(program, inputs=[]):
    intcode = Intcode(program, inputs)

    print(f"Code {inputs}")

    result = intcode.start()

    # print(f"Value is {result}")

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
    data = open("./data/day5.txt")
    lines = data.readlines()
    program = [int(i) for line in lines for i in line.rstrip().split(',')]

    runCode(program, sys.argv[1:])

    # try:
    #     target = 19690720
    #     noun, verb = runIt(target, program)
    #     print(f"Code {100 * noun + verb}")

    # except Exception as inst:
    #         message, code = inst.args
    #         print(f"{message}: {code}")
