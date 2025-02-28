import React, { useState, useMemo } from "react";
import Calendar from './components/Calendar';
import TaskEventModal from "./components/TaskEventModal";
import TaskCard from "./components/TaskCard";

// TODO: Check if this is needed.
import './styles/fullcalendar.css';

interface EventExtras {
    // Commented out are the properties of FullCalendar's EventInput.
    // title: string,
    // start: string | Date,
    // end?:  string | Date,
    // id:    string,
    taskID: string | null,
}

interface TaskExtras {
    // title:     string,
    // id:        strgin,
    // start:     string,
    description?: string,
    isCompleted:  boolean,
    duration:     number,
    priority:     number,
    events?:      Event[] | null
}

const App: React.FC = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [events, setEvents] = useState<EventInput[]>([
        { title: "testevent", start: new Date().toISOString() },
        { title: 'Task 1', start: '2025-02-25T10:00:00' },
        { title: 'Task 2', start: '2025-02-23T13:00:00' },
        { title: 'Task 3', start: '2025-02-23T09:00:00' },
    ]);

    // FIXME: Doesn't work, the calendar is still re-rendered when modal is open.
    // Memoize events so they don't get a new reference unless updated
    const memoizedEvents = useMemo(() => events, [events]);

    return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">

      {/* If the function isn't wrapped in lambda, it will execute immediately when rendered. */}
      <button onClick={() => setIsModalOpen(true)}>Create event</button>

        {isModalOpen && (
            <TaskEventModal
                events={memoizedEvents}
                setEvents={setEvents}
                isModalOpen={isModalOpen}
                setIsModalOpen={setIsModalOpen}
            />
        )}

        <Calendar events={memoizedEvents}/>

        <h2 className="mt-4">Task List</h2>

        <TaskCard 
            title="Develop API Endpoints" 
            priority="high" 
            duration="6 hours" 
            deadline="2025-03-01" 
            description="Build and test backend endpoints for user authentication and data retrieval."
            dropdown={true} 
            otherTasks={["Set up database", "Create routes", "Implement security measures"]} 
        />

    </div>
    );
};

export default App;

