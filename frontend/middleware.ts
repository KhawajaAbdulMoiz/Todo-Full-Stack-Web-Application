import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes that require authentication
export async function middleware(request: NextRequest) {
  // Define public routes that don't require authentication
  const publicRoutes = ['/auth/login', '/auth/register', '/'];

  // Check if the current route is public
  const isPublicRoute = publicRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If it's a public route, allow access
  if (isPublicRoute) {
    return NextResponse.next();
  }

  // For protected routes, check for valid JWT token
  // First check for token in cookies
  let token = request.cookies.get('auth_token')?.value;

  // If not in cookies, check for token in authorization header
  if (!token) {
    const authHeader = request.headers.get('authorization');
    if (authHeader && authHeader.toLowerCase().startsWith('bearer ')) {
      token = authHeader.substring(7); // Remove 'Bearer ' prefix (7 characters)
    }
  }

  // If still no token, try to get it from localStorage by checking for a custom header
  // This is needed when the token is stored in localStorage and sent via a custom header
  if (!token) {
    token = request.headers.get('x-auth-token') || request.headers.get('x-access-token') || undefined;
  }

  if (!token) {
    // No token found, redirect to login
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  try {
    // Verify the JWT token using the secret
    const secret = new TextEncoder().encode(
      process.env.BETTER_AUTH_SECRET || 'fallback_secret_for_dev'
    );

    const { jwtVerify } = await import('jose');
    const verified = await jwtVerify(token, secret);

    // Token is valid, allow access to the requested resource
    return NextResponse.next();
  } catch (error) {
    console.error('Token verification failed:', error);
    // Token is invalid, redirect to login
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }
}

// Specify which routes the middleware should apply to
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};