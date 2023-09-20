from . import __version__ as app_version

app_name = "h_and_t_bill"
app_title = "H And T Bill"
app_publisher = "Abhishek"
app_description = "This is H and T Billing App"
app_email = "abhishekshinde9503@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/h_and_t_bill/css/h_and_t_bill.css"
# app_include_js = "/assets/h_and_t_bill/js/h_and_t_bill.js"

# include js, css files in header of web template
# web_include_css = "/assets/h_and_t_bill/css/h_and_t_bill.css"
# web_include_js = "/assets/h_and_t_bill/js/h_and_t_bill.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "h_and_t_bill/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "h_and_t_bill.utils.jinja_methods",
#	"filters": "h_and_t_bill.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "h_and_t_bill.install.before_install"
# after_install = "h_and_t_bill.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "h_and_t_bill.uninstall.before_uninstall"
# after_uninstall = "h_and_t_bill.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "h_and_t_bill.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    
        # "cron": {
        #     "1 * * * *": [
        #          "h_and_t_bill.h_and_t_bill.doctype.practice.email7.send_email"
        #     ]
        # }, 
        # "all": [
        #     "h_and_t_bill.test_mail6.all"
        # ],
        # "daily": [
        #     "h_and_t_bill.test_mail6.daily"
        # ],
        
        "hourly": [
            "h_and_t_bill.h_and_t_bill.doctype.practice.email7.send_email"
        ],
        
        # "weekly": [
        #     "h_and_t_bill.test_mail6.weekly"
        # ],
        # "monthly": [
        #     "h_and_t_bill.test_mail6.monthly"
        # ],
}

# Testing
# -------

# before_tests = "h_and_t_bill.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "h_and_t_bill.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "h_and_t_bill.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["h_and_t_bill.utils.before_request"]
# after_request = ["h_and_t_bill.utils.after_request"]

# Job Events
# ----------
# before_job = ["h_and_t_bill.utils.before_job"]
# after_job = ["h_and_t_bill.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"h_and_t_bill.auth.validate"
# ]
