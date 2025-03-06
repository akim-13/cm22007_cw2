import React, { useState, useEffect } from "react";
import axios from "axios";

interface Achievement {
  achievementID: number;
  title: string;
  description: string;
  requiredPoints: number;
  image_path: string;
}

interface AchievementModalProps {
  isOpen: boolean;
  onClose: () => void;
  username?: string; // Optional username prop
}

const AchievementModal: React.FC<AchievementModalProps> = ({ 
  isOpen, 
  onClose, 
  username = "joe" // Default username for testing
}) => {
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [userAchievements, setUserAchievements] = useState<number[]>([]);
  const [filter, setFilter] = useState<"all" | "completed" | "locked">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      fetchAchievements();
      fetchUserAchievements();
    }
  }, [isOpen, username]);

  const fetchAchievements = async () => {
    try {
      const response = await axios.get('http://localhost:8000/check_achievements');
      setAchievements(response.data);
    } catch (error) {
      console.error("Error fetching achievements:", error);
    }
  };
  
  const fetchUserAchievements = async () => {
    try {
      console.log("Fetching achievements for user:", username); // Debugging output
      const response = await axios.get(`http://localhost:8000/get_achievements_from_user/${username}`);
      const userAchievementIds = response.data.achievements.map((ach: any) => ach.achievementID);
      setUserAchievements(userAchievementIds);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching user achievements:", error);
      setLoading(false);
    }
  };

  const filteredAchievements = achievements.map(achievement => ({
    ...achievement,
    completed: userAchievements.includes(achievement.achievementID)
  })).filter(achievement => {
    if (filter === "all") return true;
    if (filter === "completed") return achievement.completed;
    if (filter === "locked") return !achievement.completed;
    return true;
  });

  if (!isOpen) return null;

  if (loading) {
    return (
      <div style={{ 
        position: "fixed", 
        top: 0, 
        left: 0, 
        right: 0, 
        bottom: 0, 
        backgroundColor: "rgba(0,0,0,0.5)", 
        display: "flex", 
        justifyContent: "center", 
        alignItems: "center", 
        zIndex: 1000 
      }}>
        <div>Loading achievements...</div>
      </div>
    );
  }

  return (
    <div style={{ 
      position: "fixed", 
      top: 0, 
      left: 0, 
      right: 0, 
      bottom: 0, 
      backgroundColor: "rgba(0,0,0,0.5)", 
      display: "flex", 
      justifyContent: "center", 
      alignItems: "center", 
      zIndex: 1000 
    }}>
      <div style={{ 
        backgroundColor: "white", 
        padding: "20px", 
        borderRadius: "10px", 
        width: "100%", 
        maxWidth: "500px", 
        maxHeight: "80vh", 
        overflow: "auto" 
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "15px" }}>
          <h2 style={{ margin: 0 }}>Achievements</h2>
          <button 
            onClick={onClose} 
            style={{ 
              background: "none", 
              border: "none", 
              cursor: "pointer", 
              fontSize: "16px" 
            }}
          >
            ✕
          </button>
        </div>

        <div style={{ marginBottom: "15px" }}>
          <button 
            onClick={() => setFilter("all")} 
            style={{ 
              marginRight: "10px", 
              padding: "5px 10px", 
              background: filter === "all" ? "#ddd" : "#f0f0f0", 
              border: "1px solid #ccc", 
              borderRadius: "8px", 
              cursor: "pointer"
            }}
          >
            All
          </button>
          <button 
            onClick={() => setFilter("completed")} 
            style={{ 
              marginRight: "10px", 
              padding: "5px 10px", 
              background: filter === "completed" ? "#ddd" : "#f0f0f0", 
              border: "1px solid #ccc", 
              borderRadius: "8px",
              cursor: "pointer" 
            }}
          >
            Completed
          </button>
          <button 
            onClick={() => setFilter("locked")} 
            style={{ 
              padding: "5px 10px", 
              background: filter === "locked" ? "#ddd" : "#f0f0f0", 
              border: "1px solid #ccc", 
              borderRadius: "8px",
              cursor: "pointer" 
            }}
          >
            Locked
          </button>
        </div>

        <div>
          {filteredAchievements.map(achievement => (
            <div 
              key={achievement.achievementID} 
              style={{ 
                border: "1px solid #ccc", 
                borderRadius: "10px", 
                padding: "12px", 
                marginBottom: "10px",
                backgroundColor: achievement.completed ? "#f8f8f8" : "#f0f0f0",
                display: "flex",
                alignItems: "center"
              }}
            >
              {achievement.image_path && (
                <img 
                  src={`/static/${achievement.image_path}`} 
                  alt={achievement.title} 
                  style={{ 
                    width: "50px", 
                    height: "50px", 
                    marginRight: "15px",
                    opacity: achievement.completed ? 1 : 0.3
                  }} 
                />
              )}
              <div>
                <div style={{ fontWeight: "bold" }}>
                  {achievement.title}
                  {achievement.completed ? " (Completed)" : ` (Locked - ${achievement.requiredPoints} points)`}
                </div>
                <div style={{ marginTop: "5px" }}>{achievement.description}</div>
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <div>
            You've completed {filteredAchievements.filter(a => a.completed).length} of {filteredAchievements.length} achievements
          </div>
        </div>
      </div>
    </div>
  );
};

export default AchievementModal;