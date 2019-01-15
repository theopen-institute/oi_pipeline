frappe.pages['pipeline'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Applicant Pipeline',
        single_column: true
    });

    $(frappe.render_template("pipeline")).appendTo(page.body.addClass("no-border"));
}