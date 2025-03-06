import React, { useState, useMemo } from "react";
import Calendar from './components/Calendar';
import TaskEventModal from "./components/TaskEventModal";
import TaskCard from "./components/TaskCard";
import InputPrompt from "./components/InputPrompt";

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
        <div className="flex h-screen w-full justify-center">

            {/* Task Card on the left */}
            <div className="flex-none w-[300px] p-4 border-r border-gray-300">
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

            {/* Main content on the right */}
            <div className="flex-grow flex flex-col p-6">
                    <TaskEventModal
                    events={memoizedEvents}
                    setEvents={setEvents}
                    isModalOpen={isModalOpen}
                    setIsModalOpen={setIsModalOpen}
                    />

                <Calendar events={memoizedEvents} setIsModalOpen={setIsModalOpen} />

                <div className="pt-4">
                    <InputPrompt />
                </div>
                    
            </div>
        </div>
    );

};

export default App;
