import TaskEventModal from "./components/TaskEventModal";

import React, { useState } from "react";
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
    const [isTaskMode, setIsTaskMode] = useState(true);
    const [newEvent, setNewEvent] = useState<EventInput>({});
    const [events, setEvents] = useState<EventInput[]>([{title: "testevent", start: new Date().toISOString()}]);

    return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">
      
      {/* If the function isn't wrapped in lambda, it will execute immediately when rendered. */}
      <button onClick={() => setIsModalOpen(true)}>Create event</button>

        { 
            isModalOpen && (
                <TaskEventModal
                    events={events}
                    setEvents={setEvents}
                    newEvent={newEvent}
                    setNewEvent={setNewEvent}
                    isModalOpen={isModalOpen}
                    setIsModalOpen={setIsModalOpen}
                    isTaskMode={isTaskMode}
                    setIsTaskMode={setIsTaskMode}
                />
            )
        }
      
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

export default App
