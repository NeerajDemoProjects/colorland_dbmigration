
from odoo import _, api, fields, models

class Employee(models.Model):
    _inherit = 'hr.employee'
    has_close_option = fields.Boolean(default=False)
class PosSession(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_hr_employee(self, params):
        params['search_params']['fields'].append('has_close_option')
        employees = self.env['hr.employee'].search_read(**params['search_params'])
        print(employees)
        employee_ids = [employee['id'] for employee in employees]
        user_ids = [employee['user_id'] for employee in employees if employee['user_id']]
        manager_ids = self.env['res.users'].browse(user_ids).filtered(
            lambda user: self.config_id.group_pos_manager_id in user.groups_id).mapped('id')
        employees_barcode_pin = self.env['hr.employee'].browse(employee_ids).get_barcodes_and_pin_hashed()
        bp_per_employee_id = {bp_e['id']: bp_e for bp_e in employees_barcode_pin}
        for employee in employees:
            print(">>test2 manager_ids", manager_ids)
            employee['role'] = 'manager' if employee['has_close_option'] else 'cashier'
            employee['barcode'] = bp_per_employee_id[employee['id']]['barcode']
            employee['pin'] = bp_per_employee_id[employee['id']]['pin']

        return employees
