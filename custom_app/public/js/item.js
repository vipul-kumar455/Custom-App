frappe.ui.form.on('Item', {
    refresh: function(frm) {
        if (frm.doc.__islocal) {            
            return;
        }

        frm.add_custom_button(__('Send Email'), function() {
            sendEmail(frm);
        }, __('Actions'));
    }
});

function sendEmail(frm) {
    frappe.call({
        method: 'custom_app.public.py.item.send_email',
        args: {
            item_code: frm.doc.item_code
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint(__('Email sent successfully.'));
            } else {
                frappe.msgprint(__('Failed to send email.'));
            }
        }
    });
}
