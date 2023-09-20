// Copyright (c) 2023, Abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on('Practice', {
	// refresh: function(frm) {

	// }
});
// frappe.ui.form.on('Practice', {
//     scan(frm) {
//         // frm.set_value('user', frappe.session.user);
//         // const currentTime = new Date().toLocaleTimeString([], {
//         //     hour: '2-digit',
//         //     minute: '2-digit',
//         //     second: '2-digit'
//         // });
//         // frm.set_value('current_time', currentTime);
//         new frappe.ui.Scanner({
//             dialog: true,
//             multiple: false,
//             on_scan(data) {
//                 // Send the scanned data to the server
//                 frappe.call({
//                     method: 'your_app.qr_code_scan.doctype.qr_code_scan.qr_code_scan.process_qr_code',
//                     args: {
//                         qr_code_data: data.decodedText
//                     },
//                     callback: function(response) {
//                         if (response.message) {
//                             frm.set_value("qr_code_data", response.message);
//                         } else {
//                             frappe.msgprint("Error processing QR code data");
//                         }
//                     }
//                 });
//             }
//         });
//     }
// });



// frappe.ui.form.on('Practice', {
//     scan(frm) {
//         // frm.set_value('user', frappe.session.user);
//         // const currentTime = new Date().toLocaleTimeString([], {
//         //     hour: '2-digit',
//         //     minute: '2-digit',
//         //     second: '2-digit'
//         // });
//         // frm.set_value('current_time', currentTime);
//         new frappe.ui.Scanner({
//             dialog: true, // open camera scanner in a dialog
//             multiple: false, // stop after scanning one value
//             on_scan(data) {
//                 frappe.msgprint(data.decodedText);
//                 frm.set_value("qr_code_data", data.data);
//             }
//         });
//     }
// });

// frappe.ui.form.on('Practice', {
// 	scan: function(frm) {
// 		frm.call({
// 			method:'validate',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}
// });

// frappe.ui.form.on('Practice', {
// 	scan: function(frm) {
// 		frm.call({
// 			method:'get_data',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}
// });



// frappe.ui.form.on('Practice', {
//     refresh: function(frm) {
//         var developer_mode = frappe.boot.developer_mode ? 'ON' : 'OFF';

//         if (developer_mode === 'ON') {
//             var email_content = "Developer Mode is currently ON.";

//             frappe.call({
//                 method: "frappe.core.doctype.communication.email.make",
//                 args: {
//                     recipients: "vikas.deshmukh@gmail.com",
//                     subject: "Regarding Developer Mode",
//                     content: email_content,
//                     doctype: "Practice",  // Replace with the appropriate document type
//                     name: frm.doc.name  // Use frm.doc.name to access the document name
//                 },
//                 callback: function(response) {
//                     if (response.message) {
//                         frappe.msgprint("Email sent successfully");
//                     }
//                 }
//             });
//         }
//     }
// });
