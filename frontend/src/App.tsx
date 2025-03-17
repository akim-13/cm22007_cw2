import React, { useState, useRef, useEffect } from "react";
import Calendar from "./components/Calendar";
import TaskEventModal from "./components/TaskEventModal";
import TaskCard from "./components/TaskCard";
import InputPrompt from "./components/InputPrompt";
import SignIn from "./components/SignIn"; // Import the SignIn component
import axios from "axios";
import "./styles/fullcalendar.css";

const App: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false); // added from input_prompt
  const [isSignedIn, setIsSignedIn] = useState(false); // Authentication state
  const [tasks, setTasks] = useState<any[]>([]); // Store tasks fetched from the API
  const initialExtendedProps = {
    username: "joe",
    taskID: undefined,
    description: undefined,
    priority: 0,
    isCompleted: false,
    duration: undefined,
    events: undefined,
  };

  const newFCEvent = useRef<{ [key: string]: any }>({
    extendedProps: { ...initialExtendedProps },
  });

  const [events, setEvents] = useState<EventInput[]>([
    {
      title: "testevent",
      start: new Date().toISOString(),
      extendedProps: { priority: "1" },
    },
    { title: "Task 1", start: "2025-02-25T10:00:00" },
    { title: "Task 2", start: "2025-02-23T13:00:00" },
    { title: "Task 3", start: "2025-02-23T09:00:00" },
  ]);

  // Fetch tasks from the API when the component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const username = "joe"; // Replace with dynamic username if needed
        const response = await axios.get(`http://localhost:8000/get_user_tasks/${username}`);
        setTasks(response.data.tasks); // Update tasks state with the fetched tasks
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, []);

  const handleSignIn = () => {
    setIsSignedIn(true); // Update authentication state once the user signs in
  };

  return (
    <div className="flex h-screen w-full justify-center">
      {/* Show SignIn component if not signed in */}
      {!isSignedIn ? (
        <SignIn onSignIn={handleSignIn} />
      ) : (
        <>
          {/* Task Card on the left */}
          <div className="flex-none w-[300px] p-4 border-r border-gray-300">
            {/* Render task cards dynamically based on fetched tasks */}
            {tasks.map((task) => (
              <TaskCard
                key={task.taskID}
                title={task.title}
                priority={task.priority === 0 ? "low" : "high"} // Example of mapping priority
                duration={task.duration ? `${task.duration} hours` : "N/A"}
                deadline={task.deadline}
                description={task.description}
                dropdown={true}
                otherTasks={[]} // You can dynamically fetch and pass other tasks if needed
              />
            ))}
          </div>

          {/* Main content on the right */}
          <div className="flex-grow flex flex-col p-6">
            {isModalOpen && (
              <TaskEventModal
                events={events}
                setEvents={setEvents}
                isModalOpen={isModalOpen}
                setIsModalOpen={setIsModalOpen}
                newFCEvent={newFCEvent}
                initialExtendedProps={initialExtendedProps}
              />
            )}

            <Calendar
              events={events}
              setIsModalOpen={setIsModalOpen}
              newFCEvent={newFCEvent}
              initialExtendedProps={initialExtendedProps}
            />

            <div className="pt-4">
              <InputPrompt
                setIsModalOpen={setIsModalOpen}
                initialExtendedProps={initialExtendedProps}
                newFCEvent={newFCEvent}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default App;
