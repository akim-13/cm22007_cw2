import { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import axios from "axios";
import AchievementModal from "./AchievementModal";
import SettingsModal from "./SettingsModal";
import { StandaloneEvent, Task, TaskEvent } from "../App";

// interface Task {
//     id: string;
//     title: string;
//     start: string;
//     extendedProps: {
//         description: string;
//         priority: number;
//         duration: number;
//         isCompleted: boolean;
//     };
// }

// interface StandaloneEvent {
//     id: string;
//     title: string;
//     start: string;
//     end: string;
// }

// interface CalendarEvent {
//     title: string;
//     start: string;
//     end: string;
// }

// // TODO: Move these conversions to Calendar component
// const fetchStandaloneEvents = async () => {
//     try {
//         const standaloneEventsResponse = await axios.get(
//             `http://localhost:8000/get_standalone_events/${username}`
//         );
//         const standaloneEvents = standaloneEventsResponse.data.standalone_events.map(
//             (event: any) => ({
//                 id: "standalone-" + event.standaloneEventID.toString(),
//                 title: event.standaloneEventName,
//                 start: event.start,
//                 end: event.end,
//             })
//         );
//         setStandaloneEvents([...standaloneEvents]);
//     } catch (error) {
//         console.error("Error fetching events:", error);
//     }
// };

// const fetchTaskEvents = async () => {
//     try {
//         const eventsResponse = await axios.get(
//             `http://localhost:8000/get_events_from_user/${username}`
//         );
//         const events = eventsResponse.data.events.map(
//             (event: any) => ({
//                 id: "ev-" + event.eventID.toString(),
//                 title: event.title,
//                 start: event.start,
//                 end: event.end,
//             })
//         );
//         setTaskEvents([...events]);
//     } catch (error) {
//         console.error("Error fetching events:", error);
//     }
// };

// const fetchTasks = async () => {
//     try {
//         const taskResponse = await axios.get(`http://localhost:8000/get_user_tasks/${username}`);
//         console.log("Tasks fetched from API:", taskResponse.data.tasks); 
//         const tasks = taskResponse.data.tasks.map((task: any) => ({
//             id: "taskev-" + task.taskID.toString(),
//             title: task.title,
//             start: new Date(task.deadline).toISOString(),
//             extendedProps: {
//                 description: task.description,
//                 priority: task.priority,
//                 duration: task.duration,
//                 isCompleted: task.isCompleted,
//             },
//         }));
//         setTasks(tasks);
//     } catch (error) {
//         console.error("Error fetching tasks:", error);
//     }
// };

const formatDate = (date: Date): string => {
    // return date.toLocaleString("en-US", {
    //     month: "2-digit",
    //     day: "2-digit",
    //     year: "numeric",
    //     hour: "2-digit",
    //     minute: "2-digit",
    //     hour12: true,
    // });

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
