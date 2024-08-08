import os
import fitz  # PyMuPDF


def pdf_desensitize(input_file, pages: list[int], output_file):
    """
    pages: 从1开始的页码
    """
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)

    # Open the input PDF file
    doc = fitz.open(input_file)

    pages = [page - 1 for page in pages]  # 从0开始

    # Iterate through the pages
    for page_num in pages:
        if page_num < len(doc):
            # Get the page
            page = doc.load_page(page_num)
            w, h = page.rect.width, page.rect.height
            doc.delete_page(page_num)
            # Create a new empty page with the same dimensions
            doc.new_page(pno=page_num, width=w, height=h)

    # Save the modified PDF to the output file
    doc.save(output_file)
    doc.close()
    return output_file

if __name__ == '__main__':
    print(pdf_desensitize('../src/upload/ori_pdf.pdf', [1, 2], '../src/upload/ori_pdf_removed.pdf'))