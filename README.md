# Yautja Tablet

A Python/Tkinter tool to translate ASCII text into Yautja 16-segment characters.  
The project demonstrates progressive features across three versions, from simple translation to a fully interactive ASCII editor.

---

## Versions

### **v1 – Basic Translation**
- Loads a text file (`input.txt`)  
- Translates ASCII characters to Yautja 16-segment patterns  
- Displays Yautja characters on a canvas  
- **No scrolling, no editing**

### **v2 – Interactive Segments**
- Scrollable canvas for large text files  
- Click Yautja segments to toggle them on/off  
- Changes are updated live  
- Save translated ASCII and raw patterns via buttons

### **v3 – Editable ASCII Editor**
- Editable ASCII text field on the right-hand side  
- Arrow key navigation with blinking cursor  
- Overwrite ASCII characters with keyboard input  
- Backspace support  
- Changes to ASCII automatically update Yautja characters on the left  
- Fully interactive translation and editing

---

## Usage

1. Ensure Python 3 is installed with Tkinter.  
2. Place your text in `input.txt` or select a file via the "Load File" button.  
3. Run the desired version:

```bash
python VERSION1/yautja_v1.py
python VERSION2/yautja_v2.py
python VERSION3/yautja_v3.py
