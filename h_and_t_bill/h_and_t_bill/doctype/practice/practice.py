# Copyright (c) 2023, Abhishek and contributors
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


# class Practice(Document):
#     @frappe.whitelist()
#     def get_data(self):
#         # create a new document
#         doc = frappe.new_doc('Test-2')
#         doc.full_name = self.name
#         doc.insert()

#     def on_trash(self):
#         frappe.msgprint("hi")
#         frappe.db.rollback()

# # Create an instance of your class
# my_instance = Practice()

# # Define a function that wraps the instance method
# def enqueue_get_data():
#     my_instance.get_data()

# # Enqueue the function with the specified delay
# enqueue(enqueue_get_data, queue='short', enqueue_after=5)


  
  
  
  
  
  
  
  
  
  
  
  # def after_login():
  #       frappe.msgprint(_("Welcome to ERPNext! This is your welcome message."), title=_("Welcome"))

# 	@frappe.whitelist()
# 	def check_developer_mode(self):
# 		try:
# 			with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
# 				config = json.load(config_file)
# 				developer_mode = config.get('developer_mode', 0)
# 				if developer_mode:
# 					frappe.msgprint("Developer mode == 1.<br><br>PLEASE TURN OFF Developer mode")
# 				else:
# 					frappe.msgprint("Developer mode == 0.")
# 		except FileNotFoundError:
# 			frappe.msgprint("File not found: site_config.json")

# class Practice(Document):
#     # pass
# 	@frappe.whitelist()
# 	def validate(self):
# 		site_config = frappe.get_site_config()
# 		developer_mode = site_config.get("developer_mode")
# 		message = "Developer Mode is currently " + ("ON" if developer_mode else "OFF")
# 		frappe.msgprint(message)

# @frappe.whitelist()
# def check_developer_mode():
#     practice = frappe.get_doc("Practice", "your_document_name")
#     if practice.is_developer_mode_enabled():
#         frappe.msgprint("Developer mode is enabled.")
#     else:
#         frappe.msgprint("Developer mode is not enabled.")

