import json
import frappe

# @frappe.whitelist()
# def cron():
#   """
#   This function prints a message and checks the developer mode.
#   """

#   frappe.msgprint('Hi, do you have a new message')
#   print('Cron function defined')

#   try:
#     with open('/home/erpadmin/bench05-dev-vppl/sites/deverpvppl.erpdata.in/site_config.json', 'r') as config_file:
#       config = json.load(config_file)
#       developer_mode = config.get('developer_mode', 0)
#       if developer_mode:
#         print("Developer mode == 1. PLEASE TURN OFF Developer mode")
#       else:
#         print("Developer mode == 0.")
#   except FileNotFoundError:
#     print("File not found: site_config.json")

