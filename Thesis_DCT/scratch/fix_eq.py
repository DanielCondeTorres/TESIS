import re

with open("General_Sections/Methods.tex", "r") as f:
    lines = f.readlines()

in_eq = False
colon_preceded = False

for i in range(len(lines)):
    line = lines[i]
    stripped = line.strip()
    
    if stripped.startswith(r"\begin{equation}") or stripped.startswith(r"\begin{subequations}") or stripped.startswith(r"\begin{pmatrix}") or stripped.startswith(r"\begin{align}"):
        in_eq = True
        # Check previous line
        j = i - 1
        while j >= 0 and lines[j].strip() == "":
            j -= 1
        if j >= 0 and lines[j].strip().endswith(":"):
            colon_preceded = True
        else:
            colon_preceded = False
            
    elif stripped.startswith(r"\end{equation}") or stripped.startswith(r"\end{subequations}") or stripped.startswith(r"\end{pmatrix}") or stripped.startswith(r"\end{align}"):
        if colon_preceded:
            # Check lines right before \end{equation} for trailing dot or comma
            j = i - 1
            while j >= 0 and lines[j].strip() == "":
                j -= 1
            if j >= 0:
                prev_line = lines[j].rstrip()
                if prev_line.endswith(".") or prev_line.endswith(","):
                    lines[j] = prev_line[:-1] + "\n"
                    print(f"Fixed line {j+1}: {prev_line} -> {lines[j].strip()}")
        
        in_eq = False
        colon_preceded = False

with open("General_Sections/Methods.tex", "w") as f:
    f.writelines(lines)
