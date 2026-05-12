import { UUID } from 'crypto';

// Backend API Models
export interface UserBase {
  email: string;
  full_name?: string | null;
  is_active: boolean;
  is_super_user: boolean;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserPublic extends UserBase {
  id: string; // UUID
  created_at: string; // ISO datetime
}

export interface User extends UserPublic {
  hashed_password: string;
}

// API Response types
export interface ApiError {
  detail: string | Record<string, string[]>;
}

export interface ApiResponse<T> {
  data?: T;
  detail?: string;
  count?: number;
}