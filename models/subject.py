from odoo import models, fields, api


class Subject(models.Model):
    _name = "college.subject"


    name = fields.Char(string="Subject")
    no_of_semester = fields.Char(string="No Of Semester")
    course_id = fields.Many2one("college.course")
    subject_id = fields.Many2one('college.semester', string="Subject")
    maximum_mark = fields.Float()




