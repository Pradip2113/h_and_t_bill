# Copyright (c) 2023, Abhishek and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
import json

class Practice(Document):
    pass
	# @frappe.whitelist()
	# def check_developer_mode(self):
	# 	try:
	# 		with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
	# 			config = json.load(config_file)
	# 			developer_mode = config.get('developer_mode', 0)
	# 			if developer_mode:
	# 				frappe.msgprint("Developer mode == 1.<br><br>PLEASE TURN OFF Developer mode")
	# 			else:
	# 				frappe.msgprint("Developer mode == 0.")
	# 	except FileNotFoundError:
	# 		frappe.msgprint("File not found: site_config.json")

# @frappe.whitelist()
# def check_developer_mode():
#     practice = frappe.get_doc("Practice", "your_document_name")
#     if practice.is_developer_mode_enabled():
#         frappe.msgprint("Developer mode is enabled.")
#     else:
#         frappe.msgprint("Developer mode is not enabled.")
