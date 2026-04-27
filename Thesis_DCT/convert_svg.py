import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import QSize, QRectF

def svg_to_pdf(svg_path, pdf_path):
    app = QApplication(sys.argv)
    
    renderer = QSvgRenderer(svg_path)
    if not renderer.isValid():
        print(f"Error: Invalid SVG file at {svg_path}")
        return False
    
    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPaperSize(QPrinter.A4)
    printer.setOutputFileName(pdf_path)
    
    # Get the natural size of the SVG
    svg_size = renderer.defaultSize()
    
    # Set the page size to the SVG size to avoid margins
    printer.setPaperSize(QSize(svg_size.width(), svg_size.height()), QPrinter.Point)
    printer.setFullPage(True)
    
    painter = QPainter(printer)
    renderer.render(painter)
    painter.end()
    
    print(f"Successfully converted {svg_path} to {pdf_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_svg.py <input.svg> <output.pdf>")
        sys.exit(1)
    
    svg_to_pdf(sys.argv[1], sys.argv[2])
