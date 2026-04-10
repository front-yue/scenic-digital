# 智慧文旅数字导览系统 (Scenic Digital Board)

[![Vue 3](https://img.shields.io/badge/Vue.js-3.0-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-Next-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Flask](https://img.shields.io/badge/Flask-Python-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)

智慧文旅数字导览系统是一个基于 **Vue 3 + Flask + MySQL** 构建的现代化、科幻风格的大屏展示与管理平台。该项目最初作为 Fay 数字人的 IoT 中控模拟系统，现已全面重构升级为**专注于景区全景概览、实时客流监控、景点管理以及与 Fay 数字人交互**的综合性解决方案。

非常适合用于：**企业展厅展示、景区游客中心大屏、政府数字化投标演示**以及**全栈开发学习参考**。

---

## 🔥 核心特性

- 🎨 **极致的科幻 UI 设计**
  - 采用 Tailwind CSS v4 构建深色科幻风格（Cyberpunk/Tech风格）。
  - 包含复杂的 CSS 几何裁剪（Clip-path）、3D 翻转、粒子特效与光晕发光渲染。
- 📊 **实时客流与舒适度计算**
  - 后端动态基于各景点实时在园人数与最大承载量计算拥挤度（畅通/适中/拥挤）。
  - 前端大屏实时联动呈现各景点的状态变化。
- 🤖 **无缝集成 Fay 数字人**
  - 预留数字人 3D Avatar 展位，作为大屏的视觉中心。
  - 支持通过 API 直接唤起/关闭 Fay 核心服务，并管理麦克风/音频硬件状态。
- ⚙️ **所见即所得的数据管理后台**
  - 内置科幻风格的 `AdminOverlay` 弹窗。
  - 支持一键修改景区全局基础信息（名称、介绍、票价、营业时间）。
  - 支持景点列表的完整 CRUD（增删改查），修改后大屏数据即刻热更新。
- 🏗 **标准化的全栈架构**
  - **前端**：Vue 3 Composition API, Axios 拦截器封装, 多环境变量支持。
  - **后端**：Python Flask 分层架构（Routes -> Services -> DB Utils），遵循 RESTful API 设计规范。

---

## 🛠 技术栈

### 前端 (Frontend)
- **核心框架**: Vue 3
- **构建工具**: Vite
- **样式方案**: Tailwind CSS v4
- **网络请求**: Axios
- **图标库**: Lucide Vue Next

### 后端 (Backend)
- **核心框架**: Python Flask
- **架构模式**: 蓝图 (Blueprints) 路由分发 + Service 业务逻辑层
- **跨域处理**: Flask-CORS
- **数据库驱动**: PyMySQL

### 数据库 (Database)
- **MySQL 8.0+** (提供完整的建表与测试数据 SQL 脚本)

---

## 🚀 快速开始

### 1. 数据库准备
1. 确保已安装并运行 MySQL 服务。
2. 创建数据库并导入初始化脚本：
   ```bash
   mysql -u root -p < database/scenic_init.sql
   ```
3. 默认将创建 `scenic` 数据库，并包含 `scenic_info`、`scenic_spots` 和 `scenic_flow` 三张表及测试数据。

### 2. 后端服务启动 (Flask)
1. 进入 `backend` 目录：
   ```bash
   cd backend
   ```
2. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置数据库连接：
   修改 `backend/config.py` 中的 `SQLALCHEMY_DATABASE_URI` 或对应的 MySQL 账号密码。
4. 启动服务 (默认端口 8888)：
   ```bash
   python run.py
   ```

### 3. 前端大屏启动 (Vue 3)
1. 返回项目根目录，安装 Node 依赖：
   ```bash
   npm install
   ```
2. 配置环境变量：
   复制 `.env.example` 为 `.env`，确保配置了正确的后端地址：
3. 启动 Vite 开发服务器：
   ```bash
   npm run dev
   ```

---

## � 核心目录结构

```text
├── backend/                   # Python Flask 后端目录
│   ├── app/
│   │   ├── routes/            # 路由层 (API 接口定义)
│   │   ├── services/          # 业务逻辑层 (CRUD 及客流计算)
│   │   ├── utils/             # 工具类 (数据库连接、统一响应封装)
│   │   └── __init__.py        # Flask App 工厂与蓝图注册
│   ├── config.py              # 后端环境配置
│   ├── requirements.txt       # Python 依赖
│   └── run.py                 # 后端启动入口
├── database/                  # 数据库目录
│   └── scenic_init.sql        # MySQL 初始化脚本 (包含建表与 Mock 数据)
├── src/                       # Vue 3 前端源码
│   ├── api/                   # Axios 请求封装 (scenic.js, fay.js)
│   ├── components/            # Vue 组件
│   │   └── admin/
│   │       └── AdminOverlay.vue # 系统数据管理控制台弹窗
│   ├── pages/                 # 页面级组件
│   │   └── ScenicScreen.vue   # 智慧文旅大屏主页面
│   ├── utils/                 # 前端工具类 (request 实例分发)
│   ├── App.vue                # 根组件
│   └── main.js                # Vue 挂载入口
├── .env.example               # 环境变量示例
├── package.json               # NPM 依赖与脚本
├── tailwind.config.js         # Tailwind 配置
└── vite.config.js             # Vite 配置
```

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request 来完善这个项目！
如果是重大变更，请先开一个 Issue 讨论您想要改变的内容。

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议 - 详情请查看 LICENSE 文件。
