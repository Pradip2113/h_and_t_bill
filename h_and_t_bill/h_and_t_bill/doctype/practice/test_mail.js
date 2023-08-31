// Assuming this code is part of a custom script in ERPNext

// Check if developer mode is active based on frappe.boot.developer_mode
// import frappe;

var developer_mode = frappe.boot.developer_mode ? 'ON' : 'OFF';

if (developer_mode === 'ON') {
    var email_content = "Developer Mode is currently ON.";
    
    frappe.call({
        method: "frappe.core.doctype.communication.email.make",
        args: {
            recipients: "vikas.deshmukh@gmail.com",
            subject: "Regarding Developer Mode",
            content: email_content,
            doctype: "Sales Invoice",  // Replace with the appropriate document type
            name: doc.name  // Assuming you have access to the document object
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint("Email sent successfully");
            }
        }
    });
}

