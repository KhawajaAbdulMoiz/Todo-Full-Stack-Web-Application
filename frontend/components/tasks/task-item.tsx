'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface TaskItemProps {
  task: Task;
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

export default function TaskItem({ task, onTaskUpdate, onTaskDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [completed, setCompleted] = useState(task.completed);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleCompletion = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.toggleTaskCompletion(task.id);
      setCompleted(response.task.completed);
      onTaskUpdate(response.task);
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Error toggling task completion:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const updateData = {
        title: title.trim(),
        description: description.trim() || null,
        completed,
      };

      const response = await apiClient.updateTask(task.id, updateData);
      onTaskUpdate(response.task);
      setIsEditing(false);
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      setIsLoading(true);
      try {
        await apiClient.deleteTask(task.id);
        onTaskDelete(task.id);
      } catch (err: any) {
        setError(err.message || 'Failed to delete task');
        console.error('Error deleting task:', err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  if (isEditing) {
    return (
      <form onSubmit={handleUpdate} className="border rounded-lg p-4 space-y-4">
        {error && (
          <div className="bg-destructive/15 text-destructive p-2 rounded text-sm">
            {error}
          </div>
        )}
        
        <div className="space-y-2">
          <Label htmlFor={`edit-title-${task.id}`}>Title</Label>
          <Input
            id={`edit-title-${task.id}`}
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor={`edit-description-${task.id}`}>Description</Label>
          <Input
            id={`edit-description-${task.id}`}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Saving...' : 'Save'}
          </Button>
          <Button 
            type="button" 
            variant="outline" 
            onClick={() => {
              setIsEditing(false);
              setTitle(task.title);
              setDescription(task.description || '');
              setCompleted(task.completed);
              setError(null);
            }}
            disabled={isLoading}
          >
            Cancel
          </Button>
        </div>
      </form>
    );
  }

  return (
    <div className={`bg-white rounded-xl p-5 shadow-md border-l-4 ${
      task.completed
        ? 'border-green-500 bg-green-50/30'
        : 'border-blue-500 bg-white'
    } transition-all duration-300 hover:shadow-lg animate-fade-in`}
    style={{ animationDelay: Math.random() * 0.3 + 's' }}>
      {error && (
        <div className="bg-destructive/15 text-destructive p-3 rounded-md mb-3 text-sm">
          {error}
        </div>
      )}

      <div className="flex items-start gap-4">
        <button
          onClick={handleToggleCompletion}
          disabled={isLoading}
          className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center mt-1 transition-colors ${
            task.completed
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-gray-300 hover:border-blue-500'
          }`}
        >
          {task.completed && (
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        <div className="flex-grow min-w-0">
          <h3 className={`font-semibold text-lg truncate ${
            task.completed ? 'line-through text-gray-500' : 'text-gray-900'
          }`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-2 text-gray-600 ${
              task.completed ? 'line-through text-gray-400' : 'text-gray-600'
            }`}>
              {task.description}
            </p>
          )}
          <div className="mt-3 text-xs text-gray-500 flex items-center">
            {task.createdAt && <span>Created: {new Date(task.createdAt).toLocaleDateString()}</span>}
            {task.completed && (
              <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full bg-green-100 text-green-800">
                <svg className="-ml-0.5 mr-1.5 h-2 w-2 text-green-500" fill="currentColor" viewBox="0 0 8 8">
                  <circle cx="4" cy="4" r="3" />
                </svg>
                Completed
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-2 ml-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsEditing(true)}
            disabled={isLoading}
            className="border-gray-300 text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            disabled={isLoading}
            className="text-white bg-red-500 hover:bg-red-600"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}