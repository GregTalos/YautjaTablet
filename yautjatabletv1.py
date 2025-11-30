"""
Yautja Tablet v1
- Loads a text file (input.txt)
- Translates ASCII characters to Yautja 16-segment patterns
- Displays Yautja characters on a canvas
- No scrolling, no editing
"""

import math
import tkinter as tk

# Constants adjusted for smaller characters
RADIUS = 22  # Smaller radius for the characters
SPACING = 40  # Smaller spacing between characters
DIGIT_COUNT = 40  # Display 40 characters in total

# 16 direction vectors for segment drawing
DIRECTIONS_16 = {
    0:  (0, -0.72),
    1:  (math.sqrt(2)/2, -math.sqrt(2)/2),
    2:  (0.72, 0),
    3:  (math.sqrt(2)/2, math.sqrt(2)/2),
    4:  (0, 0.72),
    5:  (-math.sqrt(2)/2, math.sqrt(2)/2),
    6:  (-0.72, 0),
    7:  (-math.sqrt(2)/2, -math.sqrt(2)/2),
    8:  (0, -0.72),
    9:  (math.sqrt(2)/2, -math.sqrt(2)/2),
    10: (0.72, 0),
    11: (math.sqrt(2)/2, math.sqrt(2)/2),
    12: (0, 0.72),
    13: (-math.sqrt(2)/2, math.sqrt(2)/2),
    14: (-0.72, 0),
    15: (-math.sqrt(2)/2, -math.sqrt(2)/2),
}

# Define the Yautja segments for numbers (same as in your original code)
digit_segments = [
    [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],  # 0
    [1,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0],  # 1
    [1,0,1,1,0,1,1,0,0,0,1,0,0,0,0,1],  # 2
    [0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1],  # 3
    [0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1],  # 4
    [1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,1],  # 5
    [0,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1],  # 6
    [1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0],  # 7
    [1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,1],  # 8
    [1,0,1,1,0,1,1,0,0,1,1,0,1,0,0,1],  # 9
    [1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0],  # A
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],  # B
    [1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1],  # C
    [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],  # D
    [1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1],  # E
    (1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,1),  # F index 14
    (1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),  # G index 15
    (1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0),  # H index 16
    (0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1),  # I index 17
    (1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1),  # J index 18
    (1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0),  # K index 19
    (1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1),  # L index 20     
    (1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),  # M index 21
    (1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0),  # N index 22
    (1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1),  # O index 23
    (1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1),  # P index 24
    (1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1),  # Q index 25
    (1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0),  # R index 26
    (0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1),  # S index 27
    (0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1),  # T index 28
    (1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0),  # U index 29   
    (1,1,1,1,0,0,0,0,0,1,0,0,1,0,0,0),  # V index 30
    (1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1),  # W index 31
    (0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1),  # X index 32
    (0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1),  # Y index 33
    (1,1,1,1,0,0,0,0,0,1,0,0,1,0,0,1),  # Z index 34
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),  #   index 35 (space)
]

# Function to draw a single segment of a character
def draw_segment(canvas, i, center_x, center_y, color, width):
    dx, dy = DIRECTIONS_16[i]
    
    # Adjust the vertical offset to the new character size
    offset_y = 0 if i < 8 else RADIUS + 8  # Reduce the vertical offset to RADIUS

    # Define the starting and ending points for the segment
    x1 = center_x
    y1 = center_y + offset_y
    x2 = center_x + dx * RADIUS
    y2 = center_y + dy * RADIUS + offset_y
    
    # Draw the segment
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

# Function to draw the base grid of a Yautja character
def draw_base_grid(canvas, center_x, center_y):
    for i in range(16):
        draw_segment(canvas, i, center_x, center_y, 'gray', 1)

# Function to draw the active Yautja segments
def draw_yautja_segments(canvas, segments, center_x, center_y):
    for i, active in enumerate(segments):
        if active:
            draw_segment(canvas, i, center_x, center_y, 'red', 3)

# Function to draw a single Yautja digit on the canvas
def draw_digit(canvas, segments, digit_index, char=None, offset_x=100, offset_y=100):
    spacing = 0  # You can adjust spacing here to ensure proper alignment
    center_x = offset_x + digit_index * spacing
    center_y = offset_y  # Vertical position, keep it small so the characters fit
    draw_base_grid(canvas, center_x, center_y)
    draw_yautja_segments(canvas, segments, center_x, center_y)
    if char is not None:
        canvas.create_text(center_x+400, center_y , text=char, fill='red', font=('DS-Digital', 24, 'bold'))

# Function to load characters from a file and convert them to Yautja segments
def load_characters_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content

# Function to draw the tablet display of characters
def draw_yautja_tablet(canvas, content, offset_x=100, offset_y=100, spacing=SPACING):
    characters_per_line = 10  # Display up to 10 characters per line
    for i, char in enumerate(content):
        # Check if the character is a digit or a letter
        if char.isdigit():  # Handling digits
            segs = digit_segments[int(char)]
        elif char.isalpha():  # Handling letters (A-Z)
            # Map letters to their respective Yautja segment patterns
            index = ord(char.upper()) - ord('A')  # Map A-Z to 0-25
            if 0 <= index < len(digit_segments):
                segs = digit_segments[index + 10]  # Adjust based on your offset
            else:
                segs = digit_segments[0]  # Default to 0 if letter mapping is missing
        else:
            # For non-alphanumeric characters, fallback to default (blank or placeholder)
            segs = digit_segments[0]  # Default to 0 if no mapping exists
        
        # Calculate the row and column of the character
        row = i // characters_per_line
        col = i % characters_per_line
        
        # Calculate the offset_y for the current row
        new_offset_y = offset_y + row * (RADIUS * 3 + 2)  # Increase vertical spacing per line
        
        # Draw the character at the correct position
        draw_digit(canvas, segs, col, char, offset_x + col * spacing, new_offset_y)

# Function to create the tablet interface with dynamic canvas size
def create_tablet_interface(file_path):
    content = load_characters_from_file(file_path)
    
    # Calculate the canvas width based on the number of characters and new spacing
    canvas_width = len(content) * SPACING /3 # Adjusted canvas width for 40 characters
    # Calculate the canvas height based on the number of lines required (10 characters per line)
    canvas_height = 400 + (len(content) // 10 + 1) * (RADIUS + 10)  # Add extra space for final line
    
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Yautja Character Tablet v1.0")

    # Create the canvas with dynamic width and height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black')
    canvas.pack()
    canvas.create_text(280,55 , text="Yautja text", fill='red', font=('DS-Digital', 22, 'bold'))
    canvas.create_text(690,55 , text="Human ASCII text", fill='red', font=('C059', 22, 'bold'))
    canvas.create_text(490,15 , text="Human ASCII text file : input.txt", fill='red', font=('Bitstream Charter', 22, 'bold'))    # Draw Yautja characters on the canvas
    draw_yautja_tablet(canvas, content)

    # Start the Tkinter main loop
    root.mainloop()

# Example of using the tablet to display characters from a file



create_tablet_interface("input.txt")  # Assuming input.txt contains "HELLO" or any text
