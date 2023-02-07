
from odoo import models, fields, api


class Exam(models.Model):
    _name = "college.paper"

    subject_id = fields.Many2one("college.subject", string="Subject")
    pass_mark = fields.Float(string="Pass Mark")
    max_mark = fields.Float(string="Maximum Mark")
    exam_id = fields.Many2one('college.exam')
    mark = fields.Float(string="Mark")
    pass_fail = fields.Boolean(string="Pass/Fail")
    sheet_id = fields.Many2one("college.sheet")

    @api.onchange('mark')
    def mark_true(self):
        if self.mark >= self.pass_mark:
            self.pass_fail = True
        else:
            self.pass_fail = False
