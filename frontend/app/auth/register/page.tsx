'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import RegisterForm from '@/components/auth/register-form';

export default function RegisterPage() {
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleRegisterSuccess = () => {
    // Redirect to dashboard after successful registration
    router.push('/dashboard');
    router.refresh(); // Refresh to update UI based on auth state
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-600 mt-2">Join us to manage your tasks efficiently</p>
        </div>
        
        {error && (
          <div className="bg-destructive/15 text-destructive p-3 rounded-md mb-4 text-center">
            {error}
          </div>
        )}
        
        <RegisterForm onRegisterSuccess={handleRegisterSuccess} />
        
        <div className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <a href="/auth/login" className="font-medium text-indigo-600 hover:text-indigo-500">
            Sign in
          </a>
        </div>
      </div>
    </div>
  );
}