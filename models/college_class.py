from odoo import models, fields, api


class Class(models.Model):
    _name = "college.class"

    name = fields.Char(string="Name", compute="compute_name", store=True)
    semester_id = fields.Many2one("college.semester", string="Semester")
    course_id = fields.Many2one("college.course")
    academic_year_id = fields.Many2one("academic.year", string="Academic Year")
    student_ids = fields.One2many("college.student", 'class_id', string='Student')
    promotion_id = fields.Many2one('college.class', string="Promotion Class")

    @api.depends('semester_id', 'academic_year_id')
    def compute_name(self):
        for record in self:
            if record.semester_id and record.academic_year_id:
                record.name = "%s:" % record.semester_id.name + "%s" % record.academic_year_id.name
            else:
                record.name = False

    # def _academic_year(self):
    #     current_year = date.today()
    #     print(current_year)
    #     year = current_year.year
    #     print(year)
    #     year_list = []
    #     for i in range(2000, year):
    #         print(i)
    #         year_list.append((i, i))
    #     print(year_list)
    #     return year_list

    # @api.onchange('course_id')
    # def student_class(self):
    #     print('self.semester_id', self.semester_id)
    #     print('self.academic_year_id', self.academic_year_id)
    #     print('self.course_id', self.course_id)
    #     if self.semester_id and self.academic_year_id and self.course_id:
    #         print('qqqqqqqqqqq', self.semester_id,self.academic_year_id,self.course_id)
    #         rec = self.env['college.student'].search([('semester_id', '=', self.semester_id.id),
    #                                               ('course_id', '=', self.course_id.id),
    #                                               ('academic_year_id', '=', self.academic_year_id.id)])
    #         print(rec,"fdeyd")
    #         for i in rec:
    #             i.student_id = self.id

