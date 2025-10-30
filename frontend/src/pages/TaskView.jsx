import React from 'react';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { taskService } from '../services/api';
import Editor from '@monaco-editor/react';
import { ArrowLeft, Play, CheckCircle, XCircle } from 'lucide-react';
import '../styles/TaskView.css';

function TaskView() {
  const { taskId } = useParams();
  const [task, setTask] = useState(null);
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadTask();
  }, [taskId]);

  const loadTask = async () => {
    try {
      const response = await taskService.getById(taskId);
      setTask(response.data);
      setCode(response.data.starter_code || '# Write your code here\n');
    } catch (error) {
      console.error('Error loading task:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setResult(null);

    try {
      const response = await taskService.submitCode({
        task_id: parseInt(taskId),
        code: code
      });
      setResult(response.data);
      
      if (response.data.success) {
        setTimeout(() => loadTask(), 1000);
      }
    } catch (error) {
      console.error('Error submitting code:', error);
      setResult({
        success: false,
        message: 'Submission failed',
        test_results: []
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="task-view">
      <header className="task-header">
        <button onClick={() => navigate(`/module/${task.module_id}`)} className="back-btn">
          <ArrowLeft size={20} /> Back to Module
        </button>
        {task.completed && <span className="completed-badge">✓ Completed</span>}
      </header>

      <div className="task-container">
        <div className="task-description">
          <h1>{task.title}</h1>
          <div className="task-meta">
            <span className="difficulty">{task.difficulty}</span>
            <span className="attempts">Attempts: {task.attempts}</span>
          </div>
          <div className="description-content">
            <p>{task.description}</p>
          </div>

          {task.test_cases && task.test_cases.length > 0 && (
            <div className="test-cases">
              <h3>Test Cases</h3>
              {task.test_cases.map((test, index) => (
                <div key={index} className="test-case">
                  <div>
                    <strong>Input:</strong>
                    <pre>{test.input}</pre>
                  </div>
                  <div>
                    <strong>Expected Output:</strong>
                    <pre>{test.expected_output}</pre>
                  </div>
                </div>
              ))}
            </div>
          )}

          {result && (
            <div className={`result-panel ${result.success ? 'success' : 'error'}`}>
              <div className="result-header">
                {result.success ? (
                  <CheckCircle size={24} color="#4CAF50" />
                ) : (
                  <XCircle size={24} color="#F44336" />
                )}
                <h3>{result.message}</h3>
              </div>
              
              {result.test_results && result.test_results.length > 0 && (
                <div className="test-results">
                  {result.test_results.map((test, index) => (
                    <div key={index} className={`test-result ${test.passed ? 'passed' : 'failed'}`}>
                      <h4>Test {index + 1}: {test.passed ? '✓ Passed' : '✗ Failed'}</h4>
                      {!test.passed && (
                        <>
                          <p><strong>Input:</strong> {test.input}</p>
                          <p><strong>Expected:</strong> {test.expected}</p>
                          <p><strong>Got:</strong> {test.actual || 'No output'}</p>
                          {test.error && <p className="error-msg"><strong>Error:</strong> {test.error}</p>}
                        </>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="editor-section">
          <div className="editor-header">
            <h3>Code Editor</h3>
            <button 
              onClick={handleSubmit} 
              disabled={submitting}
              className="submit-btn"
            >
              <Play size={20} />
              {submitting ? 'Running...' : 'Run Code'}
            </button>
          </div>
          <Editor
            height="500px"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              automaticLayout: true,
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default TaskView;