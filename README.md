# ANKIIT ERP - Full Stack ERP SaaS Platform

A modern, scalable ERP system built with React, FastAPI, and PostgreSQL.

## 🚀 Features

- **Multi-tenant SaaS architecture**
- **Modular ERP modules** (Finance, HR, CRM, Inventory, etc.)
- **Modern React frontend** with TypeScript
- **FastAPI backend** with automatic API documentation
- **PostgreSQL database** with multi-tenancy support
- **JWT authentication** and role-based access control
- **Responsive design** with Tailwind CSS
- **Docker deployment** ready

## 🏗️ Architecture

```
ANKIIT ERP/
├── frontend/          # React + TypeScript frontend
├── backend/           # FastAPI Python backend
├── database/          # Database migrations and schemas
├── docker/            # Docker configuration
├── docs/              # API documentation
└── scripts/           # Development and deployment scripts
```

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Tailwind CSS, React Router
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy, Alembic
- **Database**: PostgreSQL 15+
- **Authentication**: JWT, OAuth2
- **Deployment**: Docker, Docker Compose
- **Testing**: Pytest, Jest, React Testing Library

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+

### Development Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd ANKIIT-ERP
   ```

2. **Start with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Or setup manually**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload

   # Frontend
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📋 Development Roadmap

### Phase 1: Foundation ✅
- [x] Project structure setup
- [x] Basic authentication system
- [x] Multi-tenant database design
- [x] Core API endpoints
- [x] Finance Module (Core ERP functionality)

### Phase 2: Core Modules 🚧
- [x] User management
- [x] Organization/tenant management
- [x] Role-based access control
- [x] Basic dashboard

### Phase 3: ERP Modules 📅
- [x] Finance & Accounting (Complete with Chart of Accounts, Transactions, Invoices, Payments)
- [ ] HR & Payroll
- [ ] CRM
- [ ] Inventory Management
- [ ] Project Management

### Phase 4: Advanced Features 📅
- [ ] Business Intelligence
- [ ] Reporting & Analytics
- [ ] Workflow automation
- [ ] Mobile app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.
