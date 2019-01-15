import os
import frappe
import json
from frappe import _
from frappe.utils import get_site_path, cint, get_url
from frappe.utils.data import convert_utc_to_user_timezone
import datetime
import frappe.www.list

no_cache = 1
no_sitemap = 1

def get_context(context):
    files = ["bob", "brob", "brooob"]
    print("PARSED###########")
    #context.files = files

    todos = frappe.get_all('ToDo',fields=["name", "status", "reference_type", "reference_name", 
                                            "owner", "assigned_by", "creation", "date", "priority"], 
                                            order_by="creation asc" , filters = {"status": "Open"}, limit_page_length=10000)

    categorized_todos = {}
    for todo in todos:
        todo["creation"] = todo["creation"].strftime('%Y-%m-%d %H:%M')
        if (todo["reference_type"] == "Student Applicant"):
            application = frappe.get_doc("Student Applicant", todo["reference_name"])
            todo["first_name"] = application.first_name
            todo["last_name"] = application.last_name
            if hasattr(application, "action_step"):
                todo["action_step"] = application.action_step
            if hasattr(application, "program"):
                todo["program"] = application.program
            if hasattr(application, "student_mobile_number"):
                todo["student_mobile_number"] = application.student_mobile_number
            if hasattr(application, "student_email_address"):
                todo["student_email_address"] = application.student_email_address
            todo["comments"] = frappe.get_list('Communication', fields=['content', 'user'], filters={'reference_name': application.name})
            for comment in todo["comments"]:
                #print(comment.content)
                #print comment.content.replace("'", "\\\'")
                comment.content = json.dumps(comment.content)
                comment.content = comment.content.replace("'", "\\\'")

        # assemble into a categorized list by program
        if "program" in todo:
            program_name = todo["program"]
            if not program_name in categorized_todos:
                categorized_todos[program_name] = []
            categorized_todos[program_name].append(todo)

    print(categorized_todos)
    return {"categorized_todos": categorized_todos} 

 
@frappe.whitelist()
def add_new_comment(document_type, document_name):
    d = frappe.get_doc(document_type, document_name)
    print(d)
    z = d.add_comment("comment", text="new comment submitted here")
    return(z)
