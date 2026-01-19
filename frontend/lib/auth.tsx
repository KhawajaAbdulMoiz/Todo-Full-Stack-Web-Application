'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

// -------------------- Types --------------------
interface User {
  id: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// -------------------- Auth Provider --------------------
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Restore user and token from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('logged_in_user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('logged_in_user');
      }
    }

    // Listen for storage changes to sync across tabs
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'logged_in_user') {
        if (e.newValue) {
          try {
            setUser(JSON.parse(e.newValue));
          } catch {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  // -------------------- Login --------------------
const login = async (email: string, password: string) => {
  setIsLoading(true);

  try {
    const baseUrl =
      process.env.NEXT_PUBLIC_API_BASE_URL ??
      'http://localhost:8000/api/v1';

    const response = await fetch(`${baseUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data?.detail || data?.message || 'Login failed');
    }

    // ✅ YOUR backend returns token here
const token = data?.data?.token ?? data?.token;
const user = data?.data?.user ?? data?.user;

    if (!token || !user) {
      throw new Error('Invalid login response from server');
    }

    localStorage.setItem('auth_token', token);
    localStorage.setItem('logged_in_user', JSON.stringify(user));

    setUser(user);
  } catch (err: any) {
    console.error('Login error:', err);
    throw new Error(err?.message || 'Login failed');
  } finally {
    setIsLoading(false);
  }
};


  // -------------------- Register --------------------
  const register = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const baseUrl =
        process.env.NEXT_PUBLIC_API_BASE_URL ||
        process.env.API_BASE_URL ||
        'http://localhost:8000/api/v1';

      const response = await fetch(`${baseUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Registration failed');
      }

      // Extract token from response following canonical contract: response.data.token
      const token = data?.data?.token;
      const user = data?.data?.user;

      if (!token || !user) {
        throw new Error('Invalid registration response from server');
      }

      // Store the token in localStorage (same as apiClient does)
      localStorage.setItem('auth_token', token);

      const normalizedUser: User = {
        id: user.id,
        email: user.email,
        createdAt: user.created_at || user.createdAt,
        updatedAt: user.updated_at || user.updatedAt,
      };

      setUser(normalizedUser);
      localStorage.setItem('logged_in_user', JSON.stringify(normalizedUser));
    } catch (err: any) {
      console.error('Registration error:', err);

      let message = 'Registration failed';

      if (typeof err === 'string') {
        message = err;
      } else if (err instanceof Error) {
        message = err.message;
      } else if (err?.detail) {
        message = err.detail;
      } else if (err?.message && typeof err.message === 'string') {
        message = err.message;
      } else {
        message = JSON.stringify(err);
      }

      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  };


  const logout = () => {
    setUser(null);
    localStorage.removeItem('logged_in_user');
    localStorage.removeItem('auth_token'); // Also remove the auth token
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};


export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
