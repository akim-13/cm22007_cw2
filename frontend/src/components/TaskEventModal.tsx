import React, { useState, useRef } from "react";
import { Dialog, DialogTitle } from "@headlessui/react";
import {
  TitleInput,
  StartDateInput,
  EndDateInput,
  DurationInput,
  PrioritySelect,
  DescriptionInput,
  CompletedCheckbox,
  ModeToggleButton,
} from "./TaskEventInputs";
import axios from "axios";

const HOST="http://localhost:8000"


interface TaskEventModalProps {
    events: InputEvent[];
    setEvents: (events: InputEvent[]) => void;
    isModalOpen: boolean;
    setIsModalOpen: (value: boolean) => void;
}


const TaskEventModal: React.FC<TaskEventModalProps> = ({ 
    events, setEvents, 
    isModalOpen, setIsModalOpen, 
    newFCEvent, initialExtendedProps,
}) => {
    const [isTaskMode, setIsTaskMode] = useState(true);
    const [, forceUpdate] = useState(0); 

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

        forceUpdate(x => x+1);
    };

    const getFormData = () => {
        const currentFCEvent = newFCEvent.current;
        const formData = new FormData();

        if (isTaskMode) {
            formData.append("title", currentFCEvent.title);
            formData.append("deadline", currentFCEvent.start);
            formData.append("description", currentFCEvent.extendedProps.description);
            formData.append("duration", currentFCEvent.extendedProps.duration);
            formData.append("priority", currentFCEvent.extendedProps.priority);
        } else {
            formData.append("start", currentFCEvent.start);
            formData.append("end", currentFCEvent.end);
            formData.append("standaloneEventName", currentFCEvent.title);
            formData.append("standaloneEventDescription", currentFCEvent.extendedProps.description);
        }

        return formData;
    }

    const sendAddRequest = async (formData: formData) => {
        try {
            const addOperation = isTaskMode ? "add_task" : "add_standalone_event"
            const response = await axios.post(`${HOST}/${addOperation}`, formData );
            console.log(`Add request ${addOperation} sent successfully:`)
            for (const pair of formData.entries()) { console.log(`${pair[0]}: ${pair[1]}`); }
        } catch (error) {
            console.error("Error performing ${operation}:", error);
        }
    }

    const fetchTasksOrEventsData = async () => {
        try {
            const getOperation = isTaskMode ? "get_latest_user_task" : "get_latest_standalone_event"
            const username = "joe"
            const response = await axios.get(`${HOST}/${getOperation}/${username}`)
            console.log(`Fetch request ${getOperation} successful:`)
            console.log(response.data)
            return response.data
        } catch (error) {
            console.error(`Error performing ${getOperation}:`, error);
            return null
        }
    }

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        // newFCEvent.current = { extendedProps: {...initialExtendedProps} }

        const formData = getFormData();
        await sendAddRequest(formData);
        const taskOrEventData = await fetchTasksOrEventsData();

        if (taskOrEventData === null) {
            alert("Sorry, something went wrong.")
            console.error("Something went wrong when adding a task or an event. No changes have been made.")
            return
        }

        if (isTaskMode) {
            newFCEvent.current.extendedProps["username"] = taskOrEventData.latest_task.username
            newFCEvent.current["id"] = taskOrEventData.latest_task.taskID
            try {
                const response = await axios.get(`${HOST}/get_events_from_task/${newFCEvent.current["id"]}`)
                // TODO: Process and add these events.
                console.warn(response.data)
            } catch (error) {
                console.error(`Error retrieving events from task ID "${newFCEvent.current["id"]}"`, error)
            }
        } else {
            newFCEvent.current.extendedProps["username"] = taskOrEventData.latest_standalone_event.username
            newFCEvent.current["id"] = taskOrEventData.latest_standalone_event.standaloneEventID
        }

        setEvents([...events, {...newFCEvent.current}]);
        setIsModalOpen(false);
    };

    return (
      <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} className="fixed inset-0 flex z-[10000] items-center justify-center">
        <div className="fixed bg-gray-200 p-6 rounded-lg shadow-lg w-[400px] min-h-[505px] flex flex-col">

          <DialogTitle className="text-lg font-bold text-black">
            {isTaskMode ? "Manage Task" : "Manage Event"}
          </DialogTitle>

          {/* Toggle Mode Buttons */}
          <div className="flex space-x-4 mt-2">
            <ModeToggleButton mode="task" isActive={isTaskMode} setIsTaskMode={setIsTaskMode} />
            <ModeToggleButton mode="event" isActive={!isTaskMode} setIsTaskMode={setIsTaskMode} />
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="mt-4 flex-1 flex flex-col justify-between">

            {/* Shared Fields */}
            <TitleInput value={newFCEvent.current.title} onChange={handleInputChange} isTaskMode={isTaskMode} />
            <StartDateInput value={newFCEvent.current.start} onChange={handleInputChange} />

            {/* Specific Fields */}
            <div className="min-h-[150px]">
                {isTaskMode ? (
                    <>
                        {/* Task-Specific Fields */}
                        <DurationInput value={newFCEvent.current.extendedProps.duration} onChange={handleInputChange} />
                        <PrioritySelect value={newFCEvent.current.extendedProps.priority} onChange={handleInputChange} />
                        <DescriptionInput value={newFCEvent.current.extendedProps.description} onChange={handleInputChange} />
                        <CompletedCheckbox checked={newFCEvent.current.extendedProps.isCompleted} onChange={handleInputChange} />
           
                    </>
                ) : (
                    <>
                        {/* Event-Specific Fields */}
                        <EndDateInput value={newFCEvent.current.end} onChange={handleInputChange} />
                        <DescriptionInput value={newFCEvent.current.extendedProps.description} onChange={handleInputChange} />
         
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
