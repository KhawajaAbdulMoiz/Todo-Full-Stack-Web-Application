---
name: backend-core
description: Design backend systems by generating routes, handling requests/responses, and connecting to databases.
---

# Backend Core Development Skill

## Instructions

1. **Routing**
   - Define RESTful routes (GET, POST, PUT, DELETE)
   - Use clear and meaningful endpoint names
   - Group routes by resource/module

2. **Request & Response Handling**
   - Parse request parameters, body, and headers
   - Validate incoming data
   - Send structured JSON responses
   - Handle success and error responses properly

3. **Database Integration**
   - Connect backend to a database (SQL or NoSQL)
   - Perform CRUD operations
   - Use environment variables for credentials
   - Handle connection errors safely

4. **Middleware Usage**
   - Authentication & authorization
   - Logging and request tracking
   - Error handling middleware

## Best Practices
- Follow REST API standards
- Keep controllers thin and reusable
- Use proper HTTP status codes
- Secure sensitive data (tokens, passwords)
- Separate routes, controllers, and database logic
- Write scalable and readable code

## Example Structure

```js
// routes/userRoutes.js
import express from "express";
import { getUsers, createUser } from "../controllers/userController.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
