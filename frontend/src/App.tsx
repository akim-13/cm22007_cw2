import React, { useState, useMemo, useRef } from "react";
import Calendar from './components/Calendar';
import TaskEventModal from "./components/TaskEventModal";
import TaskCard from "./components/TaskCard";
import InputPrompt from "./components/InputPrompt";
import './styles/fullcalendar.css';

const App: React.FC = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const initialExtendedProps = {
        username: "joe",
        // EventExtras
        taskID: undefined,
        description: undefined,
        // TaskExtras
        priority: 0,
        isCompleted: false,
        duration: undefined,
        events: undefined,
    }

    const newFCEvent = useRef<{ [key: string]: any }>({ initialExtendedProps: {...initialExtendedProps} });
    const [events, setEvents] = useState<EventInput[]>([
        { title: "testevent", start: new Date().toISOString(), extendedProps: { priority: "1" } },
        { title: 'Task 1', start: '2025-02-25T10:00:00' },
        { title: 'Task 2', start: '2025-02-23T13:00:00' },
        { title: 'Task 3', start: '2025-02-23T09:00:00' },
    ]);

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
                {isModalOpen && (
                    <TaskEventModal
                        events={memoizedEvents}
                        setEvents={setEvents}
                        isModalOpen={isModalOpen}
                        setIsModalOpen={setIsModalOpen}
                        newFCEvent={newFCEvent}
                        initialExtendedProps={initialExtendedProps}
                    />
                )}

                <Calendar 
                    events={memoizedEvents} 
                    setIsModalOpen={setIsModalOpen} 
                    newFCEvent={newFCEvent}
                    initialExtendedProps={initialExtendedProps}
                />

                <div className="pt-4">
                    <InputPrompt setIsModalOpen={setIsModalOpen}/>
                </div>
                    
            </div>
        </div>
    );

};

export default App;
