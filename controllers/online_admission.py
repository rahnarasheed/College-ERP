import base64

from odoo import http
from odoo.http import request


class OnlineAdmission(http.Controller):

    @http.route('/online/admission', auth='public', website=True)
    def admission_form(self):
        course = request.env['college.course'].sudo().search([])
        academic_year = request.env['academic.year'].sudo().search([])
        print(course, "course")
        print(academic_year,"year")
        vals = {
            'course': course,
            'year': academic_year,
        }
        # product = request.env['product.product'].sudo().search([])
        return http.request.render('college_erp.admission_form', vals)
            # 'products': product,})

    @http.route('/online/admission/submit', auth='public', website=True)
    def admission_submit_form(self, **post):
        print(post.get('first_name'))
        admission = request.env['college.admission'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            # 'transfer_certificate': post.get('transfer_certificate'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'communication_address': post.get('address'),
            'course_id': post.get('course_id'),
            'academic_year_id': post.get('academic_year')
        })
        # detail = request.env['college.admission'].sudo().search([])[-1]
        file_name = post.get('transfer_certificate').filename
        file = post.get('transfer_certificate')
        attachment_id = request.env['ir.attachment'].sudo().create({
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_model': 'college.admission',
            'res_id': admission.id,
            'res_field': 'transfer_certificate'
        })
        vals = {
            'student': admission,
        }
        return request.render("college_erp.student_form_success", vals)
