# ANKIIT ERP - Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** - For running the development environment
- **Node.js 18+** - For frontend development
- **Python 3.11+** - For backend development (optional, Docker handles this)

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd ANKIIT-ERP

# Copy environment configuration
cp config.env.example .env
# Edit .env with your preferred settings
```

### 2. Start Development Environment
```bash
# Start all services with Docker
docker-compose up -d

# Or use the PowerShell script (Windows)
.\start-dev.ps1
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## 🏗️ Architecture Overview

### Backend (FastAPI + PostgreSQL)
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust, scalable database
- **SQLAlchemy**: SQL toolkit and ORM
- **JWT Authentication**: Secure token-based authentication
- **Multi-tenancy**: Support for multiple organizations
- **Role-based Access Control**: Granular permissions system

### Frontend (React + TypeScript)
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **React Query**: Server state management
- **Lucide React**: Beautiful, customizable icons

### Key Features
- ✅ **Authentication System** - Login, registration, JWT tokens
- ✅ **Multi-tenant Architecture** - Support for multiple organizations
- ✅ **Role-based Access Control** - Granular permissions
- ✅ **Modern UI/UX** - Clean, professional design
- ✅ **Responsive Design** - Works on all devices
- ✅ **API Documentation** - Auto-generated with FastAPI

## 📁 Project Structure

```
ANKIIT ERP/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   └── schemas/        # Pydantic schemas
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   └── contexts/       # React contexts
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile.dev      # Frontend container
├── docker-compose.yml      # Development environment
└── README.md               # Project documentation
```

## 🔧 Development

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Database Management
```bash
# Access PostgreSQL
docker exec -it ankiit_erp_postgres psql -U ankiit_user -d ankiit_erp

# View logs
docker-compose logs -f postgres
```

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Update `.env` with production values
2. **Database**: Use managed PostgreSQL service (AWS RDS, etc.)
3. **Redis**: Use managed Redis service (AWS ElastiCache, etc.)
4. **Security**: Update `SECRET_KEY` and enable HTTPS
5. **Monitoring**: Add logging and monitoring services

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 Roadmap

### Phase 1: Foundation ✅
- [x] Project structure setup
- [x] Basic authentication system
- [x] Multi-tenant database design
- [x] Core API endpoints

### Phase 2: Core Modules 🚧
- [ ] User management
- [ ] Organization/tenant management
- [ ] Role-based access control
- [ ] Basic dashboard

### Phase 3: ERP Modules 📅
- [ ] Finance & Accounting
- [ ] HR & Payroll
- [ ] CRM
- [ ] Inventory Management
- [ ] Project Management

### Phase 4: Advanced Features 📅
- [ ] Business Intelligence
- [ ] Reporting & Analytics
- [ ] Workflow automation
- [ ] Mobile app

## 🐛 Troubleshooting

### Common Issues

**Docker services not starting**
```bash
# Check Docker status
docker info

# Restart services
docker-compose down
docker-compose up -d
```

**Database connection issues**
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

**Frontend build issues**
```bash
# Clear node modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Backend import errors**
```bash
# Check Python path
cd backend
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Reinstall dependencies
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Open an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section above

---

**ANKIIT ERP** - Building the future of business management, one module at a time! 🚀
