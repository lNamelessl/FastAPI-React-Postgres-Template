import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import styles from './App.module.css';

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <div className={styles.app}>
          <Routes>
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Navigate to="/signup" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
};

export default App;