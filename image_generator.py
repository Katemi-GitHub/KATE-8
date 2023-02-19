import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
win_width = 420
win_height = 420

# Set the dimensions of the cell
cell_width = win_width // 8
cell_height = win_height // 8

# Set the size of the window
win = pygame.display.set_mode((win_width, win_height))

# Set the title of the window
pygame.display.set_caption("Drawing App")

# Set the default color to black
color = (0, 0, 0)

# Create a list to store the pixel colors
pixels = [[0 for y in range(8)] for x in range(8)]

# Set the default file name
file_name = "output.txt"

# Function to save the pixel colors to a text file
def save_to_file():
    with open(file_name, "w") as file:
        for y in range(8):
            for x in range(8):
                if pixels[x][y] == 1:
                    color_code = "11"
                else:
                    color_code = "00"
                coord = bin(y)[2:].zfill(3) + bin(x)[2:].zfill(3)
                file.write(coord + color_code + "\n")

# Run the program
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the pixel colors to a text file
            save_to_file()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            # Get the cell that was clicked
            cell_x = mouse_pos[0] // cell_width
            cell_y = mouse_pos[1] // cell_height
            # Change the color of the cell
            pixels[cell_x][cell_y] = 1 - pixels[cell_x][cell_y]
            # Redraw the screen
            win.fill((255, 255, 255))
            for y in range(8):
                for x in range(8):
                    if pixels[x][y] == 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                    pygame.draw.rect(win, color, (x * cell_width, y * cell_height, cell_width, cell_height))
            pygame.display.update()

# Quit Pygame
pygame.quit()

print("code finished")
with open("output.txt", "r") as file:
    new_output = [line.strip() for line in file.readlines()]

with open("fixed_output.txt", "w") as output_file:
    for line in new_output:
        output_file.write("01010000" + "\n")
        output_file.write(line + "\n")
        output_file.write("10100000" + "\n")
        output_file.write("00000000" + "\n")
    output_file.write("10110000" + "\n")
    output_file.write("11111111" + "\n")
    output_file.write("10110000" + "\n")
    output_file.write("00000000" + "\n")