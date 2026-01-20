'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';

interface TaskToggleProps {
  task: Task;
  onTaskUpdate: (task: Task) => void;
}

export default function TaskToggle({ task, onTaskUpdate }: TaskToggleProps) {
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggle = async () => {
    setIsUpdating(true);
    setError(null);

    try {
      const response = await apiClient.toggleTaskCompletion(task.id);
      onTaskUpdate(response);
    } catch (err: any) {
      setError(err.message || 'Failed to update task status');
      console.error('Error toggling task:', err);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={handleToggle}
        disabled={isUpdating}
        className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
      />
      <span className={task.completed ? 'line-through text-gray-500' : ''}>
        {task.title}
      </span>
      {error && (
        <span className="text-red-500 text-sm">{error}</span>
      )}
    </div>
  );
}