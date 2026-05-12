export interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
  full_name: string;
}

export interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
  full_name?: string;
  apiError?: string;
}

export interface SignupResponse {
  success: boolean;
  message?: string;
  user?: any;
}