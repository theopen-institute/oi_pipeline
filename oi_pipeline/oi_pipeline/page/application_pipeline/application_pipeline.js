frappe.pages['application-pipeline'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Student Application Pipeline',
		single_column: true
	});
}