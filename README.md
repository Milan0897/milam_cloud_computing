# Student Document Management System

A full-stack web application for students to securely manage their academic documents (marksheets, admin cards, registration certificates, etc.) using AWS S3 for storage.

## Features

- **Authentication**: Secure JWT-based register/login
- **Document Management**: Upload, view, delete documents
- **Categories**: Marksheet, Admin Card, Registration Certificate, ID Proof, Other
- **File Support**: PDF, JPEG, PNG, WebP (max 10MB)
- **Private Storage**: Each student only accesses their own documents
- **AWS S3 Integration**: Presigned URLs for secure uploads/downloads
- **Responsive UI**: Works on desktop and mobile

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + Vite |
| Backend | Node.js + Express |
| Database | PostgreSQL (Prisma ORM) |
| Storage | AWS S3 |
| Auth | JWT + bcrypt |
| Deployment | Docker + Docker Compose |

## Project Structure

```
student-doc-system/
├── backend/
│   ├── prisma/
│   │   └── schema.prisma
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── nginx.conf
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.production.example
└── AWS_SETUP_GUIDE.md
```

## Quick Start (Development)

### Prerequisites
- Node.js 18+
- PostgreSQL 15+
- AWS Account (for S3)

### Backend Setup
```bash
cd backend
cp .env.example .env
# Edit .env with your values
npm install
npx prisma generate
npx prisma migrate dev
npm run dev
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Production Deployment

See [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md) for complete AWS EC2 + S3 deployment instructions.

### Quick Deploy with Docker
```bash
cp .env.production.example .env.production
# Edit .env.production with production values
docker compose -f docker-compose.yml --env-file .env.production up -d --build
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get current user profile

### Documents
- `GET /api/documents` - List user's documents (query: category)
- `GET /api/documents/categories` - Get category options
- `GET /api/documents/presigned-upload` - Get presigned upload URL
- `GET /api/documents/:id` - Get document with view URL
- `POST /api/documents` - Upload document (multipart/form-data)
- `DELETE /api/documents/:id` - Delete document

## Environment Variables

### Backend
| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| JWT_SECRET | Secret for JWT signing (64+ chars) | Yes |
| JWT_EXPIRES_IN | Token expiry (default: 7d) | No |
| PORT | Server port (default: 5000) | No |
| NODE_ENV | Environment (development/production) | No |
| FRONTEND_URL | Frontend origin for CORS | Yes |
| AWS_REGION | AWS region | Yes |
| AWS_ACCESS_KEY_ID | AWS access key | Yes |
| AWS_SECRET_ACCESS_KEY | AWS secret key | Yes |
| AWS_S3_BUCKET | S3 bucket name | Yes |

## Security Features

- Passwords hashed with bcrypt (cost: 12)
- JWT tokens with 7-day expiry
- S3 access via presigned URLs (no public access)
- User isolation (documents scoped to userId)
- CORS configured for specific origin
- Helmet-ready (add helmet middleware for production)

## License

MIT