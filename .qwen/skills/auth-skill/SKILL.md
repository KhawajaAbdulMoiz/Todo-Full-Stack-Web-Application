---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate user input (email, password)
   - Hash passwords before storing
   - Prevent duplicate accounts

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Handle invalid login attempts

3. **Password Hashing**
   - Use industry-standard hashing (bcrypt / argon2)
   - Apply salting automatically
   - Never store plain-text passwords

4. **JWT Tokens**
   - Generate access tokens on login
   - Set expiration times
   - Verify tokens on protected routes

5. **Better Auth Integration**
   - Centralize auth logic
   - Support token refresh
   - Simplify session handling

## Best Practices
- Always hash passwords
- Use HTTPS for auth routes
- Short-lived access tokens
- Store secrets in environment variables
- Protect routes with middleware

## Example Structure
```js
// Signup
const hashedPassword = await bcrypt.hash(password, 10);

// Signin
const isValid = await bcrypt.compare(password, user.password);

// JWT
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "1h" }
);
