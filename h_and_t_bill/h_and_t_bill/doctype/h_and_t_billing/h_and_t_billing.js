// Copyright (c) 2023, Abhishek and contributors
// For license information, please see license.txt

frappe.ui.form.on('H and T Billing', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('H and T Billing', {
	show_list: function(frm) {
		frm.clear_table("h_and_t_table")
		frm.refresh_field('h_and_t_table')
		frm.clear_table("calculation_table")
		frm.refresh_field('calculation_table')
		frm.call({
			method:'get_data',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});
frappe.ui.form.on('H and T Billing', {
	set_item: function(frm) {
		frm.call({
			method:'selectall',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});
frappe.ui.form.on('H and T Billing', {
	do_billing: function(frm) {
		frm.clear_table("child_h_and_t_invisible")
		frm.refresh_field('child_h_and_t_invisible')
		frm.clear_table("calculation_table")
		frm.refresh_field('calculation_table')
		frm.call({
			method:'get_all_data_calcalation',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('H and T Billing', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

// frappe.ui.form.on('H and T Billing', {
// 	data: function(frm) {
// 		frm.call({
// 			method:'delete_issue_date',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}
// });