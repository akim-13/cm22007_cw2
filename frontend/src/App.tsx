import React from "react";
import './styles/fullcalendar.css';
import Calendar from './components/Calendar';

const App: React.FC = () => {
  return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">
      <Calendar />
    </div>
  );
};

export default App;
