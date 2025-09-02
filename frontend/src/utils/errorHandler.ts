export function getErrorMessage(error: any): string {
  if (typeof error === 'string') {
    return error;
  }
  
  if (error?.message) {
    // Handle common API error patterns
    const message = error.message.toLowerCase();
    
    // Network errors
    if (message.includes('fetch') || message.includes('network') || message.includes('failed to fetch')) {
      return 'Network error. Please check your connection and try again.';
    }
    
    // Authentication errors
    if (message.includes('401') || message.includes('unauthorized')) {
      return 'Please log in to continue.';
    }
    
    // Login specific errors
    if (message.includes('invalid credentials') || message.includes('incorrect password') || message.includes('wrong password')) {
      return 'Invalid email or password. Please try again.';
    }
    
    if (message.includes('user not found') || message.includes('email not found') || message.includes('account not found')) {
      return 'No account found with this email address. Please check your email or create a new account.';
    }
    
    if (message.includes('account locked') || message.includes('account disabled')) {
      return 'Your account has been locked. Please contact support for assistance.';
    }
    
    if (message.includes('too many attempts') || message.includes('rate limit')) {
      return 'Too many login attempts. Please wait a few minutes before trying again.';
    }
    
    // Validation errors
    if (message.includes('422') || message.includes('validation')) {
      return 'Please check your input and try again.';
    }
    
    // Server errors
    if (message.includes('500') || message.includes('server') || message.includes('internal server error')) {
      return 'Server error. Please try again later.';
    }
    
    // Stock errors
    if (message.includes('stock') || message.includes('insufficient')) {
      return 'Sorry, this item is out of stock or you requested more than available.';
    }
    
    // Product not found
    if (message.includes('404') || message.includes('not found')) {
      return 'Product not found.';
    }
    
    return error.message;
  }
  
  return 'An unexpected error occurred. Please try again.';
}
