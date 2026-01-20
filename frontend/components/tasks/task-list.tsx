'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { Task } from '@/lib/types';
import TaskItem from '@/components/tasks/task-item';
import TaskForm from '@/components/tasks/task-form';

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // Fetch tasks for the user
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const tasksData = await apiClient.getTasks();

        // Transform backend response to match frontend types
        const formattedTasks = (Array.isArray(tasksData) ? tasksData : []).map(task => ({
          id: String(task.id),
          title: task.title,
          description: task.description || '',
          completed: task.completed || false,
          user_id: task.user_id,
          created_at: task.created_at,
          updated_at: task.updated_at,
        }));

        console.log('Tasks loaded:', formattedTasks.length);
        setTasks(formattedTasks);

      } catch (err: any) {
        setError(err.message || 'Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId]);

  // Handler for when a task is updated
  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(prevTasks =>
      prevTasks.map(task => (task.id === updatedTask.id ? updatedTask : task))
    );
  };

  // Handler for when a task is deleted
  const handleTaskDelete = (taskId: string) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
  };

  // Handler for when a new task is created
  const handleTaskCreate = (newTask: Task) => {
    setTasks(prevTasks => [...prevTasks, newTask]);
  };

  // Filter tasks based on selection
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all'
  });

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading your tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-destructive/15 text-destructive p-6 rounded-xl max-w-md mx-auto">
        <h3 className="font-medium">Error Loading Tasks</h3>
        <p className="mt-1 text-sm">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 text-sm text-destructive underline hover:no-underline"
        >
          Reload page
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-1 shadow-lg">
        <div className="bg-white rounded-xl p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Create New Task</h2>
          <TaskForm onTaskCreate={handleTaskCreate} />
        </div>
      </div>

      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Your Tasks</h2>
        <div className="flex space-x-2 bg-gray-100 p-1 rounded-lg">
          <button
            className={`px-3 py-1 rounded-md text-sm font-medium ${filter === 'all'
              ? 'bg-white text-blue-600 shadow'
              : 'text-gray-600 hover:text-gray-900'
              }`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            className={`px-3 py-1 rounded-md text-sm font-medium ${filter === 'active'
              ? 'bg-white text-blue-600 shadow'
              : 'text-gray-600 hover:text-gray-900'
              }`}
            onClick={() => setFilter('active')}
          >
            Active
          </button>
          <button
            className={`px-3 py-1 rounded-md text-sm font-medium ${filter === 'completed'
              ? 'bg-white text-blue-600 shadow'
              : 'text-gray-600 hover:text-gray-900'
              }`}
            onClick={() => setFilter('completed')}
          >
            Completed
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
            <div className="mx-auto h-12 w-12 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks</h3>
            <p className="mt-1 text-gray-500">
              {filter === 'completed'
                ? "You haven't completed any tasks yet."
                : filter === 'active'
                  ? "You have no active tasks. Add one above!"
                  : "Get started by adding a new task."}
            </p>
          </div>
        ) : (
          filteredTasks.filter(t => t?.id).map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdate={handleTaskUpdate}
              onTaskDelete={handleTaskDelete}
            />
          ))
        )}
      </div>

      {tasks.length > 0 && (
        <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 text-center text-gray-600 border border-white/30">
          You have <span className="font-semibold text-blue-600">{tasks.length}</span> total tasks,
          <span className="font-semibold text-green-600"> {tasks.filter(t => t?.completed === true).length} </span> completed
        </div>
      )}
    </div>
  );
}