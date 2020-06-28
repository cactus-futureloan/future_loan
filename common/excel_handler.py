from pprint import pprint
import openpyxl


class ExcelHandler():
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = None

    def open_file(self):
        """打开表格"""
        workbook = openpyxl.load_workbook(self.file_path)
        self.workbook = workbook
        return workbook

    def get_sheet(self, sheet_name):
        """获取sheet表单"""
        workbook = self.open_file()
        sheet = workbook[sheet_name]
        return sheet

    def read_data(self, sheet_name):
        """读取数据"""
        sheet = self.get_sheet(sheet_name)
        rows_data = list(sheet.rows)
        # 获取标题
        title_data = []
        for title in rows_data[0]:
            title_data.append(title.value)

        # 获取值
        test_data = []
        for row in rows_data[1:]:
            row_data = {}
            for index, cell in enumerate(row):
                row_data[title_data[index]] = cell.value
            test_data.append(row_data)

        return test_data

    def write(self, sheet_name, row, column, data):
        """写入数据"""
        sheet = self.get_sheet(sheet_name)
        cell = sheet.cell(row, column)
        cell.value = data
        self.save()
        self.close()

    def save(self):
        """保存文件"""
        self.workbook.save(self.file_path)

    def close(self):
        """关闭文件"""
        self.workbook.close()


if __name__ == '__main__':
    wb = ExcelHandler("D:\workspace\Future_Loan_1\data\cases.xlsx")
    data = wb.read_data("Sheet1")
    pprint(data)
