import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook
from .database import diemdanh_ngay


def put_vie_text(img, text, position, color, font_size = 30, font_path = "C:/Windows/Fonts/Arial.ttf",):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img

def xuat_file_diemdanh_ngay(ngay, file_path=""):
    rows = diemdanh_ngay(ngay)
    rows = [[f"DANH SACH DIEM DANH NGAY {ngay}"], ["MSSV", "Họ Tên", "Năm Sinh", "Diem Danh"]] + rows
    # Khởi tạo một workbook và Tạo một worksheet mới
    wb = Workbook()
    ws = wb.active
    
    for row_index, row_data in enumerate(rows, start=1):
        for col_index, cell_value in enumerate(row_data, start=1):
            ws.cell(row=row_index, column=col_index, value=cell_value)
    # Lưu workbook vào file Excel
    if file_path == "":
        file_path = f"diemdanh_{ngay}.xlsx"
    wb.save(file_path)
