#!/usr/bin/env python3
"""
generate_bonded.py  –  TikZ/LaTeX approach
Outputs: bond_stretching.png  angle_bending.png  dihedral_proper.png  dihedral_improper.png
"""
import os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DPI  = 300

# ── PDF → PNG ──────────────────────────────────────────────────────────────

def pdf_to_png(pdf, png):
    base = png[:-4]
    tools = []
    if shutil.which('pdftoppm'):
        tools.append(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', pdf, base])
    if shutil.which('convert'):
        tools.append(['convert', '-density', str(DPI), '-background', 'white',
                      '-flatten', pdf, png])
    if shutil.which('gs'):
        tools.append(['gs', '-dNOPAUSE', '-dBATCH', '-dFirstPage=1', '-dLastPage=1',
                      f'-r{DPI}', '-sDEVICE=png16m', f'-sOutputFile={png}', pdf])
    for cmd in tools:
        subprocess.run(cmd, capture_output=True, cwd=HERE)
        for s in ['.png', '-1.png', '-01.png']:
            c = base + s
            if os.path.exists(c) and c != png:
                os.rename(c, png)
                break
        if os.path.exists(png):
            return True
    return False

def compile_figure(name, tex):
    tf = os.path.join(HERE, name + '.tex')
    pf = os.path.join(HERE, name + '.pdf')
    pg = os.path.join(HERE, name + '.png')
    with open(tf, 'w') as f:
        f.write(tex)
    r = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory', HERE, tf],
        capture_output=True, text=True, cwd=HERE)
    if r.returncode != 0:
        print(f'LaTeX error ({name}):')
        print('\n'.join(r.stdout.splitlines()[-25:]))
        return
    if pdf_to_png(pf, pg):
        print(f'{name}.png  OK')
    else:
        print(f'{name}: PDF-to-PNG failed')

# ── TikZ preamble ────────────────────────────────────────────────────────────

PREAMBLE = r"""\documentclass[tikz, border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{decorations.pathmorphing, arrows.meta, shadings, calc, fadings}
\pagecolor{white}
\tikzfading[name=fade north, top color=transparent!100, bottom color=transparent!0]
\tikzset{
  atom/.style = {
    circle, shading=ball, ball color=black,
    minimum size = 32pt,
    text=white, font=\Large\bfseries\itshape,
    inner sep=0pt, outer sep=0pt
  },
  spr/.style = {
    decorate,
    decoration={coil, aspect=0.45, segment length=3.0mm, amplitude=4.5mm},
    gray!60, line width=2.0pt, line cap=round
  },
  bnd/.style  = {line width=3.5pt,  line cap=round, black!90},
  rarr/.style = {-{Stealth[length=7pt,width=5.5pt]},
                  red!90!black, line width=2.8pt},
  dbl/.style  = {{Stealth[length=7pt,width=5.5pt]}-{Stealth[length=7pt,width=5.5pt]},
                  red!90!black, line width=2.8pt}
}
"""

# Panel A
TEX_A = PREAMBLE + r"""
\begin{document}
\begin{tikzpicture}
  \node[atom] (i) at (-2.5, 0) {\textit{i}};
  \node[atom] (j) at ( 2.5, 0) {\textit{j}};
  
  %% Spring between atoms
  \draw[spr] (i.east) -- (j.west);
  
  %% Red arrows above
  \draw[dbl] (-3.1, 1.0) -- (-1.9, 1.0);
  \draw[dbl] ( 1.9, 1.0) -- ( 3.1, 1.0);
  
  %% Label
  \node[font=\huge\bfseries] at (-4.0, 1.5) {A};
\end{tikzpicture}
\end{document}
"""

# Panel B
TEX_B = PREAMBLE + r"""
\begin{document}
\begin{tikzpicture}
  \coordinate (Pj) at ( 0.0, -2.5);
  \coordinate (Pi) at (-2.0,  1.0);
  \coordinate (Pk) at ( 2.0,  1.0);
  
  %% Bonds
  \draw[bnd] (Pi) -- (Pj);
  \draw[bnd] (Pk) -- (Pj);
  
  %% Spring between the middle of the bonds
  \coordinate (Mi) at ($(Pi)!0.55!(Pj)$);
  \coordinate (Mk) at ($(Pk)!0.55!(Pj)$);
  \draw[spr] (Mi) -- (Mk);
  
  %% Atoms
  \node[atom] (i) at (Pi) {\textit{i}};
  \node[atom] (k) at (Pk) {\textit{k}};
  \node[atom] (j) at (Pj) {\textit{j}};
  
  %% Red arrows above i and k
  \draw[dbl] (-2.6, 2.0) -- (-1.4, 2.0);
  \draw[dbl] ( 1.4, 2.0) -- ( 2.6, 2.0);
  
  %% Label
  \node[font=\huge\bfseries] at (-3.5, 2.3) {B};
\end{tikzpicture}
\end{document}
"""

# Panel C
TEX_C = PREAMBLE + r"""
\begin{document}
\begin{tikzpicture}[x=1cm, y=1cm]
  %% Parallelogram bounds (Book fold)
  \coordinate (ML) at (-4.5,  0.0);
  \coordinate (MR) at ( 5.0,  0.0);
  
  \coordinate (TL) at (-3.0,  2.5);
  \coordinate (TR) at ( 6.5,  2.5);
  
  \coordinate (BL) at (-3.0, -2.5);
  \coordinate (BR) at ( 6.5, -2.5);

  %% Blue plane (top half)
  \fill[blue!25!white, opacity=0.6, draw=blue!50!black, line width=1pt]
    (ML) -- (MR) -- (TR) -- (TL) -- cycle;
    
  %% Green plane (bottom half)
  \fill[green!35!white, opacity=0.6, draw=green!50!black, line width=1pt]
    (ML) -- (MR) -- (BR) -- (BL) -- cycle;
    
  %% Dashed line
  \draw[dashed, line width=2pt, black!80] (-5.0, 0) -- (6.0, 0);

  %% Atoms positions
  \coordinate (Pj) at (-1.5,  0.0);
  \coordinate (Pk) at ( 1.5,  0.0);
  \coordinate (Pi) at (-2.8, -1.8);
  \coordinate (Pl) at ( 2.8,  1.8);

  %% Bonds
  \draw[bnd] (Pi) -- (Pj);
  \draw[bnd] (Pj) -- (Pk);
  \draw[bnd] (Pk) -- (Pl);

  %% Atoms
  \node[atom] (i) at (Pi) {\textit{i}};
  \node[atom] (j) at (Pj) {\textit{j}};
  \node[atom] (k) at (Pk) {\textit{k}};
  \node[atom] (l) at (Pl) {\textit{l}};

  %% Rotation arrow around j-k
  %% Draw a curved red arrow around the j-k bond
  \draw[rarr] (-0.5, 0) ++(120:0.3cm and 0.6cm) arc (120:-160:0.3cm and 0.6cm);

  %% Label
  \node[font=\huge\bfseries] at (-5.0, 2.5) {C};
\end{tikzpicture}
\end{document}
"""

# Panel D
TEX_D = PREAMBLE + r"""
\begin{document}
\begin{tikzpicture}[x=1cm, y=1cm]
  %% Blue plane
  \coordinate (BL) at (-4.5, -1.5);
  \coordinate (BR) at ( 3.5, -1.8);
  \coordinate (TR) at ( 4.5,  1.5);
  \coordinate (TL) at (-3.5,  1.8);
  \fill[blue!20!white, opacity=0.7, draw=blue!40!black, line width=1pt]
    (BL) -- (BR) -- (TR) -- (TL) -- cycle;

  %% Coordinates
  \coordinate (Pi) at (-1.5,  0.2);
  \coordinate (Pj) at (-0.2, -1.1);
  \coordinate (Pk) at ( 2.0, -0.2);
  \coordinate (Pl) at ( 1.2,  3.0);

  %% Green triangle i-j-l
  \fill[green!35!white, opacity=0.6, draw=green!60!black, line width=1pt]
    (Pi) -- (Pj) -- (Pl) -- cycle;

  %% Bonds
  \draw[bnd] (Pi) -- (Pk);
  \draw[bnd] (Pj) -- (Pk);
  \draw[bnd] (Pk) -- (Pl);

  %% Atoms
  \node[atom] (i) at (Pi) {\textit{i}};
  \begin{scope}
    \clip (i.center) circle (16pt);
    \fill[white, path fading=fade north] ($(i.center)+(-16.2pt, -16.2pt)$) rectangle ($(i.center)+(16.2pt, 0)$);
  \end{scope}

  \node[atom] (j) at (Pj) {\textit{j}};
  \begin{scope}
    \clip (j.center) circle (16pt);
    \fill[white, path fading=fade north] ($(j.center)+(-16.2pt, -16.2pt)$) rectangle ($(j.center)+(16.2pt, 0)$);
  \end{scope}

  \node[atom] (k) at (Pk) {\textit{k}};
  \begin{scope}
    \clip (k.center) circle (16pt);
    \fill[white, path fading=fade north] ($(k.center)+(-16.2pt, -16.2pt)$) rectangle ($(k.center)+(16.2pt, 0)$);
  \end{scope}

  %% Atom l (no fade)
  \node[atom] (l) at (Pl) {\textit{l}};

  %% Vertical red double arrow
  \draw[dbl] (3.2, -0.2) -- (3.2, 3.0);

  %% Label
  \node[font=\huge\bfseries] at (-4.5, 3.0) {D};
\end{tikzpicture}
\end{document}
"""

if __name__ == '__main__':
    for name, tex in [
        ('bond_stretching',   TEX_A),
        ('angle_bending',     TEX_B),
        ('dihedral_proper',   TEX_C),
        ('dihedral_improper', TEX_D),
    ]:
        compile_figure(name, tex)
    print('All done.')
