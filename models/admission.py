from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Admission(models.Model):
    _name = "college.admission"
    _rec_name = "first_name"
    _inherit = "mail.thread"

    application_no = fields.Char(string='Application  No',
                                 required=True, readonly=True,
                                 default=lambda self: _('New'))
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Text(string="Communication Address")
    permanent_address = fields.Text(string="Permanent Address")
    same_as_ca = fields.Boolean(string='Same as Communication Address')
    phone = fields.Char(string="Phone")
    email = fields.Text(string="Email")
    course_id = fields.Many2one("college.course", string='Course')
    application_date = fields.Date(Sting='Date Of Application')
    academic_year_id = fields.Many2one("academic.year", string="Academic Year")
    previous_education = fields.Selection(
        selection=[('under_graduation', 'UnderGraduation'), ('post_graduation', 'PostGraduation'),
                   ('diploma', 'Diploma')], string='Previous Education')
    educational_institute = fields.Text(string="Educational Institute")
    transfer_certificate = fields.Binary(string='Transfer Certificate', required=True)
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('application', 'Application'),
                   ('approved', 'Approved'), ('done', 'done'),
                   ('rejected', 'Rejected')], default='draft', string='State')
    admission_date = fields.Date(default=fields.Date.today())
    admission_no = fields.Char(string='Order Reference',
                               required=True, readonly=True, default=lambda self: _('New'))
    student = fields.Integer(compute='compute_student', string="Student")
    # sale_id = fields.Many2one("sale.order", string="Sale")

    # def _academic_year(self):
    #     return [(i, i) for i in range(2000, fields.Date.today().year)]

    @api.constrains('transfer_certificate')
    def validate_tc(self):
        if not self.transfer_certificate:
            raise UserError("Upload File")

    def button_confirm(self):
        # a=self.env['college.admission'].search([])
        # print(a)
        # for rec in a:
        #     print(rec.course_id.name)
        self.write({'state': "application",
                    'application_no': self.env['ir.sequence']
                   .next_by_code('college.admission') or _('New')})
        # self.sale_id.action_confirm()

    def button_rejected(self):
        self.state = 'rejected'
        mail_template = self.env.ref('college_erp.email_template_rejection')
        print(self.env.ref('college_erp.email_template_rejection'))
        mail_template.send_mail(self.id, force_send=True)
        self.write({'state': 'rejected'})

    def button_done(self):
        self.write({'state': 'done',
                    'admission_no': self.env['ir.sequence'].next_by_code('college.student') or _('New')})
        mail_template = self.env.ref('college_erp.email_template_admission')
        mail_template.send_mail(self.id, force_send=True)

        self.env['college.student'].create({
            'admission_no': self.admission_no,
            'first_name': self.first_name,
            'admission_date': self.admission_date,
            'last_name': self.last_name,
            'father': self.father,
            'mother': self.mother,
            'email': self.email,
            'phone': self.phone,
            'communication_address': self.communication_address,
            'course_id': self.course_id.id,
            'academic_year_id': self.academic_year_id.id
        })

    def get_student(self):
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'view_mode': 'tree,form',
            'res_model': 'college.student',
            'domain': [('admission_no', '=', self.admission_no)],
            'context': [('create', '=', False)]
        }

    def compute_student(self):
        for record in self:
            record.student = self.env['college.student'].search_count(
                [('admission_no', '=', self.admission_no)])
