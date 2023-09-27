import openpyxl
workbook = openpyxl.Workbook()
sheet = workbook.worksheets[0]
sheet['A1'] = 'Hello Python, Hello Excel.'
workbook.save('test.xlsx')

