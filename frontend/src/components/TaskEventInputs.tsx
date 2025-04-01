import React from "react";

interface InputProps {
  value: any;
  onChange: (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => void;
}

interface ModeToggleButtonProps {
  mode: "task" | "event";
  isActive: boolean;
  setIsTaskMode: (value: boolean) => void;
}

export const ModeToggleButton: React.FC<ModeToggleButtonProps> = ({ mode, isActive, setIsTaskMode }) => {
  return (
    <label className="flex items-center cursor-pointer">
      <input
        name="mode"
        type="radio"
        value={mode}
        checked={isActive}
        onChange={() => setIsTaskMode(mode === "task")}
        className="hidden"
      />
      <span className={`px-4 py-2 rounded ${isActive ? "bg-blue-500 text-white" : "bg-gray-300 text-black"}`}>
        {mode === "task" ? "Task" : "Event"}
      </span>
    </label>
  );
};

export const TitleInput: React.FC<InputProps & { isTaskMode: boolean }> = ({ value, onChange, isTaskMode }) => (
  <input
    name="title"
    type="text"
    placeholder={isTaskMode ? "Task Title" : "Event Title"}
    value={value}
    onChange={onChange}
    required
    className="border p-2 rounded w-full mt-2"
  />
);

export const StartDateInput: React.FC<InputProps> = ({ value, onChange, isTaskMode }) => (
  <input
    name="start"
    type={value ? "datetime-local" : "text"}
    onFocus={(e) => (e.target.type = "datetime-local")}
    placeholder={isTaskMode ? "Deadline" : "Start Date"}
    value={value}
    onChange={onChange}
    required
    className="border p-2 rounded w-full mt-2"
  />
);

export const EndDateInput: React.FC<InputProps> = ({ value, onChange }) => (
  <input
    name="end"
    type={value ? "datetime-local" : "text"}
    onFocus={(e) => (e.target.type = "datetime-local")}
    placeholder="End Date"
    value={value}
    onChange={onChange}
    required
    className="border p-2 rounded w-full mt-2"
  />
);

export const DurationInput: React.FC<InputProps> = ({ value, onChange }) => (
  <input
    name="duration"
    type="number"
    placeholder="Estimated Duration (Minutes)"
    value={value}
    onChange={onChange}
    className="border p-2 rounded w-full mt-2"
    required
  />
);

export const PrioritySelect: React.FC<InputProps> = ({ value, onChange }) => (
  <select
    name="priority"
    value={value}
    onChange={onChange}
    className="border p-2 rounded w-full mt-2"
  >
    <option value="1">Low Priority</option>
    <option value="2">Medium Priority</option>
    <option value="3">High Priority</option>
  </select>
);

export const DescriptionInput: React.FC<InputProps> = ({ value, onChange }) => (
  <textarea
    name="description"
    placeholder="Description"
    value={value}
    onChange={onChange}
    className="border p-2 rounded w-full mt-2"
  />
);

export const CompletedCheckbox: React.FC<{ checked: boolean; onChange: (event: React.ChangeEvent<HTMLInputElement>) => void }> = ({ checked, onChange }) => (
  <label className="flex items-center mt-2 text-black">
    <input
      name="isCompleted"
      type="checkbox"
      checked={checked}
      onChange={onChange}
      className="mr-2"
    />
    Mark as Completed
  </label>
);
