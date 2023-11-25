from pdf2image import convert_from_path
from pathlib import Path
from .file_util import FilesUtility, delete_directory, delete_files_in_directory, create_directory, check_if_file
import datetime
import cv2
import pytesseract


from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    
    fp.close()
    device.close()
    retstr.close()
    return text

def extract_pdf_data(path):
    if check_if_file(Path(path)):
        text = convert_pdf_to_txt(path)
        if len(text)<5:
            text = ocr_pdf_data(path)
    else:
        print("path does not contain file")
        
    return text

def ocr_pdf_data(path):
    actual_path = Path(path).parent
    filesUtil = FilesUtility()
    filesUtil.user_file_path = actual_path
    file_parts = Path(path).parts
    file_name = file_parts[len(file_parts) - 1]
    name_ext_arr = str(file_name).split('.')
    filesUtil.user_file_name = name_ext_arr[0]
    filesUtil.user_file_ext = name_ext_arr[1]
    filesUtil.image_dir = name_ext_arr[0] + '-images-' + (datetime.datetime.now()).strftime("%m%d%Y%H%M%S")
    create_directory(path, filesUtil.image_dir)
    all_images = convert_pdf_get_png(actual_path, file_name)
    text=""
    for i, image in enumerate(all_images):
        if not filesUtil.is_break:
            print("file name ::: " + str(name_ext_arr[0])+"     page ::: " + str(i + 1))
            image_path = f'{actual_path}\\{filesUtil.image_dir}\\{filesUtil.image_prefix}{i}{filesUtil.image_ext}'
            image.save(image_path)
            text = text + " " + process_image(image_path)
        else:
            break
    delete_files_in_directory(f'{filesUtil.user_file_path}\\{filesUtil.image_dir}')
    delete_directory(f'{filesUtil.user_file_path}\\{filesUtil.image_dir}', filesUtil.image_dir)

    
    return text

def process_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    # img = cv2.medianBlur(img,3)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    t = pytesseract.image_to_string(img, config='--psm 6 --oem 3')
    return t
def convert_pdf_to_png(path, file):
    images = convert_from_path(f'{str(path)}/{file}', 500)
    for i, image in enumerate(images):
        image.save(f'{path}/{FilesUtility().image_dir}/save_{i}.png')


def convert_pdf_get_png(path, file):
    images = convert_from_path(f'{str(path)}/{file}', 500)
    return images