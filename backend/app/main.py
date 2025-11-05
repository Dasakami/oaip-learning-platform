from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from sqladmin import Admin
from app.api import auth, modules, tasks, progress
from app.models.user import User
from app.models.task import Task
from app.models.module import Module

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OAIP Learning Platform", version="1.0.0")
from sqladmin import ModelView
admin = Admin(app, engine, title="My Admin Panel")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(modules.router, prefix="/api/modules", tags=["Modules"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])

class UserAdmin(ModelView, model=User):
    column_list = ["id", "username", "email"]

class TaskAdmin(ModelView, model=Task):
    column_list = ["id", "title", "module_id"]

class ModuleAdmin(ModelView, model=Module):
    column_list = ["id", "name"]

admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
admin.add_view(ModuleAdmin)

@app.get("/")
def root():
    return {"message": "OAIP Learning Platform API"}

@app.get("/health")
def health():
    return {"status": "healthy"}