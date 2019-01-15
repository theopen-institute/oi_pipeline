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
		comment.content = None
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
    
    # def get_time(path):
    #   dt = os.path.getmtime(path)
    #   return convert_utc_to_user_timezone(datetime.datetime.utcfromtimestamp(dt)).strftime('%Y-%m-%d %H:%M')

    # def get_size(path):
    #   size = os.path.getsize(path)
    #   if size > 1048576:
    #       return "{0:.1f}M".format(float(size) / 1048576)
    #   else:
    #       return "{0:.1f}K".format(float(size) / 1024)

    # path = get_site_path('private', 'backups')
    # files = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
    # backup_limit = get_scheduled_backup_limit()

    # if len(files) > backup_limit:
    #   cleanup_old_backups(path, files, backup_limit)

    # files = [('/backups/' + _file,
    #   get_time(os.path.join(path, _file)),
    #   get_size(os.path.join(path, _file))) for _file in files if _file.endswith('sql.gz')]
    # files.sort(key=lambda x: x[1], reverse=True)
