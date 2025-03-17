import React, { useState, useEffect, useRef} from "react";
import axios from "axios"; // Make sure axios is imported
import Calendar from "./components/Calendar";
import TaskEventModal from "./components/TaskEventModal";
import TaskCard from "./components/TaskCard";
import InputPrompt from "./components/InputPrompt";
import SignIn from "./components/SignIn"; // Import the SignIn component
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

  
  // Fetch tasks from the API when the component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const taskResponse = await axios.get(`http://localhost:8000/get_user_tasks/${initialExtendedProps.username}`);
        console.log("Tasks fetched from API:", taskResponse.data.tasks);
        setTasks(taskResponse.data.tasks); // Assuming the response has a 'tasks' key
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, [initialExtendedProps.username]); // Fetch tasks when the component mounts or when the username changes

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
            {tasks.length > 0 ? (
              tasks.map((task) => (
                <TaskCard
                  key={task.taskID} // Unique key for each task
                  title={task.title}
                  priority={task.priority === 0 ? "Low" : "High"} // Assuming priority is a number
                  duration={`${task.duration} hours`}
                  deadline={task.deadline}
                  description={task.description}
                  dropdown={true} // or false based on your needs
                  otherTasks={[
                    "Set up database",
                    "Create routes",
                    "Implement security measures",
                  ]}
                />
              ))
            ) : (
              <p>No tasks available</p> // Display a message when there are no tasks
            )}
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
