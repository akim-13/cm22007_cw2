import React from "react";
import './styles/fullcalendar.css';
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

const App: React.FC = () => {
  return (
    <div className="p-5 h-screen fixed top-0 bottom-0 left-0 right-0">
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        editable={true}
        selectable={true}
        height="95%"
        timeZone="GMT"
        headerToolbar={{
          left: 'prev,next,today',
          center: 'title',
          right: ''
        }}
        events={[
          { title: "Event 1", date: "2025-02-20" },
          { title: "Event 2", date: "2025-02-22" },
        ]}
        views={{
          timeGridWeek: {
            type: 'timeGrid',
            slotDuration: '01:00:00',
          }
        }}
      />
    </div>
  );
};

export default App;