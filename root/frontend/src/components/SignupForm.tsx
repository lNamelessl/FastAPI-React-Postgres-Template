import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';
import { UserCreate } from '../types/api';
import { SignupFormData, FormErrors } from '../types/forms';
import { validateSignupForm } from '../utils/validation';
import FormInput from './FormInput';
import Button from './Button';
import FormError from './FormError';
import styles from './SignupForm.module.css';

const SignupForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<SignupFormData>({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Validate form
    const validationErrors = validateSignupForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      const userData: UserCreate = {
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name || undefined,
        is_active: true,
        is_super_user: false,
      };

      const response = await apiService.signup(userData);

      if (response.success) {
        // Redirect to login page
        navigate('/login', { 
          state: { message: 'Signup successful! Please log in.' } 
        });
      } else {
        setErrors({
          apiError: response.message || 'Signup failed. Please try again.',
        });
      }
    } catch (error: any) {
      setErrors({
        apiError: error?.message || 'An unexpected error occurred.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <FormError message={errors.apiError || null} />

      <FormInput
        label="Email"
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        error={errors.email}
        placeholder="you@example.com"
        required
      />

      <FormInput
        label="Password"
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
        error={errors.password}
        placeholder="At least 8 characters"
        required
      />

      <FormInput
        label="Confirm Password"
        type="password"
        name="confirmPassword"
        value={formData.confirmPassword}
        onChange={handleChange}
        error={errors.confirmPassword}
        required
      />

      <FormInput
        label="Full Name"
        type="text"
        name="full_name"
        value={formData.full_name}
        onChange={handleChange}
        error={errors.full_name}
        placeholder="John Doe"
      />

      <Button type="submit" fullWidth loading={loading}>
        Create Account
      </Button>

      <p className={styles.loginLink}>
        Already have an account?{' '}
        <a href="/login">Sign in here</a>
      </p>
    </form>
  );
};

export default SignupForm;