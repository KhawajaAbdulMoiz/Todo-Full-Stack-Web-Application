# Research Summary: Multi-User Todo Web Application

## Objective
Research and resolve unknowns for implementing a multi-user todo web application with authentication, secure user isolation, and persistent storage.

## 1. Better Auth + FastAPI Integration

### Decision
Implement custom JWT verification middleware in FastAPI to work with Better Auth.

### Rationale
Better Auth handles frontend authentication and token issuance, while FastAPI implements custom verification using the same secret key. This approach maintains the security benefits of JWT while enabling seamless integration between the frontend authentication system and backend API protection.

### Alternatives Considered
- **Session-based authentication**: Would require maintaining session state on the server, complicating scalability and adding complexity to the architecture.
- **Custom auth solution**: Would require building authentication from scratch, increasing development time and potential security vulnerabilities.
- **OAuth-only approach**: Would limit user registration options and add complexity for a simple todo application.

## 2. SQLModel Best Practices for Neon PostgreSQL

### Decision
Use async SQLAlchemy engine with asyncpg driver for optimal Neon performance.

### Rationale
Neon's serverless nature benefits from async operations and connection pooling. The async approach allows better resource utilization and improved performance under load, which aligns with the scalability requirements of the application.

### Alternatives Considered
- **Traditional sync connections**: Would block threads during database operations, reducing efficiency.
- **Other ORMs (SQLAlchemy Core, Peewee)**: Would not provide the same level of integration with FastAPI and type hinting benefits of SQLModel.
- **Raw SQL queries**: Would lose the benefits of ORM abstraction and type safety.

## 3. Next.js 16+ App Router Patterns

### Decision
Implement protected routes using middleware and client-side auth state management.

### Rationale
App Router provides better performance through server components and improved developer experience with file-based routing. Combining server-side middleware for route protection with client-side auth state management offers optimal security and user experience.

### Alternatives Considered
- **Pages router**: Would miss out on the performance and architectural benefits of the newer App Router.
- **Client-side only protection**: Would expose protected routes in the bundle unnecessarily.
- **Server-only protection**: Would require more server round trips and potentially slower navigation.

## 4. JWT Token Management

### Decision
Store JWT tokens in httpOnly cookies for enhanced security, with fallback to localStorage for SPA functionality.

### Rationale
httpOnly cookies prevent XSS attacks by making tokens inaccessible to JavaScript, while still allowing automatic inclusion in API requests. This provides better security than storing tokens in localStorage.

### Alternatives Considered
- **localStorage only**: Vulnerable to XSS attacks that could steal tokens.
- **sessionStorage only**: Would require re-authentication on tab refresh.
- **Memory storage only**: Would require re-authentication on page refresh.

## 5. Database Schema Design

### Decision
Implement a normalized schema with separate User and Task tables, with foreign key relationships and proper indexing.

### Rationale
Normalization reduces data redundancy and maintains consistency. Proper indexing on foreign keys and commonly queried fields ensures optimal query performance as the dataset grows.

### Alternatives Considered
- **Denormalized approach**: Would improve read performance but increase complexity and risk of data inconsistency.
- **Single table with JSON fields**: Would simplify schema but reduce query efficiency and type safety.
- **Document database**: Would not align with the SQLModel constraint and relational nature of user-task relationships.

## 6. API Design Patterns

### Decision
Follow RESTful conventions with proper HTTP methods, status codes, and consistent JSON response structures.

### Rationale
RESTful APIs are well-understood, widely supported, and provide clear patterns for resource manipulation. Consistent response structures improve frontend development experience and error handling.

### Alternatives Considered
- **GraphQL**: Would add complexity for a simple todo application without complex relationships.
- **RPC-style endpoints**: Would not follow standard web conventions and could confuse developers.
- **Custom patterns**: Would require additional documentation and learning curve.

## 7. Frontend State Management

### Decision
Use React Context API combined with useState for authentication state management, with SWR for server state caching.

### Rationale
Context API provides a clean way to share authentication state across components without prop drilling. SWR offers built-in caching, revalidation, and error handling for server state.

### Alternatives Considered
- **Redux Toolkit**: Would add unnecessary complexity for the simple state requirements of this application.
- **Zustand**: Would work well but Context API is sufficient and doesn't require additional dependencies.
- **Recoil**: Would be overkill for the simple state requirements.

## 8. Security Measures

### Decision
Implement multiple layers of security: JWT verification, input validation, rate limiting, and proper error handling.

### Rationale
Defense in depth ensures that if one security measure fails, others provide protection. Input validation prevents injection attacks, rate limiting prevents abuse, and proper error handling avoids information disclosure.

### Alternatives Considered
- **Single security layer**: Would create a single point of failure.
- **Overly complex security**: Would add unnecessary complexity without proportional security gains.
- **Security after MVP**: Would make it harder to add security measures later without refactoring.