import React, { useState } from "react";
import { Dialog, DialogTitle } from "@headlessui/react";
//import './styles/fullcalendar.css';
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

const App: React.FC = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newEvent, setNewEvent] = useState<any>({title: "", start: "", end: ""});
    const [events, setEvents] = useState<any>([{title: "testevent", start: new Date().toISOString()}]);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        // Default start to now.
        setEvents([...events, {...newEvent, start: new Date().toISOString()}]);
        setIsModalOpen(false);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        // The spread operator {...x, y} copies the fields from the old object x to the new one y
        // to ensure that changing one fieild doesn't delete the others. The [] syntax is for
        // evaluating event.target.name and making the evaluated expression the key.
        setNewEvent({...newEvent, [event.target.name]: event.target.value});
    };

    return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">
      
      {/* If the function isn't wrapped in lambda, it will execute immediately when rendered. */}
      <button onClick={() => setIsModalOpen(true)}>Create event</button>
      
        {isModalOpen && (
            <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} className="fixed inset-0 flex items-center justify-center">
                <div className="bg-gray-200 p-6 rounded-lg shadow-lg">
                    <DialogTitle className="text-lg font-bold text-black">Create Event</DialogTitle>
                    <form onSubmit={handleSubmit}>
                        <input
                            type="text"
                            name="title"
                            placeholder="Event Title"
                            value={newEvent.title}
                            onChange={handleInputChange}
                            required
                            className="border p-2 rounded w-full mt-2"
                        />
                        <div className="mt-4 flex justify-end space-x-2">
                            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
                                Add Event
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
