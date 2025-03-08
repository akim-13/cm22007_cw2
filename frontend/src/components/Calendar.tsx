import React, { useState } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import AchievementModal from "./AchievementModal";

// Add setIsModalOpen to the component props
const Calendar: React.FC<any> = ({ events, setIsModalOpen }) => {
    const [isAchievementModalOpen, setIsAchievementModalOpen] = useState(false);

    const handleAchievementsClick = () => {
        setIsAchievementModalOpen(true);
    };

    const handleSettingsClick = () => {
        //Add your settings logic here
        alert('Settings panel will be shown here');
    }

    return (
        <>
            <FullCalendar
                plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                initialView="timeGridWeek"
                editable={true}
                selectable={true}
                height="90%"
                timeZone="local"
                headerToolbar={{
                    left: 'prev,next,today,title',
                    center: '',
                    right: 'achievements,settings'
                }}
                titleFormat={
                    { month: 'short', day: 'numeric' ,year: "numeric"}
                }
                customButtons={{
                    achievements: {
                        text: 'Achievements',
                        click: handleAchievementsClick
                    },
                    settings: {
                        text: 'Settings',
                        click: handleSettingsClick
                    },
                }}
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
                    const extendedProps = info.event.extendedProps;
                    let extendedPropsText = "";

                    if (extendedProps) {
                        extendedPropsText = Object.entries(extendedProps)
                            .map( ([key, value]) => `${key}: ${value}`)
                            .join("\n");
                    }

                    alert(`Event: ${info.event.title}\nID: ${info.event.id}\nStarts: ${startTime}\nEnds: ${endTime}\n---\nExtended props:\n${extendedPropsText}`);
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
            
            <AchievementModal 
                isOpen={isAchievementModalOpen} 
                onClose={() => setIsAchievementModalOpen(false)} 
            />
        </>
    );
};

export default Calendar;
