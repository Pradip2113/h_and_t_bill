import frappe

# Fetch the document
doc = frappe.get_doc("Agriculture Development", "YourDocType")

# Find the child table field
for field in doc.get("fields"):
    if field.fieldtype == "Table" and field.options == "YourChildTable":
        child_table = field
        break

# Hide a specific column in the child table
for field in child_table.get("fields"):
    if field.fieldname == "YourColumnToHide":
        field.hidden = 1
        break

# Save the changes
doc.save()  
