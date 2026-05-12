import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import styles from './LoginPage.module.css';

const LoginPage: React.FC = () => {
  const location = useLocation();
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const state = location.state as any;
    if (state?.message) {
      setMessage(state.message);
    }
  }, [location]);

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          <h1>Sign In</h1>
          <p>Welcome back</p>
        </div>

        {message && <div className={styles.successMessage}>{message}</div>}

        <div className={styles.placeholder}>
          <p>Login form coming soon...</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;