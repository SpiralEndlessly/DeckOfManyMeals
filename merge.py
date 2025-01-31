from PIL import Image
from subprocess import run
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def merge_svgs_to_pdf(input_folder, output_pdf):
    """
    Merges every four SVG images into a single A4 PDF page by rendering them to PNG using Inkscape.

    Parameters:
        input_folder (str): Path to the folder containing the SVG files.
        output_pdf (str): Path to the output PDF file.
    """
    # Constants for A6 dimensions in points (1 inch = 72 points)
    A6_WIDTH = 105 / 25.4 * 300  # in pixels
    A6_HEIGHT = 148 / 25.4 * 300  # in pixels

    # A4 dimensions in points
    A4_WIDTH, A4_HEIGHT = A4
    print(A4_WIDTH)
    print(A4_HEIGHT)

    # List all SVG files in the input folder
    svg_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.svg')])

    # Create the PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)

    for i in range(0, len(svg_files), 4):
        # Take the next four SVG files (or fewer if at the end)
        batch = svg_files[i:i+4]

        for index, svg_file in enumerate(batch):
            # Convert SVG to PNG using Inkscape command-line
            svg_path = os.path.join(input_folder, svg_file)
            png_path = svg_path.replace('.svg', '.png')
            run([
                "inkscape",
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={int(A6_WIDTH)}",
                f"--export-height={int(A6_HEIGHT)}",
                svg_path
            ], check=True)

            # Open the PNG as an image
            img = Image.open(png_path)

            # Calculate the position on the page
            x_offset = (index % 2) * (A4_WIDTH / 2)
            y_offset = A4_HEIGHT - ((index // 2 + 1) * (A4_HEIGHT / 2))

            # Draw the image onto the canvas
            c.drawImage(png_path, x_offset, y_offset, width=(A4_WIDTH / 2), height=(A4_HEIGHT / 2))

            # Remove the temporary PNG file
            #os.remove(png_path)

        # Finish the page
        c.showPage()

        # Draw background
        c.drawImage("img/background.png", 0, 0, width=(A4_WIDTH), height=(A4_HEIGHT))
        # Finish the page
        c.showPage()

    # Save the PDF
    c.save()

# Example usage
# merge_svgs_to_pdf("/path/to/svg/folder", "/path/to/output.pdf")


merge_svgs_to_pdf("svg", "output.pdf")
