import React from 'react';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { moduleService, progressService, authService } from '../services/api';
import { BookOpen, CheckCircle, LogOut, TrendingUp } from 'lucide-react';
import '../styles/Dashboard.css';

function Dashboard({ setAuth }) {
  const [modules, setModules] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [modulesRes, statsRes] = await Promise.all([
        moduleService.getAll(),
        progressService.getStats()
      ]);
      setModules(modulesRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setAuth(false);
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>OAIP Learning Platform</h1>
          <button onClick={handleLogout} className="logout-btn">
            <LogOut size={20} /> Logout
          </button>
        </div>
      </header>

      <div className="dashboard-content">
        {stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <BookOpen size={32} />
              <div>
                <h3>{stats.completed_modules}/{stats.total_modules}</h3>
                <p>Modules Completed</p>
              </div>
            </div>
            <div className="stat-card">
              <CheckCircle size={32} />
              <div>
                <h3>{stats.completed_tasks}/{stats.total_tasks}</h3>
                <p>Tasks Completed</p>
              </div>
            </div>
            <div className="stat-card">
              <TrendingUp size={32} />
              <div>
                <h3>{stats.overall_progress.toFixed(1)}%</h3>
                <p>Overall Progress</p>
              </div>
            </div>
          </div>
        )}

        <div className="modules-section">
          <h2>Learning Modules</h2>
          <div className="modules-grid">
            {modules.map((module) => (
              <div 
                key={module.id} 
                className="module-card"
                onClick={() => navigate(`/module/${module.id}`)}
              >
                <div className="module-header">
                  <h3>{module.title}</h3>
                  <span className="module-order">Module {module.order}</span>
                </div>
                <p className="module-description">{module.description}</p>
                <div className="module-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${module.progress_percentage}%` }}
                    ></div>
                  </div>
                  <span className="progress-text">
                    {module.completed_tasks}/{module.total_tasks} tasks completed
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;