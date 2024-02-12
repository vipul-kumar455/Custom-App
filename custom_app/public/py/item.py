 
 
import frappe

@frappe.whitelist()
def send_email(item_code):
    sql_query = """
        SELECT
            si.name,
            si.posting_date
        FROM
            `tabSales Invoice` si
        INNER JOIN
            `tabSales Invoice Item` item ON si.name = item.parent
        WHERE
            item.item_code = %(item_code)s
        ORDER BY
            si.posting_date DESC
        LIMIT 5
    """

    sales_invoices = frappe.db.sql(sql_query, {'item_code': item_code}, as_dict=True)

    if not sales_invoices:
        frappe.msgprint('No sales invoices found for this item.')
        return

    attachments = []
    for invoice in sales_invoices:
        attachment_content = get_pdf_data('Sales Invoice', invoice['name'])
        attachments.append({
            'fname': f'{invoice["name"]}.pdf',
            'fcontent': attachment_content
        })

    message = frappe.render_template('custom_app/templates/emails/sales_invoice_template.html', {
        'item_name': item_code,
        'sales_invoices': sales_invoices
    })

    frappe.sendmail(
        recipients=['kumvipul1047@gmail.com'],
        subject=f'Latest Sales Invoices for Item: {item_code}',
        message=message,
        attachments=attachments,                
    )
    return True

def get_pdf_data(doctype, name):     
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)

 
 