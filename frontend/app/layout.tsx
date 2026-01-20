import './globals.css'
import type { Metadata } from 'next'
import { AuthProvider } from '@/lib/auth'

export const metadata: Metadata = {
  title: 'TaskFlow - Collaborative Task Management',
  description: 'A secure, collaborative todo application for teams',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
<body className="antialiased">
  <AuthProvider>{children}</AuthProvider>
</body>
    </html>
  )
}
