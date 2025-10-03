# TODO LIST应用

```
todo_app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI应用入口
│   ├── config.py              # 配置文件
│   ├── database.py            # 数据库连接
│   ├── models/                # SQLModel 数据模型
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── api/                   # API路由
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── todos.py
│   ├── crud/                  # 数据库操作
│   │   ├── __init__.py
│   │   └── todo.py
│   └── dependencies.py        # 依赖项
├── requirements.txt
└── README.md
```