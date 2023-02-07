from odoo import models, fields, api


class AcademicYear(models.Model):
    _name = "academic.year"

    name = fields.Char(string="Name", compute="compute_name", store=True)
    start_date = fields.Date()
    end_date = fields.Date()

    @api.depends('start_date', 'end_date')
    def compute_name(self):
        for i in self:
            i.name = "%s" % i.start_date + "- %s" % i.end_date

