import React, { useState} from "react";
import axios from "axios";

const FetchButton: React.FC = () => {
  const [data, setData] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      console.log("Sending request to API...");
      const response = await axios.get("http://127.0.0.1:8000/");
      console.log("API Response:", response);
      setData(response.data.message);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch Data</button>
      {data && <p>Response: {data}</p>}
    </div>
  );
};

export default FetchButton;
