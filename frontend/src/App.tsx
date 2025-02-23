import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import TaskCard from "./components/TaskCard";

const App: React.FC = () => {
  return (
    <div style={{ padding: "20px" }}>
      <h2>FullCalendar</h2>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridWeek"
        editable={true}
        selectable={true}
        events={[
          { title: "Event 1", date: "2025-02-20" },
          { title: "Event 2", date: "2025-02-22" },
        ]}
      />

      <h2 className="mt-4">Task List</h2>

      {/* Task cards to test all features */}
      <TaskCard 
        title="Develop API Endpoints" 
        priority="high" 
        duration="6 hours" 
        deadline="2025-03-01" 
        description="Build and test backend endpoints for user authentication and data retrieval."
        dropdown={true} 
        otherTasks={["Set up database", "Create routes", "Implement security measures"]} 
      />

      <TaskCard 
        title="Write Documentation" 
        priority="medium" 
        duration="4 hours" 
        deadline="2025-02-25"
        description="Create user guides and API documentation for developers."
        dropdown={true} 
        otherTasks={["Outline main topics", "Write examples", "Format content"]} 
      />

      <TaskCard 
        title="Update UI Components" 
        priority="high" 
        duration="5 hours" 
        deadline="2025-03-05"
        description="Improve styling and usability of UI components."
        dropdown={true} 
        otherTasks={["Refactor button styles", "Improve accessibility", "Optimize responsiveness"]} 
      />

      <TaskCard 
        title="Team Meeting" 
        priority="low" 
        duration="1 hour" 
        deadline="2025-02-28"
        description="Discuss project progress and next steps."
        dropdown={true} 
        otherTasks={["Prepare slides", "Assign tasks", "Summarize discussion"]} 
      />

      <TaskCard 
        title="Bug Fixes" 
        priority="high" 
        duration="3 hours" 
        deadline="2025-03-02"
        description="Identify and resolve critical bugs affecting the application."
        dropdown={true} 
        otherTasks={["Check error logs", "Fix login issue", "Improve error handling"]} 
      />
    </div>
  );
};

export default App;
