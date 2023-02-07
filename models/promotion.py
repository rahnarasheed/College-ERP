from odoo import models, fields


class Promotion(models.Model):
    _name = "college.promotion"
    _rec_name = "exam_id"

    exam_id = fields.Many2one('college.exam', string="Exam")
    semester_id = fields.Many2one('college.semester', string="Semester")
    class_id = fields.Many2one("college.class", string="Class")
    next_class_id = fields.Many2one("college.class", string="Next Class")
    promotion_ids = fields.One2many("college.sheet", "promotion_id")
    state = fields.Selection(selection=[('pending', 'Pending'), ('completed', 'Completed')])
    hide_button = fields.Boolean(default=True, string="HideButton")
    promote_button = fields.Boolean(default=False)

    def button_generate(self):
        self.write({'hide_button': False})
        self.write({'promote_button': True})
        if self.class_id and self.exam_id:
            print("errtrt")
            rec = self.env['college.sheet'].search([('class_id', '=', self.class_id.id),
                                                    ('exam_id', '=', self.exam_id.id), ('pass_fail', '=', True)])
            for i in rec:
                print(i, "aaaaaaaaaaaaaaaaaaaaaa")
                i.promotion_id = self.id

    def button_promote(self):
        self.write({'promote_button': False})
        self.write({'state': 'completed'})
        for line in self.promotion_ids.student_id:
            line.class_id = self.next_class_id.id
            line.semester_id = self.next_class_id.semester_id.id





        # def button_promote(self):
        #     self.env['college.class'].create({
        #     'student_ids': [(0, 0, {
        #         'first_name'= line.student_id
        #     })for line in self.promotion_ids.student_id]
        # })
        # self.write({'promotion_ids': [5, 0, 0]})
        # abc = self.env['college.class'].search([('name', '=', self.next_class_id)]).create({
        #     'student_ids': [(0, 0, {
        #         "first_name": line.student_id.first_name
        #     }) for line in self.promotion_ids]
        # })
