import { useState } from "react";
import { Check, Plus } from "lucide-react";

export default function InputPrompt() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState(null);

<<<<<<< Updated upstream
  const handleSubmit = () => {
    alert(`Input: ${input}`); // Displays the input string
    console.log("Input submitted:", input);
    setInput(""); // Clear input after submission
    return input;
=======
  const handleSubmit = async () => {
    if (!input.trim()) return;

    try {
      const username = "joe";
      const res = await fetch(
        `http://localhost:8000/autofill/${username}?description=${encodeURIComponent(
          input
        )}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch data");
      }

      const data = await res.json();
      setResponse(data);
      console.log("AI Response:", data);
    } catch (error) {
      console.error("Error:", error);
    }

    setInput("");
>>>>>>> Stashed changes
  };

  return (
    <div className="flex flex-col w-full">
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
        <button className="ml-2 p-3 rounded-full hover:bg-gray-200">
          <Plus className="w-6 h-6" />
        </button>
      </div>

      {/* Display AI-generated response */}
      {response && (
        <div className="mt-4 p-4 border rounded-lg bg-gray-100">
          <h3 className="text-lg font-semibold">AI Suggestions:</h3>
          <pre className="whitespace-pre-wrap">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
