from database.dbsetup import SessionLocal
from database.models import Achievements

# Create a database session
db = SessionLocal()

# Query all achievements
achievements = db.query(Achievements).all()

# Print the number of achievements
print(f"Total achievements: {len(achievements)}")

# Print details of each achievement
for achievement in achievements:
    print(f"ID: {achievement.achievementID}")
    print(f"Title: {achievement.title}")
    print(f"Required Points: {achievement.requiredPoints}")
    print(f"Description: {achievement.description}")
    print("---")

# Close the database session
db.close()