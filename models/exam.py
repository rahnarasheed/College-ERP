from odoo import models, fields, api


class Exam(models.Model):
    _name = "college.exam"

    name = fields.Char(string="Name", compute="compute_name",store=True)
    type = fields.Selection(selection=[('internal', 'Internal'),
                                       ('semester', 'Semester'), ('unit test', 'Unit Test')],
                            string="Type")
    class_id = fields.Many2one("college.class", string="Class")
    semester_id = fields.Many2one("college.semester", string="Semester")
    course_id = fields.Many2one("college.course", string="Course")
    start_date = fields.Date()
    end_date = fields.Date()
    state = fields.Selection( selection=[('draft', 'Draft'),
                                         ('confirm', 'Confirm'), ('complete', 'Complete')],
                              default='draft', string='State')
    paper_ids = fields.One2many("college.paper", "exam_id")
    student = fields.Integer(compute='compute_student', string="Student")
    mark_sheet = fields.Integer(compute='compute_mark_sheet', string="Student")
    hide_button = fields.Boolean(default=True, string="HideButton")

    @api.depends('type', 'semester_id', 'course_id')
    def compute_name(self):
        print(self)
        for record in self:
            if record.type and record.semester_id and record.course_id:
                record.name = "%s:" % record.type +\
                              "%s" % record.semester_id.name + \
                              "%s" % record.course_id.name
            else:
                record.name = False

    @api.onchange('type')
    def subject(self):
        if self.type == 'semester' and self.semester_id:
            self.write({'paper_ids': [(5, 0)]})
            for rec in self.semester_id.syllabus_ids:
                self.env['college.paper'].create({
                    'subject_id': rec.id,
                    'max_mark': rec.maximum_mark,
                    'exam_id': self.id
                })

    def generate_mark_sheet(self):
        self.write({'hide_button': False})
        # print(self.read(), "abc")
        print(self.class_id.id, "self")
        print(self.env['college.class'].browse(self.class_id.id), "selllf")
        students = self.env['college.student'].browse(self.class_id.id)
        print(students, "abvvva")
        for data in self.class_id.student_ids:
            self.env['college.sheet'].create({
                'exam_id': self.id,
                'class_id': self.class_id.id,
                'course_id': self.course_id.id,
                'semester_id': self.semester_id.id,
                'student_id': data.id,
                'paper_ids': [(0, 0, {
                    'subject_id': line.subject_id.id,
                    'pass_mark': line.pass_mark,
                    'max_mark': line.max_mark,
                }) for line in self.paper_ids]
            })
            # return {
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'tree,form',
            #     'res_model': 'college.sheet',
            #     'domain': [('exam_id', '=', self.id)],
            # }


    def get_sheet(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sheet',
            'view_mode': 'tree,form',
            'res_model': 'college.sheet',
            'domain': [('exam_id', '=', self.id)],
            'context': [('create', '=', False)]
        }

    def compute_mark_sheet(self):
        for record in self:
            record.mark_sheet = self.env['college.sheet'].search_count(
                [('exam_id', '=', self.id)])

    def get_student(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'view_mode': 'tree,form',
            'res_model': 'college.student',
            'domain': [('semester_id', '=', self.semester_id.id)],
            'context': [('create', '=', False)]
        }

    def compute_student(self):
        for record in self:
            record.student = self.env['college.student'].search_count(
                [('semester_id', '=', self.semester_id.id)])

    def expiry_check(self):
        print("yuiouyuiyi")
        today = fields.Date.today()
        exam = self.env['college.exam'].search([('state', '=', 'draft')])
        for i in exam:
            if i.end_date:
                if i.end_date < today:
                    i.write({'state': 'complete'})



  # @api.onchange('type')
  #   def subject(self):
  #       if self.type == 'semester' and self.semester_id:
  #           sub = self.env['college.semester']\
  #               .search([('id', '=', self.semester_id.id)])
  #           print(self.semester_id,sub,"ahhh")
  #           paper = self.env['college.paper']
  #           for rec in sub.syllabus_ids:
  #               paper.create({
  #                   'subject_id': rec.id,
  #                   'max_mark': rec.maximum_mark,
  #                   'exam_id': self.id
  #               })