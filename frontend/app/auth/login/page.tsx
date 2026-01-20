'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import LoginForm from '@/components/auth/login-form';

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { isAuthenticated, isLoading: authIsLoading } = useAuth();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
      router.refresh(); // Refresh to ensure the UI updates properly
    }
  }, [isAuthenticated, router]);

  const handleLoginSuccess = () => {
    // Redirect to dashboard after successful login
    router.push('/dashboard');
    router.refresh(); // Refresh to ensure the UI updates properly
  };

  if (isAuthenticated) {
    return null; // Return nothing while redirecting
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-600 mt-2">Sign in to your account to continue</p>
        </div>

        {error && (
          <div className="bg-destructive/15 text-destructive p-3 rounded-md mb-4 text-center">
            {error}
          </div>
        )}

        <LoginForm />

        <div className="mt-6 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/auth/register" className="font-medium text-indigo-600 hover:text-indigo-500">
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}