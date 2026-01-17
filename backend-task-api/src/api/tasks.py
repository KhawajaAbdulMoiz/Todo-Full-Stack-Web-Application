from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from core.database import get_async_session
from core.security import get_current_user
from services.task_service import TaskService
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    return await task_service.get_tasks(current_user.id)


@router.post("/tasks", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    return await task_service.create_task(task_create, current_user.id)


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )
    return task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = await task_service.update_task(task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    success = await task_service.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = await task_service.toggle_task_completion(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not authorized"
        )
    return task