import React from 'react';
import TaskieChat from './components/TaskieChat';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Taskie Chat Interface</h1>
      </header>
      <main>
        <TaskieChat />
      </main>
    </div>
  );
}

export default App;