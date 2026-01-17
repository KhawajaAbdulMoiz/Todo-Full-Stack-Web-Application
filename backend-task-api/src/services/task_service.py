from sqlmodel import select
from typing import List, Optional
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
        task = Task(
            **task_create.dict(),
            user_id=user_id
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_tasks(self, user_id: uuid.UUID) -> List[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def update_task(self, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
        task = await self.get_task(task_id, user_id)
        if not task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        task = await self.get_task(task_id, user_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def toggle_task_completion(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        task = await self.get_task(task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task