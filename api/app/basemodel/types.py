from pydantic import BaseModel


class LogoutModel(BaseModel):
    access_token: str


class TasksModel(BaseModel):
    access_token: str
    title: str
    about: str = ''
    description: str
    date: str = ''
    members: str = ''
    value: int = 0
    status: str = 'pending'


class DeleteModel(BaseModel):
    access_token: str
    id: int


class UpdateModel(BaseModel):
    access_token: str
    id: int
    title: str
    about: str = ''
    description: str
    date: str = ''
    members: str = ''
    value: int = 0
    status: str = ''


class ReplaceTasksModel(BaseModel):
    access_token: str
    new_tasks_to_replace: str