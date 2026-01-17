from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.core.database import get_async_session
from src.core.security import get_current_user
from src.services.task_service import TaskService
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
import uuid


router = APIRouter()


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    task_service = TaskService(session)
    return task_service.get_tasks(current_user.id)


@router.post("/tasks", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    task_service = TaskService(session)
    return task_service.create_task(task_create, current_user.id)


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = task_service.update_task(task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    task_service = TaskService(session)
    success = task_service.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = task_service.toggle_task_completion(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task