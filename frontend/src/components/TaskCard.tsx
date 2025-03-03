import React, { useState } from 'react';

interface TaskCardProps {
  title: string;
  priority: 'high' | 'medium' | 'low';
  duration: string;
  deadline: string;
  description?: string;
  dropdown?: boolean;
  otherTasks?: string[];
}

const TaskCard: React.FC<TaskCardProps> = ({
  title,
  priority,
  duration,
  deadline,
  description = '',
  dropdown = false,
  otherTasks = []
}) => {
  const [isChecked, setIsChecked] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleCheckboxChange = () => {
    setIsChecked(!isChecked);
  };

  const priorityColor = priority === 'high' ? 'bg-red-600' : 
                        priority === 'medium' ? 'bg-orange-500' : 
                        'bg-green-500';

  return (
    <div className="border p-4 rounded-lg max-w-xs bg-gray-100 my-2">
      {/* Title & Buttons (Dropdown + Edit) */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className={`w-4 h-4 rounded ${priorityColor}`}></div>
          <h3 className="text-xl font-semibold text-black">{title}</h3>
        </div>
        <div className="flex space-x-2">
          <button className="bg-gray-100 text-black p-1 rounded">
            ✏️
          </button>
          {dropdown && (description || otherTasks.length > 0) && (
            <button 
              onClick={() => setIsExpanded(!isExpanded)} 
              className="bg-gray-100 text-black p-1 rounded"
            >
              {isExpanded ? '🔼' : '🔽'}
            </button>
          )}
        </div>
      </div>

      {/* Deadline */}
      <p className="text-black font-semibold">Deadline: {deadline}</p>

      {/* Duration */}
      <p className="text-black">Duration: {duration}</p>

      {/* Checkbox */}
      <input 
        type="checkbox" 
        checked={isChecked} 
        onChange={handleCheckboxChange} 
        className="mr-2"
      />
      <label className="text-black"> Mark as Completed</label>

      {/* Description & Sub-tasks (only show when expanded) */}
      {dropdown && isExpanded && (
        <div className="mt-2 border-t pt-2">
          {description && <p className="text-black mt-2">{description}</p>}
          {otherTasks.length > 0 && (
            <ul className="mt-2">
              {otherTasks.map((task, index) => (
                <li key={index} className="text-black pl-4 list-disc">
                  {task}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default TaskCard;
