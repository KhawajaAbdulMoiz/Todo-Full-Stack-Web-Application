# Build Instructions: Frontend & UX Integration

## Overview
This document provides step-by-step instructions to build the frontend application for production deployment on Vercel. Due to disk space limitations during the build process, this document outlines the proper build procedure that should be followed in an environment with sufficient resources.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- At least 2GB free disk space for dependencies and build process
- Git for version control

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to Frontend Directory
```bash
cd frontend  # From project root
```

### 3. Set Up Environment Variables
Create a `.env.production` file with the following variables:

```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL="https://your-backend-api.com/api/v1"

# Better Auth Configuration
BETTER_AUTH_URL="https://your-frontend-domain.com"
BETTER_AUTH_COOKIE_DOMAIN="your-frontend-domain.com"

# Application Configuration
NEXT_PUBLIC_APP_NAME="TaskFlow"
NEXT_PUBLIC_APP_ENV="production"
NEXT_PUBLIC_SERVER_HOST="https://your-frontend-domain.com"
```

## Build Process

### 1. Install Dependencies
```bash
npm install
```

### 2. Clean Previous Builds (if any)
```bash
rm -rf .next  # On Windows: rmdir /s /q .next
```

### 3. Run Production Build
```bash
npm run build
```

## Expected Build Output

Upon successful build, you should see:

```text
> frontend@0.1.0 build
> next build

Attention: Next.js now collects completely anonymous telemetry regarding usage.
This information is used to shape Next.js's roadmap and prioritize features.
You can learn more, including how to opt-out if you'd like to at: https://nextjs.org/telemetry

Creating an optimized production build...

✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (0/XX)
✓ Building analysis output
✓ Finalizing page optimization

Route (app)                              Size     First Load JS
┌ ○ /                                    1.23 kB        80.45 kB
├ ○ /auth/login                          2.34 kB        85.67 kB
├ ○ /auth/register                       2.45 kB        86.78 kB
├ ● /dashboard                           3.56 kB        92.89 kB
└ λ /api/auth/[...nextauth]              0.12 kB        75.34 kB
+ First Load JS shared by all             75.23 kB

○  (Static)     prerendered as static content
●  (SSG)        prerendered as static content and is rerendered at runtime
λ  (Dynamic)    server-rendered on demand at runtime
```

## Vercel Deployment

### 1. Using Vercel CLI
```bash
npm install -g vercel
vercel login
vercel
```

### 2. Using GitHub Integration
1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. Add the required environment variables in the Vercel dashboard
4. Deploy automatically on push to main branch

### 3. Build Command for Vercel
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

## Required Environment Variables for Vercel

### Build-time Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `NEXT_PUBLIC_APP_NAME`: Application name
- `NEXT_PUBLIC_APP_ENV`: Set to "production"

### Runtime Variables
- `BETTER_AUTH_SECRET`: Strong, randomly generated JWT secret
- `BETTER_AUTH_URL`: Frontend URL where the app is deployed

## Troubleshooting Common Build Issues

### 1. Disk Space Issues
- **Problem**: `ENOSPC: no space left on device`
- **Solution**: Ensure at least 2GB free space before building

### 2. Memory Issues
- **Problem**: `JavaScript heap out of memory`
- **Solution**: Increase Node.js memory limit:
  ```bash
  NODE_OPTIONS="--max-old-space-size=4096" npm run build
  ```

### 3. Dependency Conflicts
- **Problem**: Peer dependency warnings/errors
- **Solution**: Use exact versions specified in package.json or update dependencies to compatible versions

### 4. TypeScript Issues
- **Problem**: Type errors during build
- **Solution**: Run `npm run type-check` to identify and fix type issues

### 5. Environment Variable Issues
- **Problem**: Missing environment variables during build
- **Solution**: Ensure all NEXT_PUBLIC_* variables are set during build time

## Post-Build Verification

### 1. Start Production Server
```bash
npm start
```

### 2. Verify Functionality
- Access the homepage at http://localhost:3000
- Test authentication flows (login, register)
- Verify task management functionality
- Check responsive design on different screen sizes
- Confirm JWT token handling works properly

## Deployment Checklist

- [ ] All NEXT_PUBLIC_* environment variables are properly configured
- [ ] Better Auth is properly configured with production URLs
- [ ] API endpoints are accessible from production environment
- [ ] Authentication redirects work correctly
- [ ] Task management functionality works end-to-end
- [ ] Responsive design verified on multiple screen sizes
- [ ] Error handling displays appropriate messages
- [ ] Performance is acceptable (pages load under 3 seconds)

## Notes

- The build process may take 5-10 minutes depending on system resources
- Ensure the backend API is running and accessible before deploying the frontend
- Monitor the application after deployment to verify all functionality works as expected
- Set up proper logging and monitoring for the production application