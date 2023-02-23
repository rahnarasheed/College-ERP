from odoo import http
import io
import xlsxwriter
from odoo.http import request, content_disposition


class StudentExcelReportController(http.Controller):
    @http.route('/college_erp/excel_report/<model("mark.sheet.wizard"):report_id>', type='http', auth="user",
                csrf=False)
    def get_sale_excel_report(self, report_id=None):
        response = request.make_response(None, headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Report' + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        header_style = workbook.add_format({'align': 'center', 'bold': True})
        text_style = workbook.add_format({'align': 'center'})
        report_lines = report_id.get_student_lines()
        report = report_lines.get('report')
        query = report_lines.get('query')
        subject = report_lines.get('subject')
        # print(subject, "subject")
        sql_data = report_lines.get('mark_lines')

        if report_lines.get('report') == 'student_wise':
            # print(report_lines.get('report') == 'student_wise', "kkkkkkk")
            sheet = workbook.add_worksheet("student")
            sheet.set_column(1, 20, 25)
            sheet.write(2, 4, 'Student Wise', header_style)
            sheet.write(8, 2, 'SN.', header_style)
            sheet.write(8, 3, 'Subject', header_style)
            sheet.write(8, 4, 'Mark', header_style)
            sheet.write(8, 5, 'Pass Mark', header_style)
            sheet.write(8, 6, 'Pass/Fail', header_style)
            #
            row = 9
            number = 1
            for line in query:
                # print(line, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                sheet.set_row(row, 20)
                sheet.write(row, 2, number, text_style)
                sheet.write(row, 3, line['name'], text_style)
                sheet.write(row, 4, line['mark'], text_style)
                sheet.write(row, 5, line['pass_mark'], text_style)
                if line['pass_fail']==True:
                    sheet.write(row, 6, 'Pass', text_style)
                else:
                    sheet.write(row, 6, 'Fail', text_style)

                row += 1
                number += 1
        else:

            sheet = workbook.add_worksheet("Class")
            sheet.set_column(1, 20, 25)
            sheet.write(4, 3, 'Class Wise', header_style)
            sheet.write(8, 0, 'SN.', header_style)
            sheet.write(8, 1, 'Name', header_style)
            r = 2
            for line in subject:
                sheet.write(8, r, line, header_style)
                r = r + 1
            sheet.write(8, r, 'Obtained Mark', header_style)
            sheet.write(8, r+1, 'Total Mark', header_style)
            sheet.write(8, r + 2, 'Pass/Fail', header_style)
            #
            row = 9
            number = 1
            for lines in sql_data:
                sheet.set_row(row, 20)
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, sql_data[lines]['name'], text_style)
                col = 2
                for paper in subject:
                    sheet.write(row, col, sql_data[lines][paper], text_style)
                    col = col + 1
                sheet.write(row, col, sql_data[lines]['total_mark'], text_style)
                sheet.write(row, col+1, sql_data[lines]['max'], text_style)
                if sql_data[lines]['pass_fail'] == True:
                    sheet.write(row, col + 2, 'Pass', text_style)
                else:
                    sheet.write(row, col + 2, 'Fail', text_style)

                row += 1
                number += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response

