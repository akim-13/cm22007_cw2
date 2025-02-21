import React, { useState } from "react";
import { Dialog, DialogTitle } from "@headlessui/react";
//import './styles/fullcalendar.css';
import { EventInput } from "@fullcalendar/core";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

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
    const [newEvent, setNewEvent] = useState<EventInput>({});
    const [events, setEvents] = useState<EventInput[]>([{title: "testevent", start: new Date().toISOString()}]);
    const [isTaskMode, setIsTaskMode] = useState(true);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setEvents([...events, {...newEvent, start: new Date().toISOString()}]);
        // Default start to now.
        setIsModalOpen(false);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        // The spread operator {...x, y} copies the fields from the old object x to the new one y
        // to ensure that changing one fieild doesn't delete the others. The [] syntax is for
        // evaluating event.target.name and making the evaluated expression the key.
        setNewEvent({...newEvent, [event.target.name]: event.target.value});
    };

    const formatDate = (isoString) => {
      if (!isoString) return "";
      const date = new Date(isoString);
      return date.toLocaleString("en-US", { dateStyle: "short", timeStyle: "short" });
    };

    return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">
      
      {/* If the function isn't wrapped in lambda, it will execute immediately when rendered. */}
      <button onClick={() => setIsModalOpen(true)}>Create event</button>


        {isModalOpen && (
          <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} className="fixed inset-0 flex items-center justify-center">
            <div className="bg-gray-200 p-6 rounded-lg shadow-lg w-[400px] min-h-[450px] flex flex-col">
              <DialogTitle className="text-lg font-bold text-black">
                {isTaskMode ? "Create Task" : "Create Event"}
              </DialogTitle>

              {/* Toggle Mode Buttons */}
              <div className="flex space-x-4 mt-2">
                <label className="flex items-center cursor-pointer">
                  <input
                    name="mode"
                    type="radio"
                    value="task"
                    checked={isTaskMode}
                    onChange={() => setIsTaskMode(true)}
                    className="hidden"
                  />
                  <span className={`px-4 py-2 rounded ${isTaskMode ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
                    Task
                  </span>
                </label>

                <label className="flex items-center cursor-pointer">
                  <input
                    name="mode"
                    type="radio"
                    value="event"
                    checked={!isTaskMode}
                    onChange={() => setIsTaskMode(false)}
                    className="hidden"
                  />
                  <span className={`px-4 py-2 rounded ${!isTaskMode ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
                    Event
                  </span>
                </label>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="mt-4 flex-1 flex flex-col justify-between">
                {/* Shared Fields */}
                <input
                  name="title"
                  type="text"
                  placeholder={isTaskMode ? "Task Title" : "Event Title"}
                  value={newEvent.title}
                  onChange={handleInputChange}
                  required
                  className="border p-2 rounded w-full mt-2"
                />

                <input
                  name="start"
                  type="text"
                  onFocus={(e) => (e.target.type = "datetime-local")}
                  onBlur={(e) => {
                    e.target.type = "text";
                    e.target.value = formatDate(e.target.value);
                  }}
                  placeholder={isTaskMode ? "Deadline" : "Start Date"}
                  value={newEvent.start}
                  onChange={handleInputChange}
                  required
                  className="border p-2 rounded w-full mt-2"
                />

                {/* Fixed Height for Conditional Fields */}
                <div className="min-h-[150px]">
                  {/* Task-Specific Fields */}
                  {isTaskMode && (
                    <>
                      <input
                        name="duration"
                        type="number"
                        placeholder="Estimated Duration (Hours)"
                        value={newEvent.duration}
                        onChange={handleInputChange}
                        className="border p-2 rounded w-full mt-2"
                      />

                      <select
                        name="priority"
                        value={newEvent.priority}
                        onChange={handleInputChange}
                        className="border p-2 rounded w-full mt-2"
                      >
                        <option value="1">Low Priority</option>
                        <option value="2">Medium Priority</option>
                        <option value="3">High Priority</option>
                      </select>

                      <textarea
                        name="description"
                        placeholder="Description"
                        value={newEvent.description}
                        onChange={handleInputChange}
                        className="border p-2 rounded w-full mt-2"
                      />

                      <label className="flex items-center mt-2 text-black">
                        <input
                          name="isCompleted"
                          type="checkbox"
                          checked={newEvent.isCompleted}
                          onChange={(e) => setNewEvent({ ...newEvent, isCompleted: e.target.checked })}
                          className="mr-2"
                        />
                        Mark as Completed
                      </label>
                    </>
                  )}

                  {/* Event-Specific Fields */}
                  {!isTaskMode && (
                    <>
                      <input
                        name="end"
                        type="text"
                        onFocus={(e) => (e.target.type = "datetime-local")}
                        onBlur={(e) => {
                          e.target.type = "text";
                          e.target.value = formatDate(e.target.value);
                        }}
                        placeholder="End Date"
                        value={newEvent.end}
                        onChange={handleInputChange}
                        required
                        className="border p-2 rounded w-full mt-2"
                      />

                      <textarea
                        name="description"
                        placeholder="Description"
                        value={newEvent.description}
                        onChange={handleInputChange}
                        className="border p-2 rounded w-full mt-2"
                      />
                    </>
                  )}
                </div>

                {/* Buttons */}
                <div className="mt-4 flex justify-end space-x-2">
                  <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
                    {isTaskMode ? "Add Task" : "Add Event"}
                  </button>
                  <button type="button" onClick={() => setIsModalOpen(false)} className="bg-gray-500 text-white px-4 py-2 rounded">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </Dialog>
        )}
      
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        editable={true}
        selectable={true}
        height="95%"
        timeZone="local"
        headerToolbar={{
          left: 'prev,next,today',
          center: 'title',
          right: ''
        }}
        events={events}
        views={{
          timeGridWeek: {
            type: 'timeGrid',
            slotDuration: '01:00:00',
            slotLabelInterval: '01:00:00',
          }
        }}
        scrollTime={'09:00:00'}
        eventBorderColor="white"
        eventColor="rgb(59,130,246)"
      />
    </div>
    );
};

export default App;
