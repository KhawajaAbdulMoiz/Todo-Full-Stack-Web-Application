import { z } from 'zod';

// User-related types
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type User = z.infer<typeof UserSchema>;

// Task-related types
export const TaskSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1, 'Title is required').max(255),
  description: z.string().optional().nullable(),
  completed: z.boolean().default(false),
  user_id: z.string().uuid(),  
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),  
});

export type Task = z.infer<typeof TaskSchema>;

export const CreateTaskSchema = TaskSchema.omit({ 
  id: true, 
  user_id: true, 
  created_at: true, 
  updated_at: true 
});

export type CreateTask = z.infer<typeof CreateTaskSchema>;

export const UpdateTaskSchema = TaskSchema.partial().omit({ 
  id: true, 
  user_id: true, 
  created_at: true, 
  updated_at: true 
});

export type UpdateTask = z.infer<typeof UpdateTaskSchema>;