import React, { useState } from "react";

interface Achievement {
  id: number;
  title: string;
  description: string;
  date: string;
  completed: boolean;
}

interface AchievementModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const AchievementModal: React.FC<AchievementModalProps> = ({ isOpen, onClose }) => {
  // replace with actual achievement source
  const [achievements, setAchievements] = useState<Achievement[]>([
    {
      id: 1,
      title: "First Task Completed",
      description: "You completed your first calendar task",
      date: "2025-03-01",
      completed: true
    },
    {
      id: 2,
      title: "Weekly Streak",
      description: "Complete tasks for 7 consecutive days",
      date: "2025-03-02",
      completed: true
    },
    {
      id: 3,
      title: "Productivity Master",
      description: "Complete 10 tasks in a single day",
      date: "",
      completed: false
    },
    {
      id: 4,
      title: "Early Bird",
      description: "Complete a task before 9 AM",
      date: "",
      completed: false
    }
  ]);

  const [filter, setFilter] = useState<"all" | "completed" | "locked">("all");

  const filteredAchievements = achievements.filter(achievement => {
    if (filter === "all") return true;
    if (filter === "completed") return achievement.completed;
    if (filter === "locked") return !achievement.completed;
    return true;
  });

  if (!isOpen) return null;

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
              key={achievement.id} 
              style={{ 
                border: "1px solid #ccc", 
                borderRadius: "10px", 
                padding: "12px", 
                marginBottom: "10px",
                backgroundColor: achievement.completed ? "#f8f8f8" : "#f0f0f0"
              }}
            >
              <div>
                <div style={{ fontWeight: "bold" }}>
                  {achievement.title}
                  {achievement.completed ? " (Completed)" : " (Locked)"}
                </div>
                <div style={{ marginTop: "5px" }}>{achievement.description}</div>
                {achievement.completed && (
                  <div style={{ fontSize: "12px", color: "#666", marginTop: "5px" }}>
                    Unlocked on {achievement.date}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: "20px", textAlign: "center" }}>
          <div>
            You've completed {achievements.filter(a => a.completed).length} of {achievements.length} achievements
          </div>
        </div>
      </div>
    </div>
  );
};

export default AchievementModal;