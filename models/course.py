from odoo import models, fields
# from odoo.tools.safe_eval import datetime


class Course(models.Model):
    _name = "college.course"

    name = fields.Char(string="Name")
    category = fields.Selection(selection=[('under_graduation', 'UnderGraduation'),
                                           ('post_graduation', 'PostGraduation'), ('diploma', 'Diploma')])
    duration = fields.Char(string='Year')
    number_of_semester = fields.Integer(string="Number Of Semester")
    course_ids = fields.One2many("college.semester", "course_id")
