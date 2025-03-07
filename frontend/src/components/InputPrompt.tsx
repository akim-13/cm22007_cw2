import { useState } from "react";
import { Check, Plus } from "lucide-react";

export default function InputPrompt({ setIsModalOpen }) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    console.log("Input submitted:", input);
    setInput(""); // Clear input after submission
  };

    const handleCreateEventClick = () => {
        setIsModalOpen(true);
    };

  return (
    <div className="flex items-center border-2 border-black rounded-3xl px-6 py-3 w-full">
      <div className="relative flex-grow">
        <input
          type="text"
          className="w-full outline-none bg-transparent text-lg px-2 pr-12 py-2"
          placeholder="Type your prompt..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full hover:bg-gray-200"
          onClick={handleSubmit}
        >
          <Check className="w-6 h-6" />
        </button>
      </div>
      <button onClick={handleCreateEventClick} className="ml-2 p-3 rounded-full hover:bg-gray-200">
        <Plus className="w-6 h-6" />
      </button>
    </div>
  );
}
