# -*- coding: utf-8 -*-
# from odoo import http


# class InheritUser(http.Controller):
#     @http.route('/inherit_user/inherit_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_user/inherit_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_user.listing', {
#             'root': '/inherit_user/inherit_user',
#             'objects': http.request.env['inherit_user.inherit_user'].search([]),
#         })

#     @http.route('/inherit_user/inherit_user/objects/<model("inherit_user.inherit_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_user.object', {
#             'object': obj
#         })
