"""
Yautja Tablet v2
- Scrollable canvas for large text files
- Interactive segment toggling by mouse (click segments to toggle)
- Map Yautja 16-bit patterns to ASCII (0-9, A-Z when available)
- Save translated ASCII to output.txt
- Load input file and render; create new characters by toggling segments

Usage:
- Run this file with Python 3 (tkinter must be available)
- Use "Load" to load an input.txt file (or choose another path)
- Click segments to toggle them on/off
- Use "Save Translation" to write the translated ASCII to output.txt
- Use the horizontal/vertical scrollbars to view large files
"""

import math
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Config ---
RADIUS = 22
SPACING_X = 40
SPACING_Y = 100
CHARS_PER_LINE = 20

# 16 direction vectors for segment drawing (normalized-ish)
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

# --- Example mapping table (shortened) ---
# digit_segments (0-9) + A..Z (some provided as examples)
# Each entry is a list/tuple of 16 ints (0/1) representing segments
BASE_SEGMENTS = [
    (1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1),  # 0
    (1,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0),  # 1
    (1,0,1,1,0,1,1,0,0,0,1,0,0,0,0,1),  # 2
    (0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1),  # 3
    (0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1),  # 4
    (1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,1),  # 5
    (0,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1),  # 6
    (1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0),  # 7
    (1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,1),  # 8
    (1,0,1,1,0,1,1,0,0,1,1,0,1,0,0,1),  # 9
    (1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0),  # A index 10
    (1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0),  # B index 11
    (1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1),  # C index 12
    (1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1),  # D index 13
    (1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1),  # E index 13
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



# build ascii_map from BASE_SEGMENTS
ascii_to_segments = {}
segments_to_ascii = {}
# map digits
for i in range(10):
    ascii_to_segments[str(i)] = BASE_SEGMENTS[i]
    segments_to_ascii[tuple(BASE_SEGMENTS[i])] = str(i)
# map some letters (A-D)
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ']
for idx, ch in enumerate(letters, start=10):
    if idx < len(BASE_SEGMENTS):
        seg = BASE_SEGMENTS[idx]
        ascii_to_segments[ch] = seg
        segments_to_ascii[tuple(seg)] = ch

# Helper: create an empty 16-bit pattern
def empty_pattern():
    return [0]*16

# Convert a pattern (list of ints) to a printable key
def pattern_key(pattern):
    return tuple(int(bool(x)) for x in pattern)

# --- GUI / Canvas drawing ---
class YautjaTablet:
    def __init__(self, root):
        self.root = root
        root.title("Yautja Tablet v2.0")

        # Top frame with buttons
        top = tk.Frame(root)
        top.pack(side='top', fill='x')

        self.load_btn = tk.Button(top, text='Load File', command=self.load_file)
        self.load_btn.pack(side='left', padx=4, pady=4)

        self.save_btn = tk.Button(top, text='Save Translation', command=self.save_translation)
        self.save_btn.pack(side='left', padx=4, pady=4)

        self.save_pattern_btn = tk.Button(top, text='Save Patterns', command=self.save_patterns)
        self.save_pattern_btn.pack(side='left', padx=4, pady=4)

        self.info_label = tk.Label(top, text='Click segments to toggle. Scroll to navigate large files.')
        self.info_label.pack(side='left', padx=8)

        # Scrollable canvas setup
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='black')
        self.hbar = tk.Scrollbar(canvas_frame, orient='horizontal', command=self.canvas.xview)
        self.vbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.hbar.pack(side='bottom', fill='x')
        self.vbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Bind click
        self.canvas.bind('<Button-1>', self.on_click)

        # Data
        self.content = []  # list of characters (strings) for display
        self.patterns = []  # list of 16-bit lists for each char
        self.item_map = {}  # maps canvas item id -> (char_index, seg_index)

        # initial render from default input.txt if exists
        try:
            with open('input.txt', 'r') as f:
                content = f.read()
                self.load_content(content)
        except FileNotFoundError:
            # start with an empty example
            self.load_content('HELLO')

    def load_file(self):
        path = filedialog.askopenfilename(title='Select text file', filetypes=[('Text files','*.txt'),('All files','*.*')])
        if not path:
            return
        with open(path,'r',encoding='utf-8',errors='ignore') as f:
            text = f.read()
        self.load_content(text)

    def load_content(self, text):
        # normalize: keep printable characters; convert newlines into spaces (or preserve?)
        text = text.replace('\r','')
        # We'll preserve newlines and treat them as separators that create empty slots
        chars = []
        for ch in text:
            if ch == '\n':
                # represent newline as special placeholder (we'll insert a gap)
                chars.append('\n')
            else:
                chars.append(ch)

        self.content = chars
        # build patterns
        self.patterns = []
        for ch in self.content:
            if ch == '\n':
                self.patterns.append(None)
            else:
                seg = None
                # try direct map
                if ch in ascii_to_segments:
                    seg = list(ascii_to_segments[ch])
                elif ch.upper() in ascii_to_segments:
                    seg = list(ascii_to_segments[ch.upper()])
                else:
                    seg = empty_pattern()
                self.patterns.append(seg)

        self.redraw()

    def redraw(self):
        self.canvas.delete('all')
        self.item_map.clear()

        total = len(self.content)
        lines = (total + CHARS_PER_LINE - 1) // CHARS_PER_LINE
        width = max(CHARS_PER_LINE * SPACING_X + 200, 800)
        height = max(lines * SPACING_Y + 200, 400)
        self.canvas.config(scrollregion=(0,0,width,height))

        # Titles
        self.canvas.create_text(450,20, text='Yautja text (click segments)', fill='red', font=('DS-Digital',16,'bold'))
        self.canvas.create_text(970,20, text='Translated ASCII', fill='red', font=('DS-Digital',16,'bold'))

        for i, ch in enumerate(self.content):
            r = i // CHARS_PER_LINE
            c = i % CHARS_PER_LINE
            off_x = 50 + c * SPACING_X
            off_y = 60 + r * SPACING_Y

            if ch == '\n':
                # draw a line break indicator
                self.canvas.create_text(off_x + 20, off_y, text='\u23CE', fill='gray', font=('Arial',20))
                continue

            pattern = self.patterns[i]
            # draw base grid (faint)
            for s in range(16):
                self._draw_segment(i, s, pattern[s] if pattern is not None else 0, off_x, off_y)

            # label ascii under
            translated = segments_to_ascii.get(pattern_key(pattern), '?') if pattern is not None else '\n'
          #  self.canvas.create_text(off_x + 60, off_y - 28, text=str(ch), fill='white', font=('Arial',10))
            self.canvas.create_text(off_x + 800, off_y + 28, text=translated, fill='cyan', font=('DS-Digital',14))

    def _draw_segment(self, char_index, seg_index, active, off_x, off_y):
        dx, dy = DIRECTIONS_16[seg_index]
        # offset for lower half segments (keep visual separation)
        offset_y = 1 if seg_index < 8 else RADIUS + 8
        x1 = off_x
        y1 = off_y + offset_y
        x2 = off_x + dx * RADIUS
        y2 = off_y + dy * RADIUS + offset_y
        width = 3 if active else 0
        color = 'red' if active else 'black'
        item = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle='round')
        # tag with char and segment
        tag = f'seg_{char_index}_{seg_index}'
        self.canvas.addtag_withtag(tag, item)
        self.item_map[item] = (char_index, seg_index)

    def on_click(self, event):
        # find item clicked
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        # search for first item that maps to a seg
        for it in items:
            if it in self.item_map:
                ci, si = self.item_map[it]
                # toggle pattern
                if self.patterns[ci] is None:
                    continue
                self.patterns[ci][si] = 0 if self.patterns[ci][si] else 1
                # redraw only that char's segments
                self._redraw_char(ci)
                return
        # if clicked empty space: optionally insert a new blank char at nearest position
        # find nearest char position
        # (optional) Not implementing insertion to keep UI simple

    def _redraw_char(self, ci):
        # Remove all segment items for this char, then redraw them
        # search tags that start with seg_ci_
        prefix = f'seg_{ci}_'
        to_delete = []
        for item, (char_index, seg_index) in list(self.item_map.items()):
            if char_index == ci:
                to_delete.append(item)
                del self.item_map[item]
        for it in to_delete:
            try:
                self.canvas.delete(it)
            except Exception:
                pass
        # compute position
        r = ci // CHARS_PER_LINE
        c = ci % CHARS_PER_LINE
        off_x = 50 + c * SPACING_X
        off_y = 60 + r * SPACING_Y
        pattern = self.patterns[ci]
        for s in range(16):
            self._draw_segment(ci, s, pattern[s] if pattern is not None else 0, off_x, off_y)
        # update translation text under the char
        # (easiest method: full redraw small region)
        # For simplicity call redraw (could be optimized)
        self.redraw()

    def translate_patterns(self):
        out_chars = []
        for pat in self.patterns:
            if pat is None:
                out_chars.append('\n')
            else:
                ch = segments_to_ascii.get(pattern_key(pat), '?')
                out_chars.append(ch)
        return ''.join(out_chars)

    def save_translation(self):
        text = self.translate_patterns()
        try:
            with open('output.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo('Saved', 'Translated text saved to output.txt')
        except Exception as e:
            messagebox.showerror('Error', f'Could not save file: {e}')

    def save_patterns(self):
        # Save raw 0/1 patterns line-by-line for each character
        try:
            with open('patterns.txt','w',encoding='utf-8') as f:
                for pat in self.patterns:
                    if pat is None:
                        f.write('\n')
                    else:
                        f.write(''.join(str(int(bool(x))) for x in pat) + '\n')
            messagebox.showinfo('Saved', 'Patterns saved to patterns.txt')
        except Exception as e:
            messagebox.showerror('Error', f'Could not save patterns: {e}')


if __name__ == '__main__':
    root = tk.Tk()
    app = YautjaTablet(root)
    root.mainloop()
