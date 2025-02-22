import { useState } from "react";
import { Check, Plus } from "lucide-react";

export default function InputPrompt() {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    console.log("Input submitted:", input);
    setInput(""); // Clear input after submission
  };

  return (
    <div className="flex items-center border-2 border-black rounded-3xl px-6 py-3 w-full max-w-2xl">
      <input
        type="text"
        className="flex-grow outline-none bg-transparent text-lg w-full px-2"
        placeholder="Type your prompt..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button
        className="ml-3 p-3 rounded-full hover:bg-gray-200"
        onClick={handleSubmit}
      >
        <Check className="w-6 h-6" />
      </button>
      <button className="ml-2 p-3 rounded-full hover:bg-gray-200">
        <Plus className="w-6 h-6" />
      </button>
    </div>
  );
}
