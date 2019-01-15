frappe.pages['student-pipeline'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Student Applicant Pipeline',
		single_column: true
	});

	$(frappe.render_template("student_pipeline")).appendTo(page.body.addClass("no-border"));
}