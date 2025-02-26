import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

const Calendar: React.FC<any> = ({ events }) => {
    const handleAchievementsClick = () => {
        //Add your achievements logic here
        alert('Achievements panel will be shown here');
    };

    const handleSettingsClick = () => {
        //Add your settings logic here
        alert('Settings panel will be shown here');
    }

    return (
        <FullCalendar
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="timeGridWeek"
            editable={true}
            selectable={true}
            height="95%"
            timeZone="local"
            headerToolbar={{
                left: 'prev,next,today,title',
                center: '',
                right: 'achievements,settings'
            }}
            titleFormat={
                { month: 'short', day: 'numeric' ,year: "numeric"}
            }
            //The buttons for the acheivement and settings
            customButtons={{
                achievements: {
                    text: 'Achievements',
                    click: handleAchievementsClick
                },
                settings: {
                    text: 'Settings',
                    click: handleSettingsClick
                }
            }}
            //One would be the events and the other would be the tasks
            eventSources={[
                {
                    url: 'https://fullcalendar.io/api/demo-feeds/events.json',
                    color: 'rgb(59,130,246)', 
                    textColor: 'white', 
                },
                {
                    events: events,
                    color: 'rgb(255,99,132)', 
                    textColor: 'black', 
                }
            ]}
            //Event click handler (replace this with the pop up akim)
            eventClick={(info) => { 
                const startTime = info.event.start ? info.event.start.toLocaleString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                }) : 'No start time';
                
                const endTime = info.event.end ? info.event.end.toLocaleString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                }) : 'No end time';

                alert(`Event: ${info.event.title}\nStarts: ${startTime}\nEnds: ${endTime}`);
            }}
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
            nowIndicator={true}
        />
    );
};

export default Calendar;
