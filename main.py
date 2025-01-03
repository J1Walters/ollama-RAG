from parser import PDFParser
from config import PDF_DIR_PATH

def main():
    parser = PDFParser(PDF_DIR_PATH)
    parser.parse()

if __name__ == '__main__':
    main()
