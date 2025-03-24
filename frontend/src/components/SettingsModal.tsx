import { useState } from "react";

interface SettingsModalProps {
  open: boolean;
  onClose: () => void;
}

export default function SettingsModal({ open, onClose }: SettingsModalProps) {
  const [calendarUrl, setCalendarUrl] = useState("");
  const [theme, setTheme] = useState("light");
  const [eventColor, setEventColor] = useState("#ff6384"); // Red for backend events
  const [taskColor, setTaskColor] = useState("#90ee90"); // Light green for tasks


  const handleConfirm = async () => {
    if (!calendarUrl) {
      alert("Please enter a valid calendar URL");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/add_calendar/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ics_url: calendarUrl }),
      });

      if (response.ok) {
        alert("Calendar successfully added!");
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail || "Failed to add calendar"}`);
      }
    } catch (error) {
      console.error("Error adding calendar:", error);
      alert("An error occurred. Please try again.");
    }

    onClose();
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-[10000]">
      <div className="themed-bg p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-center text-lg font-semibold mb-4">Settings</h2>

        {/* Calendar URL Input */}
        <label className="block text-sm font-medium mb-1">Calendar URL:</label>
        <input
          type="url"
          placeholder="https://..."
          value={calendarUrl}
          onChange={(e) => setCalendarUrl(e.target.value)}
          className="border rounded-md p-2 w-full mb-4"
        />

        {/* Theme Selection */}
        <label className="block text-sm font-medium mb-1">Theme:</label>
        <select
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          className="border rounded-md p-2 w-full mb-4"
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>

        {/* Event Color Picker */}
        <label className="block text-sm font-medium mb-1">Event Colour:</label>
        <input
          type="color"
          id="eventColor"
          value={eventColor}
          onChange={(e) => setEventColor(e.target.value)}
          className="w-full h-10 p-1 rounded"
        />

        {/* Task Color Picker */}
        <label className="block text-sm font-medium mb-1">Task Colour:</label>
        <input
          type="color"
          id="taskColor"
          value={taskColor}
          onChange={(e) => setTaskColor(e.target.value)}
          className="w-full h-10 p-1 rounded"
        />

        {/* Buttons */}
        <div className="flex justify-center space-x-2">
          <button
            onClick={handleConfirm}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Confirm
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 text-black rounded-md hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
