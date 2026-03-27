# Importing libraries
from sqlalchemy import func

from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from models.staff_table import Staff
from models.lawyers_table import Lawyers
from models.tasks_table import Tasks, TaskStatus
from sqlalchemy.orm import Session
from dtos.task_models import TaskModel as CreateTaskRequest, UpdateTaskRequest
from datetime import date


class TaskController:

    def create_task(create_task_request: CreateTaskRequest, user: UserModel, db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        if user.role not in ['lawyer', 'staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        task = Tasks(
            title=create_task_request.title,
            description=create_task_request.description,
            caseId=create_task_request.caseId,
            assignedTo=user.id,
            dueDate=create_task_request.dueDate,
            priority=create_task_request.priority,
            status=TaskStatus.PENDING
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    def read_all(user: UserModel, db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        if user.role not in ['lawyer', 'staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        if user.role == 'lawyer':
            lawyer = db.query(Lawyers).filter(Lawyers.userId == user.id).first()

            if not lawyer:
                return APIHelper.send_not_found_error(errorMessageKey='translations.LAWYER_NOT_FOUND')

            if lawyer.isBlocked == 1:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')

        elif user.role == 'staff':
            staff = db.query(Staff).filter(
                Staff.user_id == user.id
            ).first()

            if not staff:
                return APIHelper.send_not_found_error(errorMessageKey='translations.STAFF_NOT_FOUND')

            if staff.isBlocked == 1:
                return APIHelper.send_forbidden_error(errorMessageKey='translations.BLOCKED')
        tasks = db.query(Tasks).filter(
        Tasks.assignedTo == user.id,
        Tasks.isDeleted == 0
        ).all()

        # 🔹 Counts 
        pending_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.assignedTo == user.id,
            Tasks.isDeleted == 0,
            Tasks.status == TaskStatus.PENDING
        ).scalar()

        overdue_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.assignedTo == user.id,
            Tasks.isDeleted == 0,
            Tasks.status == TaskStatus.OVERDUE
        ).scalar()

        completed_tasks = db.query(func.count(Tasks.id)).filter(
            Tasks.assignedTo == user.id,
            Tasks.isDeleted == 0,
            Tasks.status == TaskStatus.COMPLETED
        ).scalar()

        # 🔹 Final response
        return {
            "tasks": tasks,
            "summary": {
                "pending": pending_tasks,
                "overdue": overdue_tasks,
                "completed": completed_tasks
            }
        }

    def update_task(task_id: int, update_task_request: UpdateTaskRequest, user: UserModel, db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        if user.role not in ['lawyer', 'staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.isDeleted == 0
        ).first()

        if not task:
            return APIHelper.send_not_found_error(errorMessageKey='translations.TASK_NOT_FOUND')

        if task.assignedTo != user.id:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ASSIGNED_TO_THIS_TASK')

        # ✅ NEW LOGIC: Prevent update if completed/overdue
        if task.status in [TaskStatus.COMPLETED, TaskStatus.OVERDUE]:
            return APIHelper.send_bad_request_error(
                errorMessageKey='translations.TASK_ALREADY_COMPLETED'
            )

        update_data = update_task_request.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)

        return task

    def delete_task(task_id: int, user: UserModel, db: Session):
        if user is None:
            return APIHelper.send_unauthorized_error(errorMessageKey='translations.UNAUTHORIZED')

        if user.role not in ['lawyer', 'staff']:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.FORBIDDEN')

        task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.isDeleted == 0
        ).first()

        if not task:
            return APIHelper.send_not_found_error(errorMessageKey='translations.TASK_NOT_FOUND')

        if task.assignedTo != user.id:
            return APIHelper.send_forbidden_error(errorMessageKey='translations.NOT_ASSIGNED_TO_THIS_TASK')

        # Delete allowed even if completed
        db.delete(task)
        db.commit()

        return {"message": "Task deleted successfully"}

    def mark_as_done(task_id: int, user: UserModel, db: Session):

        if user is None:
            return APIHelper.send_unauthorized_error(
                errorMessageKey='translations.UNAUTHORIZED'
            )

        if user.role not in ['lawyer', 'staff']:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.FORBIDDEN'
            )

        task = db.query(Tasks).filter(
            Tasks.id == task_id,
            Tasks.isDeleted == 0
        ).first()

        if not task:
            return APIHelper.send_not_found_error(
                errorMessageKey='translations.TASK_NOT_FOUND'
            )

        if task.assignedTo != user.id:
            return APIHelper.send_forbidden_error(
                errorMessageKey='translations.NOT_ASSIGNED_TO_THIS_TASK'
            )

        # Prevent re-marking
        if task.status in [TaskStatus.COMPLETED, TaskStatus.OVERDUE]:
            return APIHelper.send_bad_request_error(
                errorMessageKey='translations.TASK_ALREADY_COMPLETED'
            )

        # current_time = date.today()

        # if task.dueDate:
        #     if current_time <= task.dueDate:
        #         task.status = TaskStatus.COMPLETED
        #     else:
        #         task.status = TaskStatus.OVERDUE
        # else:
        task.status = TaskStatus.COMPLETED

        db.commit()
        db.refresh(task)

        return task