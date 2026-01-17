---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations using best practices.
---

# Database Schema Design

## Instructions

1. **Schema planning**
   - Identify entities and relationships
   - Define primary keys and foreign keys
   - Normalize data (avoid redundancy)

2. **Table creation**
   - Use appropriate data types
   - Apply constraints (NOT NULL, UNIQUE, CHECK)
   - Define indexes for performance

3. **Migrations**
   - Version-controlled schema changes
   - Forward and rollback migrations
   - Safe schema evolution without data loss

4. **Relationships**
   - One-to-one
   - One-to-many
   - Many-to-many (junction tables)

## Best Practices
- Use meaningful table and column names
- Prefer integers or UUIDs for primary keys
- Always define foreign key constraints
- Avoid over-normalization
- Add indexes only where needed
- Keep migrations small and reversible
- Never edit old migrations in production

## Example Structure

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
