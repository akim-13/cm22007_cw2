<<<<<<< Updated upstream
import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
=======
import React, { useState, useMemo } from "react";
import Calendar from "./components/Calendar";
import TaskEventModal from "./components/TaskEventModal";
>>>>>>> Stashed changes
import InputPrompt from "./components/InputPrompt";
import SettingsModal from "./components/SettingsModal";

<<<<<<< Updated upstream
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
      <InputPrompt />
=======
// TODO: Check if this is needed.
import "./styles/fullcalendar.css";

interface EventExtras {
  // Commented out are the properties of FullCalendar's EventInput.
  // title: string,
  // start: string | Date,
  // end?:  string | Date,
  // id:    string,
  taskID: string | null;
}

interface TaskExtras {
  // title:     string,
  // id:        strgin,
  // start:     string,
  description?: string;
  isCompleted: boolean;
  duration: number;
  priority: number;
  events?: Event[] | null;
}

const App: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [events, setEvents] = useState<EventInput[]>([
    { title: "testevent", start: new Date().toISOString() },
    { title: "Task 1", start: "2025-02-25T10:00:00" },
    { title: "Task 2", start: "2025-02-23T13:00:00" },
    { title: "Task 3", start: "2025-02-23T09:00:00" },
  ]);

  // FIXME: Doesn't work, the calendar is still re-rendered when modal is open.
  // Memoize events so they don't get a new reference unless updated
  const memoizedEvents = useMemo(() => events, [events]);

  return (
    <div className="flex h-screen w-full">
      {/* Task Card on the left */}
      <div className="flex-none w-1/5 p-4 border-r border-gray-300">
        <TaskCard
          title="Develop API Endpoints"
          priority="high"
          duration="6 hours"
          deadline="2025-03-01"
          description="Build and test backend endpoints for user authentication and data retrieval."
          dropdown={true}
          otherTasks={[
            "Set up database",
            "Create routes",
            "Implement security measures",
          ]}
        />
      </div>

      {/* Main content on the right */}
      <div className="flex-grow p-6">
        {isModalOpen && (
          <TaskEventModal
            events={memoizedEvents}
            setEvents={setEvents}
            isModalOpen={isModalOpen}
            setIsModalOpen={setIsModalOpen}
          />
        )}
        <Calendar events={memoizedEvents} setIsModalOpen={setIsModalOpen} />
        <div className="pt-4">
          <InputPrompt />
        </div>
      </div>
>>>>>>> Stashed changes
    </div>
  );
};

export default App;
