from fastapi import APIRouter, Depends
from app.basemodel.types import LogoutModel, DeleteModel, ReplaceTasksModel, TasksModel, UpdateModel
from app.basemodel.auth import *
import psycopg2

router = APIRouter()

@router.post("/task")
def upload_task(data: TasksModel = Depends()):
    token = get_data(data)
    token = token[1]
    with psycopg2.connect(DB_ADDRESS) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (user_id, title, about, description, value, members, date, status) VALUES ("
                       "%s, %s, %s, %s, %s, %s, %s, %s)",
                       (int(token), data.title, data.about, data.description,
                        int(data.value), data.members, data.date, data.status))
        conn.commit()
    
    cursor.execute('''
            SELECT * FROM tasks WHERE user_id=%s
        ''',
        (token,)
    )
    
    id = len(cursor.fetchall())
    
    conn.commit()
    cursor.close()
    
    return {
        'id' : id
    }

@router.get("/task")
def get_task(data: LogoutModel = Depends()):
    token = get_data(data)
    token = token[1]
    conn = psycopg2.connect(DB_ADDRESS)
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM tasks WHERE user_id=%s''', (token,))
    data = cursor.fetchall()
    resultado = {'_default': {}}

    for item in data:
        task_id = item[0]
        resultado['_default'][task_id] = {
            'owner': item[1],
            'title': item[2],
            'about': item[3],
            'description': item[4],
            'value': item[5],
            'members': item[6],
            'date': item[7],
            'status': item[8]
        }
    
    conn.commit()
    cursor.close()
    
    return resultado


@router.put("/task")
def update_task(data: UpdateModel = Depends()):
    conn = psycopg2.connect(DB_ADDRESS)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tasks 
        SET title=%s,
            about=%s,
            description=%s,
            value=%s,
            members=%s,
            date=%s,
            status=%s
        WHERE task_id=%s
    ''',
                   (
                       data.title,
                       data.about,
                       data.description,
                       data.value,
                       data.members,
                       data.date,
                       data.status,
                       data.id
                   )
                   )
    conn.commit()
    cursor.close()


@router.delete("/task")
def del_task(data: DeleteModel = Depends()):
    token = get_data(data)
    token = token[1]
    conn = psycopg2.connect(DB_ADDRESS)
    cursor = conn.cursor()
    
    cursor.execute(
        '''
            DELETE FROM tasks WHERE task_id=%s
        ''', (data.id,)
    )
    conn.commit()
    cursor.close()


import json


@router.post("/tasks")
def replace_tasks(data: ReplaceTasksModel = Depends()):
    token = get_data(data)
    token = token[1]
    new_tasks_to_replace = json.loads(data.new_tasks_to_replace)

    conn = psycopg2.connect(DB_ADDRESS)
    cursor = conn.cursor()

    cursor.execute('''
            DELETE FROM tasks WHERE user_id=%s
        ''', (token,)
    )

    conn.commit()

    for task in new_tasks_to_replace:
        try:
            if task['status']:
                pass
        except:
            task['status'] = ''
            
        cursor.execute("INSERT INTO tasks (user_id, title, about, description, value, members, date, status) VALUES ("
                       "%s, %s, %s, %s, %s, %s, %s, %s)",
                       (token, task['title'], task['about'], task['description'],
                        task['value'], task['members'], task['date'], task['status']))
        conn.commit()
        
    cursor.close()