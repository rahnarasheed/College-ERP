from odoo import models, fields


class CollegeErp(models.Model):
    _name = "college.student"
    _inherit = "mail.thread"
    _rec_name = "first_name"

    admission_no = fields.Char(string="Admission No")
    admission_date = fields.Date(string="Admission Date")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Text(string="Communication Address")
    permanent_address = fields.Text(string="Permanent Address")
    same_as_ca = fields.Boolean(string='Same as Communication Address')
    phone = fields.Integer(string="Phone")
    email = fields.Text(string="Email")
    course_id = fields.Many2one("college.admission")
    semester_id = fields.Many2one("college.semester", string="Semester")
    class_id = fields.Many2one("college.class", string='Class')
    academic_year_id = fields.Many2one("academic.year", string="Academic Year")
