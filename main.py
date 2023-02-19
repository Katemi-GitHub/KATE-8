import time

class Clock:
    def __init__(self, hz):
        self.interval = 1 / hz
        self.last_time = time.perf_counter()
        
    def delay(self):
        current_time = time.perf_counter()
        elapsed_time = current_time - self.last_time
        if elapsed_time < self.interval:
            time.sleep(self.interval - elapsed_time)
        self.last_time = current_time

class RAM():
    def __init__(self, size):
        self.size = size
        self.memory = ['00000000' for _ in range(self.size)]
    
    def read(self, address):
        if address <= self.size:
            return self.memory[address]
    
class ROM():
    def __init__(self):
        self.memory = []
        with open("rom.katerom", "r") as file:
            self.memory = [line.strip() for line in file.readlines()]
    
    def read(self, address):
        if address <= self.size:
            return self.memory[address]

    def write(self, address, value):
        if address <= self.size:
            self.memory[address] = value

class CPU():
    def __init__(self, input):
        self.ram = RAM(256)
        self.rom = ROM()
        self.running = True
        self.pc = "00000000"
        self.acc = "00000000"
        self.rb = "00000000"
        self.rc = "00000000"
        self.sp = "00000000"
        self.jmp = "00000000" # JMP Last address
        self.input = input # Input
        self.output = "00000000" # Output
    
    def run(self):
        address = 0
        while self.running:
            sli = self.rom.memory[(address*2)+1] # Reads SLI as a whole 8 bit number
            instruction = self.rom.memory[address*2][4:]
            data = self.rom.memory[address*2][:4]
            if instruction == "0000": # NOP
                pass

            elif instruction == "0001": # STI
                self.acc = self.ram[data]

            elif instruction == "0010": # STA
                self.acc = self.rom[data]

            elif instruction == "0011": # ADD
                self.acc = '{0:08b}'.format(int(int("0b" + str(self.acc)), 2) + 1)

            elif instruction == "0100": # SUB
                self.acc = '{0:08b}'.format(int(int("0b" + str(self.acc)), 2) - 1)

            elif instruction == "0101": # LOAD A
                self.acc = sli
            
            elif instruction == "0110": # LOAD B
                self.rb = sli
            
            elif instruction == "0111": # ADD A B
                temp = int("0b" + str(self.acc), 2) + int("0b" + str(self.rb), 2)
                self.rc = '{0:08b}'.format(temp & 0xFF)
            
            elif instruction == "1000": # SUB A B
                result = int(int("0b" + str(self.acc)), 2) - int(int("0b" + str(self.rb)), 2)
                if result < 0:
                    result += 256
                self.acc = '{0:08b}'.format(result)
            
            elif instruction == "1001": # Input to A
                self.acc = self.input
            
            elif instruction == "1010": # A to Output
                self.output = self.acc
            
            elif instruction == "1011": #MOV B A
                self.rb = self.acc
            
            elif instruction == "1100": #JMP Inmediate
                address = int(int("0b" + str(data)), 2)

            elif instruction == "1101": #JMP
                self.jmp = '{0:08b}'.format(address + 1)
                address = int(int("0b" + str(data)), 2)
            
            elif instruction == "1110": #JMP Return
                address = int(int("0b" + str(self.jmp)), 2)

            elif instruction == "1111": # STOP
                self.running = False

            # Increment or decrement the address based on the instruction
            if instruction in ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000"]:
                if address < len(self.rom.memory)/2 - 1:
                    address += 1
                else:
                    address = 0
            elif instruction == "1111":
                address = 0

class FrameBuffer():
    def __init__(self):
        self.xsize = 16
        self.ysize = 16
        self.memory = []
        for x in range(self.xsize):
            for y in range(self.ysize):
                self.memory.append('{0:04b}'.format(x) + '{0:04b}'.format(y) + "00000000")
    
    def readx(self, address):
        return self.memory[address][0:3]
    def ready(self, address):
        return self.memory[address][4:7]
    def readc(self, address):
        return self.memory[address][8:15]