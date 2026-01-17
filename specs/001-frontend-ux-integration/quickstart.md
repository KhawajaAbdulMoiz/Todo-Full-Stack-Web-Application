# Quickstart Guide: Frontend & UX Integration

## Overview
This guide provides step-by-step instructions to set up and run the frontend application locally. The application connects to the backend API built in Spec 2 and implements authentication using Better Auth with JWT tokens.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Backend API from Spec 2 running (port 8000)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Environment Variables
Create a `.env.local` file in the frontend directory with the following variables:

```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api/v1"

# Better Auth Configuration
BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_COOKIE_DOMAIN="localhost"

# Application Configuration
NEXT_PUBLIC_APP_NAME="TaskFlow"
NEXT_PUBLIC_APP_ENV="development"
NEXT_PUBLIC_SERVER_HOST="http://localhost:3000"
```

For production, ensure you use strong, randomly generated secrets for authentication.

## Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend  # From project root
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Running the Application

### 1. Start Backend First
Ensure the backend API from Spec 2 is running at `http://localhost:8000`.

### 2. Start Frontend
Start the frontend at `http://localhost:3000`.

### 3. Access the Application
Open your browser and navigate to `http://localhost:3000`.

## Key Features Walkthrough

### 1. User Authentication
- Navigate to `/auth/login` or `/auth/signup`
- Enter your credentials
- JWT token will be stored securely and attached to all API requests

### 2. Task Management Dashboard
- After authentication, access the dashboard at `/dashboard`
- Create, read, update, and delete tasks
- Toggle task completion status with a simple click

### 3. Responsive UI
- The application adapts to different screen sizes
- Mobile-friendly interface for on-the-go task management

## Development Commands

### Frontend Commands
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Format code
npm run format
```

## Testing the Application

### 1. Unit Tests
Run frontend unit tests:
```bash
cd frontend
npm run test
```

### 2. Integration Tests
Test the integration between components:
```bash
cd frontend
npm run test:integration
```

### 3. End-to-End Tests
Test complete user workflows:
```bash
cd frontend
npm run test:e2e
```

## Production Deployment

### Building for Production
```bash
# Frontend
cd frontend
npm run build
```

### Environment Variables for Production
Ensure these variables are set in your production environment:
- `NEXT_PUBLIC_API_BASE_URL` (production backend API URL)
- `BETTER_AUTH_URL` (production frontend URL)
- `APP_ENV=production`
- `BETTER_AUTH_SECRET` (strong, randomly generated)