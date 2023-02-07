from odoo import models, fields


class Exam(models.Model):
    _name = "college.sheet"
    _rec_name = 'student_id'

    student_id = fields.Many2one("college.student", string="Student")
    exam_id = fields.Many2one("college.exam", string="Exam")
    class_id = fields.Many2one("college.class", string="Class")
    semester_id = fields.Many2one("college.semester", string="Semester")
    course_id = fields.Many2one('college.course', string="Course")
    pass_fail = fields.Boolean(string="Pass/Fail")
    paper_ids = fields.One2many("college.paper", "sheet_id")
    total_mark = fields.Float(string="Total Mark")
    promotion_id = fields.Many2one("college.promotion", string="Promotion")
    year_id = fields.Many2one("academic.year")
    # rank = fields.Integer(compute='compute_rank', string='Rank')

    def compute(self):
        for record in self.paper_ids:
            if record.pass_fail:
                self.pass_fail = True
            else:
                self.pass_fail = False
        for record in self:
            self.total_mark = sum(record.paper_ids.mapped('mark'))