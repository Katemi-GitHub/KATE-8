import pygame
import time
import sys

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
        self.pc = "00000000"
        self.acc = "00000000"
        self.rb = "00000000"
        self.rc = "00000000"
        self.sp = "00000000"
        self.jmp = "00000000" # JMP Last address
        self.input = input # Input
        self.output = "00000000" # Output
        self.output_b = "00000000" # Output Buffer
        self.address = 0
    
    def run(self):
        sli = self.rom.memory[(self.address*2)+1] # Reads SLI as a whole 8 bit number
        instruction = self.rom.memory[self.address*2][:4]
        itn_name = ""
        data = self.rom.memory[self.address*2][4:]
        if instruction == "0000": # NOP
            itn_name = "NOP"
            pass

        elif instruction == "0001": # STI
            itn_name = "STI"
            self.acc = self.ram[data]

        elif instruction == "0010": # STA
            itn_name = "STA"
            self.acc = self.rom[data]

        elif instruction == "0011": # ADD
            itn_name = "ADD"
            self.acc = '{0:08b}'.format(int(str(self.acc), 2) + 1)

        elif instruction == "0100": # SUB
            itn_name = "SUB"
            self.acc = '{0:08b}'.format(int(str(self.acc), 2) - 1)

        elif instruction == "0101": # LOAD A
            itn_name = "LDA"
            self.acc = sli
        
        elif instruction == "0110": # LOAD B
            itn_name = "LDB"
            self.rb = sli
        
        elif instruction == "0111": # ADD A B
            itn_name = "AAB"
            temp =int(str(self.acc), 2) +int(str(self.rb), 2)
            self.rc = '{0:08b}'.format(temp & 0xFF)
        
        elif instruction == "1000": # SUB A B
            itn_name = "SAB"
            result = int(str(self.acc), 2) - int(str(self.rb), 2)
            if result < 0:
                result += 256
            self.acc = '{0:08b}'.format(result)
        
        elif instruction == "1001": # Input to A
            itn_name = "ITA"
            self.acc = self.input
        
        elif instruction == "1010": # A to Output
            itn_name = "ATO"
            self.output = self.acc
        
        elif instruction == "1011": #MTB
            itn_name = "MTB"
            self.output_b = sli
        
        elif instruction == "1100": #JMP Inmediate
            itn_name = "JMI"
            self.address = int(str(data), 2)

        elif instruction == "1101": #JMP
            itn_name = "JMP"
            self.jmp = '{0:08b}'.format(self.address + 1)
            self.address = int(str(data), 2)
        
        elif instruction == "1110": #JMP Return
            itn_name = "JMR"
            self.address = int(str(self.jmp), 2)

        elif instruction == "1111": # STOP
            itn_name = "STP"
            self.running = False

        if instruction == "1111":
            self.address = 0
        else:
            self.address += 1
        if self.address == len(self.rom.memory)/2:
            self.address = 0
        print(str(hex(self.address)) + " " + itn_name + " " + str(data) + " " + str(sli))

class FrameBuffer():
    def __init__(self):
        self.size = 64
        self.memory = []
        for x in range(8):
            for y in range(8):
                self.memory.append('{0:03b}'.format(x) + '{0:03b}'.format(y) + "00")
    
    def readx(self, address):
        return self.memory[address][0:3]
    
    def ready(self, address):
        return self.memory[address][3:6]
    
    def readc(self, address):
        return self.memory[address][6:8]

    def writec(self, address, value):
        self.memory[address] = self.memory[address][0:6] + value

class Display():
    def __init__(self):
        self.display = pygame.display.set_mode((480, 480))
        pygame.display.set_caption("KATE-8")
        self.framebuffer_1 = FrameBuffer()
        self.framebuffer_2 = FrameBuffer()
        self.select_buffer = self.framebuffer_1
        self.other_buffer = self.framebuffer_2
    
    def swap(self, input):
        if input == "11111111":
            if self.select_buffer == self.framebuffer_1:
                self.select_buffer = self.framebuffer_2
                self.other_buffer = self.framebuffer_1
            else:
                self.select_buffer = self.framebuffer_1
                self.other_buffer = self.framebuffer_2
    
    def update(self, input):
        if input != "00000000":
            self.other_buffer.writec((int(input[0:3], 2)*8) + int(input[3:6], 2), input[6:8])
        color = (0, 0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i in range(self.select_buffer.size):
            x = int(self.select_buffer.readx(i), 2)
            y = int(self.select_buffer.ready(i), 2)
            color_index = self.select_buffer.readc(i)
            if color_index == "00":
                color = (0, 0, 0)
            elif color_index == "01":
                color = (255, 0, 255)
            elif color_index == "10":
                color = (0, 255, 255)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(self.display, color, (y * 60, x * 60, 60, 60))
        pygame.display.update()

pygame.init()
cpu = CPU("00000000")
display = Display()
com_clock = Clock(100)

# VRAM = 28160 -> 220 frames (1 frame per second) each frame 8x8 pixels

while True:
    com_clock.delay()
    cpu.run()
    display.swap(cpu.output_b)
    display.update(cpu.output)