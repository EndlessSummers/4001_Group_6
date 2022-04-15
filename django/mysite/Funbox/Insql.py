import pandas as pd
from PIL import ImageGrab

import openpyxl
from openpyxl_image_loader import SheetImageLoader

#loading the Excel File and the sheet
pxl_doc = openpyxl.load_workbook('/Users/jhin_z/Desktop/sample.xlsx')
sheet = pxl_doc['Game']

#calling the image_loader
image_loader = SheetImageLoader(sheet)

#get the image (put the cell you need instead of 'A1')
image = image_loader.get('D')

#showing the image
image.show()

#saving the image
image.save('my_path/image_name.jpg')