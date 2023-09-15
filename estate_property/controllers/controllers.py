# -*- coding: utf-8 -*-
# from odoo import http


# class EstateManagement(http.Controller):
#     @http.route('/estate_management/estate_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_management/estate_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_management.listing', {
#             'root': '/estate_management/estate_management',
#             'objects': http.request.env['estate_management.estate_management'].search([]),
#         })

#     @http.route('/estate_management/estate_management/objects/<model("estate_management.estate_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_management.object', {
#             'object': obj
#         })
