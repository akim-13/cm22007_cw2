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

interface ExtendedProps {
  description: string;
  duration: string;
  priority: string;
  isCompleted: boolean;
  username?: string;
  taskID?: string;
}

interface FCEvent {
  id?: string;
  title: string;
  start: string;
  end: string;
  extendedProps: ExtendedProps;
}

interface TaskEvent {
  start: string;
  end: string;
  taskID: string;
}

interface TaskEventModalProps {
  events: FCEvent[];
  setEvents: (events: FCEvent[]) => void;
  isModalOpen: boolean;
  setIsModalOpen: (value: boolean) => void;
  newFCEvent: React.MutableRefObject<FCEvent>;
  initialExtendedProps: ExtendedProps;
  isTaskMode: boolean;
  setIsTaskMode: (value: boolean) => void;
}

const TaskEventModal: React.FC<TaskEventModalProps> = ({ 
    events, setEvents, 
    isModalOpen, setIsModalOpen, 
    newFCEvent, initialExtendedProps,
    isTaskMode, setIsTaskMode,
}) => {
    const [, forceUpdate] = useState(0); 

    const handleInputChange = async (
      event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
    ) => {
        const { name, type } = event.target;
        const value = type === "checkbox" ? (event.target as HTMLInputElement).checked : event.target.value;

        const isMainProp = name === "title" || name === "start" || name === "end"

        if (isMainProp) {
            newFCEvent.current[name as keyof Pick<FCEvent, "title" | "start" | "end">] = value as string;
        } else {
            newFCEvent.current.extendedProps = {
                ...newFCEvent.current.extendedProps, 
                [name]: value
            };
        }

        forceUpdate(x => x+1);

        const id = newFCEvent.current["id"] ?? -1;
        try {
            if (type === "checkbox" && (event.target as HTMLInputElement).checked) {
                await axios.put(`${HOST}/complete_task/${id}`);
                console.log(`Task "${id}" completed successfully`);
            } else {
                await axios.put(`${HOST}/incomplete_task/${id}`);
                console.log(`Task "${id}" uncompleted successfully`);
            }
        } catch (error) {
            console.error("Error completing a task", error);
        }
    };

    const handleDelete = async () => {
        const currentFCEvent = newFCEvent.current;
        if (!currentFCEvent.id) {
            console.log("Nothing to delete");
            return;
        }

        try {
            if (isTaskMode) {
                await axios.delete(`${HOST}/delete_events_from_task/${currentFCEvent.id}`);
                console.log(`Events of task "${currentFCEvent.id}" deleted successfully.`);
                await axios.delete(`${HOST}/delete_task/${currentFCEvent.id}`);
                console.log(`Task "${currentFCEvent.id}" deleted successfully.`);
            } else {
                await axios.delete(`${HOST}/delete_standalone_event/${currentFCEvent.id}`);
                console.log(`Event "${currentFCEvent.id}" deleted successfully.`);
            }
        } catch (e) {
            console.error("Error deleting task or event", e);
        }

        setIsModalOpen(false);
        window.location.reload();
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
    };

    const sendAddRequest = async (formData: FormData) => {
        const addOperation = isTaskMode ? "add_task" : "add_standalone_event";
        console.warn([...formData.entries()]);
        const response = await axios.post(`${HOST}/${addOperation}`, formData);
        console.log(`Add request ${addOperation} sent successfully:`);
        for (const pair of formData.entries()) { console.log(`${pair[0]}: ${pair[1]}`); }
        return response;
    };

    const fetchTasksOrEventsData = async () => {
        const getOperation = isTaskMode ? "get_latest_user_task" : "get_latest_standalone_event";
        const username = "joe";
        try {
            const response = await axios.get(`${HOST}/${getOperation}/${username}`);
            console.log(`Fetch request ${getOperation} successful:`);
            console.log(response.data);
            return response.data;
        } catch (error) {
            console.error(`Error performing ${getOperation}:`, error);
            return null;
        }
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const formData = getFormData();

        if (newFCEvent.current.id) {
            console.log("Nothing yet but should be edited.");
            setIsModalOpen(false);

            if (isTaskMode) {
                window.location.reload();
            }
            return;
        }

        await sendAddRequest(formData);
        const taskOrEventData = await fetchTasksOrEventsData();

        if (taskOrEventData === null) {
            alert("Sorry, something went wrong.");
            console.error("Something went wrong when adding a task or an event. No changes have been made.");
            return;
        }

        const taskEvents: FCEvent[] = [];

        if (isTaskMode) {
            newFCEvent.current.extendedProps.username = taskOrEventData.latest_task.username;
            newFCEvent.current.id = taskOrEventData.latest_task.taskID;
            try {
                const response = await axios.put(`${HOST}/breakdown_task/${newFCEvent.current.id}`);

                if (response.data && Array.isArray(response.data.events_added)) {
                    response.data.events_added.forEach((event: TaskEvent) => {
                        const curTaskEvent: FCEvent = { 
                            title: newFCEvent.current.title,
                            start: event.start, 
                            end: event.end, 
                            extendedProps: {
                                ...initialExtendedProps, 
                                taskID: event.taskID
                            }
                        };

                        taskEvents.push(curTaskEvent);
                    });
                } else {
                    console.error("Invalid response format:", response.data);
                }

            } catch (error) {
                console.error(`Error retrieving events from task ID "${newFCEvent.current.id}"`, error);
            }
        } else {
            newFCEvent.current.extendedProps.username = taskOrEventData.latest_standalone_event.username;
            newFCEvent.current.id = taskOrEventData.latest_standalone_event.standaloneEventID;
        }

        const newEventTmp: FCEvent = JSON.parse(JSON.stringify(newFCEvent.current)); 
        setEvents([...events, ...taskEvents, newEventTmp]);
        setIsModalOpen(false);

        if (!isTaskMode) {
            window.location.reload();
        }
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
          <form role="form" onSubmit={handleSubmit} className="mt-4 flex-1 flex flex-col justify-between">

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
            <div className="flex justify-center space-x-2">
                <button
                    type="submit"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                    {newFCEvent.current.id ? "Update" : "Create"}
                </button>
                <button
                    type="button"
                    onClick={handleDelete}
                    className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
                >
                    Delete
                </button>
                <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-4 py-2 bg-gray-300 text-black rounded-md hover:bg-gray-400"
                >
                    Cancel
                </button>
            </div>
          </form>
        </div>
      </Dialog>
    );
};

export default TaskEventModal;
