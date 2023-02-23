from odoo import models, fields,api


class StudentMark(models.TransientModel):
    _name = "mark.sheet.wizard"
    _rec_name = "report"

    report = fields.Selection([('student_wise', 'Student Wise'), ('class_wise', 'Class Wise')], default='student_wise',
                              string='Report')
    student_id = fields.Many2one("college.student", string="Student")
    class_id = fields.Many2one("college.class", string="Class")
    semester_id = fields.Many2one("college.semester", string="Semester")
    exam_type = fields.Selection(selection=[('internal', 'Internal'),
                                            ('semester', 'Semester'), ('unit test', 'Unit Test')],
                                 string="Type")
    result = fields.Char()


    @api.onchange('report')
    def onchange_report(self):
        if self.report == 'student_wise':
            self.student_id = None
            self.semester_id = None
            self.exam_type = None
        else:
            self.semester_id = None
            self.class_id = None
            self.exam_type = None


    def button_report(self):
        if self.report == 'student_wise':
            query = """select college_subject.name,college_paper.mark,
                        college_paper.pass_mark,college_paper.pass_fail,
                        college_sheet.student_id,college_sheet.pass_fail as is_pass,college_exam.type
                        from college_subject
                         inner join college_paper on college_paper.
                        subject_id=college_subject.id 
                        inner join college_sheet on college_paper.
                        sheet_id=college_sheet.id
                        inner join college_exam on college_sheet.exam_id=college_exam.id where 1=1"""
            if self.student_id:
                query += """ And college_sheet.student_id = '%s' """ \
                         % self.student_id.id

            if self.semester_id:
                query += """ And college_sheet.semester_id=
                                                   '%s' """ % self.semester_id.id

            if self.exam_type:
                query += """ And college_exam.type='%s' """ % self.exam_type

                print("hi")
            query = query

            self.env.cr.execute(query)
            table = self.env.cr.dictfetchall()
            print(table, "table")

            for i in table:
                if i.get('is_pass') == False:
                    self.result = 'Fail'
                else:
                    self.result = 'Pass'

            data = {
                'model_id': self.id,
                'semester_id': self.semester_id.name,
                'exam_type': self.exam_type,
                'class_id': self.class_id.name,
                'student_id': self.student_id.first_name,
                'course_id': self.semester_id.course_id.name,
                'academic_year': self.student_id.academic_year_id.name,
                'query': table,
                'result': self.result}
            return self.env.ref('college_erp.action_student_mark_sheet').report_action(None, data=data)
        else:
            # print("hi")
            query = """select college_sheet.student_id,college_student.first_name,
                        college_subject.name,
                        college_paper.mark,college_sheet.total_mark,
                        college_sheet.pass_fail,college_sheet.max_mark,
                        college_exam.type
						from college_sheet 
						inner join college_student on college_sheet.student_id=college_student.id
						inner join college_paper on college_paper.sheet_id=college_sheet.id
						inner join college_subject on college_paper.subject_id=college_subject.id
						inner join college_exam on college_sheet.exam_id=college_exam.id where 1=1"""
            if self.class_id:
                query += """ And college_sheet.class_id = '%s'""" \
                         % self.class_id.id
                # print(query, "qqq")
            if self.semester_id:
                query += """ And college_sheet.semester_id='%s' """ \
                         % self.semester_id.id

            if self.exam_type:
                query += """ and college_exam.type='%s' """ \
                         % self.exam_type

            query = query

            self.env.cr.execute(query)
            table = self.env.cr.dictfetchall()
            # print(table, "table")
            student_list = set([std['student_id'] for std in table])
            # print(student_list, "lissssst12222")
            val = {}
            for std in student_list:
                # print(std)
                for i in table:
                    # print(i)
                    if not val.get(std, False):
                        # print("Hello", std, i['student_id'])
                        if std == i['student_id']:
                            val[std] = {'name': i['first_name'],
                                        i['name']: i['mark'],
                                        'total_mark': i['total_mark'], 'pass_fail': i['pass_fail'],
                                        'max': i['max_mark']}

                    else:
                        if std == i['student_id']:
                            # print(val[std], i['name'])
                            val[std][i['name']] = i['mark']
                        # print(val, 'wwwwwwwwww', i['student_id'], std)

            pass_count = 0
            fail_count = 0
            std_count = 0
            for rec in val:
                std_count += 1
                # print(rec, "rec")
                if val[rec]['pass_fail'] == True:
                    pass_count += 1
                else:
                    fail_count += 1
                # print(std_count, "11")

            subjects = [*set(i.get('name') for i in table)]
            # print(subjects, "aaa")

            data = {
                'semester_id': self.semester_id.name,
                'exam_type': self.exam_type,
                'class_id': self.class_id.name,
                'course_id': self.semester_id.course_id.name,
                'academic_year': self.class_id.academic_year_id.name,
                'query': table,
                'subject': subjects,
                'mark_lines': val,
                'pass_count': pass_count,
                'fail_count': fail_count,
                'student_count': std_count,
            }

            return self.env.ref('college_erp.action_class_mark_sheet').report_action(None, data=data)

    def button_xlsx(self):
        print("hey")
        return {
            'type': 'ir.actions.act_url',
            'url': '/college_erp/excel_report/%s' % (self.id),
            # 'url': '/class_erp/excel_report/%s' % (self.id),
            'target': 'new',
        }

    def get_student_lines(self):
        if self.report == 'student_wise':
            query = """select college_subject.name,college_paper.mark,
                                college_paper.pass_mark,college_paper.pass_fail,
                                college_sheet.student_id,college_sheet.pass_fail as is_pass,college_exam.type
                                from college_subject
                                 inner join college_paper on college_paper.
                                subject_id=college_subject.id 
                                inner join college_sheet on college_paper.
                                sheet_id=college_sheet.id
                                inner join college_exam on college_sheet.exam_id=college_exam.id where 1=1"""
            if self.student_id:
                query += """ And college_sheet.student_id = '%s' """ \
                         % self.student_id.id

            if self.semester_id:
                query += """ And college_sheet.semester_id=
                                                           '%s' """ % self.semester_id.id

            if self.exam_type:
                query += """ And college_exam.type='%s' """ % self.exam_type

                # print("hi")
            query = query

            self.env.cr.execute(query)
            table = self.env.cr.dictfetchall()
            # print(table, "table")

            for i in table:
                if i.get('is_pass') == False:
                    self.result = 'Fail'
                else:
                    self.result = 'Pass'

            data = {
                'report':self.report,
                'model_id': self.id,
                'semester_id': self.semester_id.name,
                'exam_type': self.exam_type,
                'class_id': self.class_id.name,
                'student_id': self.student_id.first_name,
                'course_id': self.semester_id.course_id.name,
                'academic_year': self.student_id.academic_year_id.name,
                'query': table,
                'result': self.result}
            return  data
        else:
            # print("hi")
            query = """select college_sheet.student_id,college_student.first_name,
                                college_subject.name,
                                college_paper.mark,college_sheet.total_mark,
                                college_sheet.pass_fail,college_sheet.max_mark,
                                college_exam.type
        						from college_sheet 
        						inner join college_student on college_sheet.student_id=college_student.id
        						inner join college_paper on college_paper.sheet_id=college_sheet.id
        						inner join college_subject on college_paper.subject_id=college_subject.id
        						inner join college_exam on college_sheet.exam_id=college_exam.id where 1=1"""
            if self.class_id:
                query += """ And college_sheet.class_id = '%s'""" \
                         % self.class_id.id
                # print(query, "qqq")
            if self.semester_id:
                query += """ And college_sheet.semester_id='%s' """ \
                         % self.semester_id.id

            if self.exam_type:
                query += """ and college_exam.type='%s' """ \
                         % self.exam_type

            query = query

            self.env.cr.execute(query)
            table = self.env.cr.dictfetchall()
            # print(table, "table")
            student_list = set([std['student_id'] for std in table])
            # print(student_list, "lissssst12222")
            val = {}
            for std in student_list:
                # print(std)
                for i in table:
                    # print(i)
                    if not val.get(std, False):
                        # print("Hello", std, i['student_id'])
                        if std == i['student_id']:
                            val[std] = {'name': i['first_name'],
                                        i['name']: i['mark'],
                                        'total_mark': i['total_mark'], 'pass_fail': i['pass_fail'],
                                        'max': i['max_mark']}

                    else:
                        if std == i['student_id']:
                            print(val[std], i['name'])
                            val[std][i['name']] = i['mark']
                        print(val, 'wwwwwwwwww', i['student_id'], std)

            pass_count = 0
            fail_count = 0
            std_count = 0
            for rec in val:
                std_count += 1
                # print(rec, "rec")
                if val[rec]['pass_fail'] == True:
                    pass_count += 1
                else:
                    fail_count += 1
                # print(std_count, "11")

            subjects = [*set(i.get('name') for i in table)]
            # print(subjects, "aaa")

            data = {
                'report': self.report,
                'semester_id': self.semester_id.name,
                'exam_type': self.exam_type,
                'class_id': self.class_id.name,
                'course_id': self.semester_id.course_id.name,
                'academic_year': self.class_id.academic_year_id.name,
                'query': table,
                'subject': subjects,
                'mark_lines': val,
                'pass_count': pass_count,
                'fail_count': fail_count,
                'student_count': std_count,
            }

            return  data

