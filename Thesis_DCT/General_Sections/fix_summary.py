import re

with open("/Users/danielcondetorres/Desktop/TESIS_PRESENTACION/MEMORIA/TESIS/Thesis_DCT/General_Sections/Summary.tex", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix the EAAAK math block issue in Galician
    if "3$ e un péptido de poli-Ala" in line:
        new_lines[-1] = new_lines[-1].rstrip() + line.lstrip()
        continue

    new_lines.append(line)
    
    # If this line is a long text line and the next line is also a long text line, insert a blank line.
    if len(line.strip()) > 100 and not line.strip().startswith('%') and not line.strip().startswith('\\'):
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if len(next_line) > 100 and not next_line.startswith('%') and not next_line.startswith('\\'):
                new_lines.append("\n")

with open("/Users/danielcondetorres/Desktop/TESIS_PRESENTACION/MEMORIA/TESIS/Thesis_DCT/General_Sections/Summary.tex", "w") as f:
    f.writelines(new_lines)
