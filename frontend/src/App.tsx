import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import InputPrompt from "./components/InputPrompt";

const App: React.FC = () => {
  return (
    <div style={{ padding: "20px" }}>
      <h2>FullCalendar</h2>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridWeek"
        editable={true}
        selectable={true}
        events={[
          { title: "Event 1", date: "2025-02-20" },
          { title: "Event 2", date: "2025-02-22" },
        ]}
      />
      <InputPrompt />
    </div>
  );
};

export default App;
