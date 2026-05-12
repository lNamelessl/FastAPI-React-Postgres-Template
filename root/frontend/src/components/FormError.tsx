import React from 'react';
import styles from './FormError.module.css';

interface FormErrorProps {
  message: string | null;
}

const FormError: React.FC<FormErrorProps> = ({ message }) => {
  if (!message) return null;

  return (
    <div className={styles.container}>
      <span className={styles.icon}>⚠</span>
      <p className={styles.message}>{message}</p>
    </div>
  );
};

export default FormError;