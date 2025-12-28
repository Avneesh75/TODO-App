import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .db import dictfetchall, init_db

logger = logging.getLogger(__name__)


@csrf_exempt
def task_api(request):
    init_db()  # ensure table exists

    try:
        if request.method == "POST":
            data = json.loads(request.body)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, description, due_date, status)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        data.get("title"),
                        data.get("description"),
                        data.get("due_date"),
                        data.get("status", "pending"),
                    ),
                )

            return JsonResponse({"message": "Task created"}, status=201)

        if request.method == "GET":
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks")
                tasks = dictfetchall(cursor)

            return JsonResponse(tasks, safe=False)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        logger.exception("Task API error")
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def task_detail_api(request, task_id):
    init_db()

    try:
        if request.method == "PUT":
            data = json.loads(request.body)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = ?, description = ?, due_date = ?, status = ?
                    WHERE id = ?
                    """,
                    (
                        data.get("title"),
                        data.get("description"),
                        data.get("due_date"),
                        data.get("status"),
                        task_id,
                    ),
                )

            return JsonResponse({"message": "Task updated"})

        if request.method == "DELETE":
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tasks WHERE id = ?",
                    (task_id,),
                )

            return JsonResponse({"message": "Task deleted"})

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        logger.exception("Task Detail API error")
        return JsonResponse({"error": str(e)}, status=500)


def task_list_view(request):
    init_db()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = dictfetchall(cursor)

    return render(request, "task_list.html", {"tasks": tasks})


def task_create_view(request):
    init_db()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, description, due_date, status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (title, description, due_date, status),
                )

            return redirect("task_list")

        except Exception as e:
            logger.exception("Task create view error")
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "task_form.html")



def task_update_api(request, task_id):
    init_db()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, description = %s, due_date = %s, status = %s
                    WHERE id = %s
                    """,
                    (title, description, due_date, status, task_id),
                )

            return redirect("task_list")

        except Exception as e:
            logger.exception("Update view error")
            return JsonResponse({"error": str(e)}, status=500)

    # GET request → fetch existing task
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()

    if not task:
        return JsonResponse({"error": "Task not found"}, status=404)

    task_data = {
        "id": task[0],
        "title": task[1],
        "description": task[2],
        "due_date": task[3].split(" ")[0] if task[3] else "",
        "status": task[4],
    }

    return render(request, "task_update.html", {"task": task_data})

    

def task_delete_api(request, task_id):
    init_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,),
            )

        return redirect('task_list')

    except Exception as e:
        logger.exception("Delete API error")
        return JsonResponse({"error": str(e)}, status=500)