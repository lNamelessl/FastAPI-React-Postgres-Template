import React from 'react';
import SignupForm from '../components/SignupForm';
import styles from './SignupPage.module.css';

const SignupPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          <h1>Create Account</h1>
          <p>Join us and get started</p>
        </div>
        <SignupForm />
      </div>
    </div>
  );
};

export default SignupPage;