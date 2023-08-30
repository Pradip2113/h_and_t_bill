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