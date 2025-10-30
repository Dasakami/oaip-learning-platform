
import React from 'react';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moduleService, taskService } from '../services/api';
import { ArrowLeft, CheckCircle, Circle } from 'lucide-react';
import '../styles/ModuleView.css';

function ModuleView() {
  const { moduleId } = useParams();
  const [module, setModule] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadModule();
  }, [moduleId]);

  const loadModule = async () => {
    try {
      const [moduleRes, tasksRes] = await Promise.all([
        moduleService.getById(moduleId),
        taskService.getModuleTasks(moduleId)
      ]);
      setModule(moduleRes.data);
      setTasks(tasksRes.data);
    } catch (error) {
      console.error('Error loading module:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: '#4CAF50',
      medium: '#FF9800',
      hard: '#F44336'
    };
    return colors[difficulty.toLowerCase()] || '#9E9E9E';
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="module-view">
      <header className="module-header">
        <button onClick={() => navigate('/dashboard')} className="back-btn">
          <ArrowLeft size={20} /> Back to Dashboard
        </button>
      </header>

      <div className="module-content">
        <div className="module-info">
          <h1>{module.title}</h1>
          <p className="module-description">{module.description}</p>
          
          <div className="module-theory">
            <h2>Theory</h2>
            <div className="theory-content" dangerouslySetInnerHTML={{ __html: module.content }} />
          </div>
        </div>

        <div className="tasks-section">
          <h2>Practice Tasks</h2>
          <div className="tasks-list">
            {tasks.map((task) => (
              <div 
                key={task.id}
                className="task-item"
                onClick={() => navigate(`/task/${task.id}`)}
              >
                <div className="task-status">
                  {task.completed ? (
                    <CheckCircle size={24} color="#4CAF50" />
                  ) : (
                    <Circle size={24} color="#9E9E9E" />
                  )}
                </div>
                <div className="task-info">
                  <h3>{task.title}</h3>
                  <p>{task.description}</p>
                  <div className="task-meta">
                    <span 
                      className="difficulty-badge"
                      style={{ backgroundColor: getDifficultyColor(task.difficulty) }}
                    >
                      {task.difficulty}
                    </span>
                    {task.attempts > 0 && (
                      <span className="attempts">Attempts: {task.attempts}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ModuleView;