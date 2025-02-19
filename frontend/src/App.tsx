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
        timeZone="local"
        headerToolbar={{
          left: 'prev,next,today',
          center: 'title',
          right: ''
        }}
        events={'https://fullcalendar.io/api/demo-feeds/events.json'}
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