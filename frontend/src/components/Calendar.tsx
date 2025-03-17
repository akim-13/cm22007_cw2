import { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import axios from "axios";
import AchievementModal from "./AchievementModal";
import SettingsModal from "./SettingsModal";

const formatDate = (date: Date): string => {
    return date.toLocaleString("en-US", {
        month: "2-digit",
        day: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
    });
};

interface TaskEvent {
    eventID: string;
    title: string;
    start: string;
    extendedProps: {
        description: string;
        priority: string;
        duration: string;
        isCompleted: boolean;
    };
}

interface StandaloneEvent {
    eventID: string;
    title: string;
    start: string;
    end: string;
}

const Calendar: React.FC<any> = ({ events, setIsModalOpen, newFCEvent, initialExtendedProps, setIsTaskMode }) => {
    const [isAchievementModalOpen, setIsAchievementModalOpen] = useState(false);
    const [backendEvents, setBackendEvents] = useState<StandaloneEvent[]>([]);
    const [taskEvents, setTaskEvents] = useState<TaskEvent[]>([]);
    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
    const username = "joe"; 
    useEffect(() => {
        fetchEvents();
        fetchTasks();
    }, []);

    const fetchEvents = async () => {
        try {
            const standaloneEventsResponse = await axios.get(
                `http://localhost:8000/get_standalone_events/${username}`
            );
            const standaloneEvents = standaloneEventsResponse.data.standalone_events.map(
                (event: any) => ({
                    eventID: event.standaloneEventID,
                    title: event.standaloneEventName,
                    start: event.start,
                    end: event.end,
                })
            );
            setBackendEvents([...standaloneEvents]);
        } catch (error) {
            console.error("Error fetching events:", error);
        }
    };

    const fetchTasks = async () => {
        try {
            const taskResponse = await axios.get(`http://localhost:8000/get_user_tasks/${username}`);
            console.log("Tasks fetched from API:", taskResponse.data.tasks); 
            const tasks = taskResponse.data.tasks.map((task: any) => ({
                id: task.taskID,
                title: task.title,
                start: new Date(task.deadline).toISOString(),
                extendedProps: {
                    description: task.description,
                    priority: task.priority,
                    duration: task.duration,
                    isCompleted: task.isCompleted,
                },
            }));
            setTaskEvents(tasks);
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    };

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
        newFCEvent.current.title = info.event.title || "";
        newFCEvent.current.start = startTime;
        newFCEvent.current.end = endTime;
        newFCEvent.current.extendedProps = extendedProps;
        setIsTaskMode(!!extendedProps.duration)
        setIsModalOpen(true);
    };

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

                events={[
                    ...events.map(event => ({
                        ...event,
                        color: "blue",  // Default color for newly added events
                    })),
                    ...taskEvents.map(task => ({
                        ...task,
                        color: "rgb(144,238,144)",  // Light green for tasks
                        textColor: "black",
                    })),
                    ...backendEvents.map(event => ({
                        ...event,
                        color: "rgb(255,99,132)",  // Red for backend events
                        textColor: "black",
                    })),
                ]}

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
