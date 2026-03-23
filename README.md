# Smart Academic Agent

面向就业能力提升的智慧教务系统与智能体平台骨架。

最新进度记录见 [docs/当前开发进度.md](docs/当前开发进度.md)。
详细运行与部署说明见 [docs/运行部署说明.md](docs/运行部署说明.md)。

## 演示账号

- 学生：`student1 / 123456`
- 管理员：`admin1 / 123456`

## 目录结构

```text
frontend/   Vue 3 + Vite + TypeScript 前端
backend/    FastAPI 后端服务
sql/        数据库脚本
docs/       补充设计文档
```

## 快速启动

### 1. 初始化数据库

```powershell
mysql -u root -p < sql\schema.sql
```

默认数据库名为 `smart_academic_system`。如需调整，请同步修改 `backend/.env`。

### 2. 启动后端

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

后端默认地址：`http://127.0.0.1:8000`

### 3. 导入演示数据

```powershell
cd backend
.\.venv\Scripts\activate
$env:PYTHONPATH='.'
python scripts\seed_demo_data.py
```

### 4. 启动前端

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

## 生产构建

### 前端

```powershell
cd frontend
npm run build
```

### 后端

```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 环境变量

### 后端

参考 [backend/.env.example](backend/.env.example)：

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `JWT_SECRET_KEY`

### 前端

参考 [frontend/.env.example](frontend/.env.example)：

- `VITE_API_BASE_URL`：后端 API 根地址，默认 `http://127.0.0.1:8000/api/v1`

## 当前已实现模块

- 登录认证与权限
- 学生首页
- 成绩查询
- 课表查询
- 培养方案查询
- 学业预警
- 教务智能问答
- 微专业推荐
- 知识库管理
- 管理员统计、预警规则、预警记录
