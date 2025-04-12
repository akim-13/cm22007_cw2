import { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import axios from "axios";
import AchievementModal from "./AchievementModal";
import SettingsModal from "./SettingsModal";
import { StandaloneEvent, Task, TaskEvent } from "../App";

const formatDate = (date: Date): string => {
    // Time zones/daylight saving time
    const adjusted = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    return adjusted.toISOString().slice(0, 16);
};

const Calendar: React.FC<any> = ({ standaloneEvents, taskEvents, tasks, setIsModalOpen, setModalTypeLocked, newFCEvent, initialExtendedProps, setModalType }) => {
    const [isAchievementModalOpen, setIsAchievementModalOpen] = useState(false);
    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
    const username = "joe"; 

    const handleEventClick = (info: any) => {
        const startTime = info.event.start ? formatDate(info.event.start) : "";
        const endTime = info.event.end ? formatDate(info.event.end) : "";
        const extendedProps = info.event.extendedProps;
        let extendedPropsText = "";

        if (extendedProps) {
            extendedPropsText = Object.entries(extendedProps)
                .map(([key, value]) => `${key}: ${value}`)
                .join("\n");
        }

        newFCEvent.current = { extendedProps: { ...initialExtendedProps } };
        newFCEvent.current.id = info.event.id
        newFCEvent.current.title = info.event.title || "";
        newFCEvent.current.start = startTime;
        newFCEvent.current.end = endTime;
        newFCEvent.current.extendedProps = extendedProps;
        setModalType(extendedProps.type);
        setIsModalOpen(true);
        setModalTypeLocked(true);
        console.warn(JSON.parse(JSON.stringify(newFCEvent.current)))
    };

    let processedEvents = [
        ...taskEvents.map((event: TaskEvent) => ({
            id: "taskev-" + event.eventID.toString(),
            title: event.title,
            start: event.start,
            end: event.end,
            extendedProps: {
                type: "task_event",
            },
            color: "blue",  // Task events
        })),
        ...tasks.map((task: Task) => ({
            id: "task-" + task.taskID.toString(),
            title: task.title,
            start: task.deadline,
            // end: task.deadline,
            extendedProps: {
                type: "task",
                description: task.description,
                priority: task.priority,
                duration: task.duration,
                isCompleted: task.isCompleted,
            },
            color: "rgb(144,238,144)",  // Light green for tasks
            textColor: "black",
        })),
        ...standaloneEvents.map((event: StandaloneEvent) => ({
            id: "standalone-" + event.standaloneEventID.toString(),
            title: event.standaloneEventName,
            start: event.start,
            end: event.end,
            extendedProps: {
                type: "standalone_event",
                description: event.standaloneEventDescription
            },
            color: "rgb(255,99,132)",  // Red for standalone events
            textColor: "black",
        })),
    ]

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
                    left: "prev,next,today,title",
                    center: "",
                    right: "achievements,settings",
                }}
                titleFormat={{ month: "short", day: "numeric", year: "numeric" }}
                customButtons={{
                    achievements: {
                        text: "Achievements",
                        click: () => setIsAchievementModalOpen(true),
                    },
                    settings: {
                        text: "Settings",
                        click: () => setIsSettingsModalOpen(true),
                    },
                }}

                events={processedEvents}

                eventClick={handleEventClick}
            />

            <AchievementModal
                isOpen={isAchievementModalOpen}
                onClose={() => setIsAchievementModalOpen(false)}
            />
            <SettingsModal
                open={isSettingsModalOpen}
                onClose={() => setIsSettingsModalOpen(false)}
             />
        </>
    );
};

export default Calendar;
