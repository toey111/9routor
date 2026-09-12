import os
from app.core.database import SessionLocal
from app.models.personnel import Personnel

def update_avatars():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <linearGradient id="userGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e2e8f0"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="32" fill="url(#bgGrad)"/>
  <circle cx="100" cy="75" r="36" fill="url(#userGrad)"/>
  <path d="M100 124 C62 124 34 154 32 196 C32 198 34 200 36 200 L164 200 C166 200 168 198 168 196 C166 154 138 124 100 124 Z" fill="url(#userGrad)"/>
</svg>"""

    os.makedirs("/app/uploads/avatars", exist_ok=True)
    with open("/app/uploads/avatars/default_white.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Wrote /app/uploads/avatars/default_white.svg")

    db = SessionLocal()
    try:
        personnel_list = db.query(Personnel).all()
        for p in personnel_list:
            p.avatar_url = "images/default-avatar-white.svg"
        db.commit()
        print(f"Updated all {len(personnel_list)} personnel avatar_url to 'images/default-avatar-white.svg'")
    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    update_avatars()
