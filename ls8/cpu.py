"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general-purpose registers
        self.reg = [0] * 8

        self.pc = 0

        self.address = 0

        self.running = True

        self.sp = 7
        # self.reg[7] = 0xF0

    def load(self):
        """Load a program into memory."""

        # if len(sys.argv) < 2:
        #     print("try another file")
        #     sys.exit()

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    value = int(n, 2)
                    self.ram[address] = value
                    address += 1
        except:
            print("can not find it!")
            sys.exit()

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, MAR):
        # accept the address to read and return the value stored there
        # Memory Address Register (MAR): contains the address that is being read or written to
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # accept a value to write, and the address to write it to
        # Memory Data Register (MDR): contains the data that was read or the data to write
        self.ram[MAR] = MDR
        # return MDR


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def ldi(self, operand_a, operand_b):
        # Set the value of a register to an integer.
        self.reg[operand_a] = operand_b
        
    def prn(self, operand_a):
        # Print numeric value stored in the given register
        print(self.reg[operand_a])

    def mul(self, operand_a, operand_b):
        product = self.reg[operand_a] * self.reg[operand_b]
        self.reg[operand_a] = product

    def push(self, operand_a):
        self.sp -= 1
        self.ram[self.sp] = self.reg[operand_a]

    def pop(self, operand_a):
        self.reg[operand_a] = self.ram[self.sp]
        self.sp += 1

    def run(self):
        """Run the CPU."""
       
        # Halt the CPU (and exit the emulator)
        HLT = 0b00000001

        LDI = 0b10000010 
        PRN = 0b01000111 
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True

        while running:
            IR = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False
                # total number of bytes in any instruction is the number of operands + 1
                self.pc += 1 

            elif IR == LDI:
                self.ldi(operand_a, operand_b)
                self.pc += 3

            elif IR == PRN:
                self.prn(operand_a)
                self.pc += 2

            elif IR == MUL:
                self.mul(operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                self.push(operand_a)
                self.pc += 2

            elif IR == POP:
                self.pop(operand_a)
                self.pc += 2

            else:
                running = False