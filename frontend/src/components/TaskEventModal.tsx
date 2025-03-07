import React, { useState, useRef } from "react";
import { Dialog, DialogTitle } from "@headlessui/react";
import axios from "axios";

const HOST="http://localhost:8000"

interface TaskEventModalProps {
    isModalOpen: boolean;
    setIsModalOpen: (value: boolean) => void;
    events: InputEvent[];
    setEvents: (events: InputEvent[]) => void;
}


interface ModeToggleButtonProps {
  mode: "task" | "event";
  isActive: boolean;
  setIsTaskMode: (value: boolean) => void;
}


const formatDate = (isoString: string): string => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString("en-US", { dateStyle: "short", timeStyle: "short" });
};


const ModeToggleButton: React.FC<ModeToggleButtonProps> = ({ mode, isActive, setIsTaskMode }) => {
  return (
    <label className="flex items-center cursor-pointer">
      <input
        name="mode"
        type="radio"
        value={mode}
        checked={isActive}
        onChange={() => setIsTaskMode(mode === "task")}
        className="hidden"
      />
      <span className={`px-4 py-2 rounded ${isActive ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
        {mode === "task" ? "Task" : "Event"}
      </span>
    </label>
  );
};

const TaskEventModal: React.FC<TaskEventModalProps> = ({ 
    events, setEvents, 
    isModalOpen, setIsModalOpen, 
}) => {
    const newFCEvent = useRef<{ [key: string]: any }>({
        extendedProps: {
            // EventExtras
            taskID: undefined,
            description: undefined,

            // TaskExtras
            isCompleted: undefined,
            duration: undefined,
            priority: undefined,
            events: undefined,
        }
    });
    const [isTaskMode, setIsTaskMode] = useState(true);

    const handleInputChange = (
      event: React.ChangeEvent<HTMLInputElement> |
      React.ChangeEvent<HTMLSelectElement> |
      React.ChangeEvent<HTMLTextAreaElement>
    ) => {
        const { name, value } = event.target;

        const isMainProp = name === "title" || name === "start" || name === "end"

        if (isMainProp) {
            newFCEvent.current[name] = value;
        } else {
            newFCEvent.current.extendedProps = {
                ...newFCEvent.current.extendedProps, 
                [name]: value
            };
        }
    };


    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const currentFCEvent = newFCEvent.current

        if (isTaskMode) {
            const newTask = {
                title: currentFCEvent.title,
                deadline: currentFCEvent.start,
                description: currentFCEvent.extendedProps.description,
                duration: currentFCEvent.extendedProps.duration,
                priority: currentFCEvent.extendedProps.priority
            }            
            try {
                // FIXME: Bad request.
                const response = await axios.post(`${HOST}/add_task`, { newTask });
                alert("Event created successfully!");
            } catch (error) {
                console.error("Error creating event:", error);
            }

        } else {
            const newEvent = {
                standaloneEventName: currentFCEvent.title,
                start: currentFCEvent.start,
                end: currentFCEvent.end,
                standaloneEventDescription: currentFCEvent.extendedProps.description
            }
        }

        setEvents([...events, { ...newFCEvent.current}]);
        setIsModalOpen(false);
    };


    const TitleInput = () => (
      <input
        name="title"
        type="text"
        placeholder={isTaskMode ? "Task Title" : "Event Title"}
        value={newFCEvent.title}
        onChange={handleInputChange}
        required
        className="border p-2 rounded w-full mt-2"
      />
    );


    const StartDateInput = () => (
      <input
        name="start"
        type="text"
        onFocus={(e) => (e.target.type = "datetime-local")}
        onBlur={(e) => {
          e.target.type = "text";
          e.target.value = formatDate(e.target.value);
        }}
        placeholder={isTaskMode ? "Deadline" : "Start Date"}
        value={newFCEvent.start}
        onChange={handleInputChange}
        required
        className="border p-2 rounded w-full mt-2"
      />
    );


    const EndDateInput = () => (
      <input
        name="end"
        type="text"
        onFocus={(e) => (e.target.type = "datetime-local")}
        onBlur={(e) => {
          e.target.type = "text";
          e.target.value = formatDate(e.target.value);
        }}
        placeholder="End Date"
        value={newFCEvent.end}
        onChange={handleInputChange}
        required
        className="border p-2 rounded w-full mt-2"
      />
    );


    const DurationInput = () => (
      <input
        name="duration"
        type="number"
        placeholder="Estimated Duration (Hours)"
        value={newFCEvent.current.extendedProps.duration}
        onChange={handleInputChange}
        className="border p-2 rounded w-full mt-2"
        required
      />
    );


    const PrioritySelect = () => (
      <select
        name="priority"
        value={newFCEvent.current.extendedProps.priority}
        onChange={handleInputChange}
        className="border p-2 rounded w-full mt-2"
      >
        <option value="1">Low Priority</option>
        <option value="2">Medium Priority</option>
        <option value="3">High Priority</option>
      </select>
    );


    const DescriptionInput = () => (
      <textarea
        name="description"
        placeholder="Description"
        value={newFCEvent.current.extendedProps.description}
        onChange={handleInputChange}
        className="border p-2 rounded w-full mt-2"
      />
    );


    const CompletedCheckbox = () => (
      <label className="flex items-center mt-2 text-black">
        <input
          name="isCompleted"
          type="checkbox"
          checked={newFCEvent.isCompleted}
          onChange={(e) =>
            setNewEvent({ ...newFCEvent, isCompleted: e.target.checked })
          }
          className="mr-2"
        />
        Mark as Completed
      </label>
    );


    return (
      <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} className="fixed inset-0 flex z-[10000] items-center justify-center">
        <div className="fixed bg-gray-200 p-6 rounded-lg shadow-lg w-[400px] min-h-[505px] flex flex-col">

          <DialogTitle className="text-lg font-bold text-black">
            {isTaskMode ? "Create Task" : "Create Event"}
          </DialogTitle>

          {/* Toggle Mode Buttons */}
          <div className="flex space-x-4 mt-2">
            <ModeToggleButton mode="task" isActive={isTaskMode} setIsTaskMode={setIsTaskMode} />
            <ModeToggleButton mode="event" isActive={!isTaskMode} setIsTaskMode={setIsTaskMode} />
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="mt-4 flex-1 flex flex-col justify-between">

            {/* Shared Fields */}
            <TitleInput />
            <StartDateInput />

            {/* Specific Fields */}
            <div className="min-h-[150px]">
                {isTaskMode ? (
                    <>
                        {/* Task-Specific Fields */}
                        <DurationInput />
                        <PrioritySelect />
                        <DescriptionInput />
                        <CompletedCheckbox />
                    </>
                ) : (
                    <>
                        {/* Event-Specific Fields */}
                        <EndDateInput />
                        <DescriptionInput />
                    </>
                )}
            </div>

            {/* Buttons */}
            <div className="mt-4 flex justify-end space-x-2">
              <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
                {isTaskMode ? "Submit Task" : "Submit Event"}
              </button>

              <button type="button" onClick={() => setIsModalOpen(false)} className="bg-gray-500 text-white px-4 py-2 rounded">
                Cancel
              </button>
            </div>

          </form>

        </div>
      </Dialog>
    )
}

export default TaskEventModal
