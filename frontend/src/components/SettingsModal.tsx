import { useState } from "react";

interface SettingsModalProps {
  open: boolean;
  onClose: () => void;
}

export default function SettingsModal({ open, onClose }: SettingsModalProps) {
  const [calendarUrl, setCalendarUrl] = useState("");

  const handleConfirm = () => {
    console.log("Calendar URL:", calendarUrl);
    onClose();
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-center text-lg font-semibold mb-4">Settings</h2>
        <label className="block text-sm font-medium mb-2">
          Enter calendar:
        </label>
        <input
          type="url"
          placeholder="https://..."
          value={calendarUrl}
          onChange={(e) => setCalendarUrl(e.target.value)}
          className="border rounded-md p-2 w-full mb-4"
        />
        <div className="flex justify-center">
          <button
            onClick={handleConfirm}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
