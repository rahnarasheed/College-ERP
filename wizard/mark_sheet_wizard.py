from odoo import models, fields


class StudentMark(models.TransientModel):
    _name = "mark.sheet.wizard"
    _rec_name = "report"

    report = fields.Selection([('student_wise', 'Student Wise'), ('class_wise', 'Class Wise')], default='student_wise',
                              string='Report')
    student_id = fields.Many2one("college.student", string="Student")
    class_id = fields.Many2one("college.class", string="Class")
    semester_id = fields.Many2one("college.semester", string="Semester")
    exam_id = fields.Many2one("college.exam", string="Exam")
    result = fields.Char()

    def button_report(self):
        query = """select college_subject.name as subject,college_paper.mark,college_paper.pass_mark,college_paper.pass_fail as is_pass,
                            college_exam.name as exam,college_sheet.pass_fail,
                            college_student.first_name,college_semester.name as semester
                            from college_paper  
                            join college_sheet on college_paper.exam_id =college_sheet.exam_id
                            join college_student on college_sheet.student_id =college_student.id
                            join college_semester on college_sheet.semester_id=college_semester.id
                            join college_subject on college_paper.subject_id=college_subject.id
                            join college_exam on college_sheet.exam_id =college_exam.id"""
        if self.student_id and self.semester_id and self.exam_id:
            query += """ where college_student.first_name = '%s' and college_semester.name = 
            '%s' and college_exam.name = '%s' """ \
                     % (self.student_id.first_name, self.semester_id.name, self.exam_id.name)
            print(query, "qqq")

        else:
            query = query

        self.env.cr.execute(query)
        table = self.env.cr.dictfetchall()
        print(table, "table")

        for i in table:
            if i.get('is_pass') == False:
                self.result = 'Fail'
                break
            else:
                self.result = 'Pass'

        data = {
            'model_id': self.id,
            'semester_id': self.semester_id.name,
            'exam_id': self.exam_id.name,
            'class_id': self.class_id.name,
            'student_id': self.student_id.first_name,
            'course_id': self.semester_id.course_id.name,
            'academic_year': self.student_id.academic_year_id.name,
            'query': table,
            'result': self.result
        }
        return self.env.ref('college_erp.action_student_mark_sheet').report_action(None, data=data)
