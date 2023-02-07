from odoo import models, fields, api


class Semester(models.Model):
    _name = "college.semester"
    _rec_name = "name"

    name = fields.Char(string="Name", compute="compute_name",store=True)
    no_of_semester = fields.Char(string="No Of Semester")
    course_id = fields.Many2one("college.course")
    syllabus_ids = fields.One2many("college.subject", "subject_id")




    @api.depends('no_of_semester', 'course_id')
    def compute_name(self):
        for record in self:
            if record.no_of_semester and record.course_id:
                record.name = "Sem %s :" % record.no_of_semester + \
                              "%s" % record.course_id.name
            else:
                record.name = False
