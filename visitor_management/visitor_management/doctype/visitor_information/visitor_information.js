// Copyright (c) 2023, Tejal KUmbhar and contributors
// For license information, please see license.txt


frappe.ui.form.on('Visitor Information', {
    validate: function(frm) {
        
        var email = frm.doc.email;

        var EmailPatttern = /^[\w\.-]+@[\w\.-]+\.\w+$/

        if (!EmailPatttern.test(email)){
            frappe.throw('Please enter a valid Email.');
            frappe.validated = false; // Prevent form submission
        }


        var whatsapp_no= frm.doc.whatsapp_no;
        var indianMobilePattern = /^[6789]\d{9}$/;

        if (!indianMobilePattern.test(whatsapp_no)) {
            frappe.msgprint('Please enter a valid Indian mobile number.');
            frappe.validated = false; // Prevent form submission
        }  



        // var contact= frm.doc.contact;
        // var indianMobilePattern = /^[6789]\d{9}$/;

        // if (!indianMobilePattern.test(contact)) {
        //     frappe.msgprint('Please enter a valid Indian mobile number.');
        //     frappe.validated = false; // Prevent form submission
        // }  

       
    }
});

frappe.ui.form.on('Child Product', {
	product_name: function(frm) {
		frm.set_query("product_name", "product", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			var alreadyavailableproductintable = [];
			frm.doc.product.forEach(function(row) {
				alreadyavailableproductintable.push(row.product_name);
			});
			return {
				filters: [['name', 'not in', alreadyavailableproductintable]]
			};
		});


	}
});

