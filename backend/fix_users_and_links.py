from app.core.database import SessionLocal
from app.models.user import User, Role
from app.models.personnel import Personnel
from app.core.security import get_password_hash

def fix_users():
    db = SessionLocal()
    try:
        # Roles
        role_admin = db.query(Role).filter(Role.name == "ADMIN").first()
        role_exec = db.query(Role).filter(Role.name == "EXECUTIVE").first()
        role_staff = db.query(Role).filter(Role.name == "STAFF").first()

        # Update or create users
        users_config = [
            {"username": "admin", "email": "admin@reru.ac.th", "role_id": role_admin.id, "pass": "admin123"},
            {"username": "executive", "email": "executive@reru.ac.th", "role_id": role_exec.id, "pass": "exec123"},
            {"username": "staff", "email": "staff@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
            {"username": "cheawchan.y", "email": "cheawchan.y@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
            {"username": "nithit.w", "email": "nithit.w@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
            {"username": "theeraphon.s", "email": "theeraphon.s@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
            {"username": "pramool.s", "email": "pramool.s@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
            {"username": "somchai.s", "email": "somchai.s@reru.ac.th", "role_id": role_staff.id, "pass": "staff123"},
        ]

        for u_cfg in users_config:
            u = db.query(User).filter(User.username == u_cfg["username"]).first()
            if not u:
                u = User(
                    username=u_cfg["username"],
                    email=u_cfg["email"],
                    password_hash=get_password_hash(u_cfg["pass"]),
                    role_id=u_cfg["role_id"],
                    is_active=True
                )
                db.add(u)
                db.flush()
                print(f"Created user: {u.username}")
            else:
                u.password_hash = get_password_hash(u_cfg["pass"])
                u.role_id = u_cfg["role_id"]
                u.is_active = True
                print(f"Updated user: {u.username}")

        db.commit()

        # Link personnel to user
        # Link ID 1 (ผศ.เชี่ยวชาญ) to 'staff' and 'cheawchan.y'
        p1 = db.query(Personnel).filter(Personnel.id == 1).first()
        staff_u = db.query(User).filter(User.username == "staff").first()
        if p1 and staff_u:
            p1.user_id = staff_u.id
            db.commit()
            print(f"Linked Personnel ID 1 ({p1.prefix_th}{p1.first_name_th}) to user '{staff_u.username}' (ID {staff_u.id})")

        p2 = db.query(Personnel).filter(Personnel.id == 2).first()
        nithit_u = db.query(User).filter(User.username == "nithit.w").first()
        if p2 and nithit_u:
            p2.user_id = nithit_u.id
            db.commit()
            print(f"Linked Personnel ID 2 ({p2.prefix_th}{p2.first_name_th}) to user '{nithit_u.username}' (ID {nithit_u.id})")

        p3 = db.query(Personnel).filter(Personnel.id == 3).first()
        theeraphon_u = db.query(User).filter(User.username == "theeraphon.s").first()
        if p3 and theeraphon_u:
            p3.user_id = theeraphon_u.id
            db.commit()
            print(f"Linked Personnel ID 3 to user '{theeraphon_u.username}'")

        p4 = db.query(Personnel).filter(Personnel.id == 4).first()
        pramool_u = db.query(User).filter(User.username == "pramool.s").first()
        if p4 and pramool_u:
            p4.user_id = pramool_u.id
            db.commit()
            print(f"Linked Personnel ID 4 to user '{pramool_u.username}'")

        print("Finished fixing users and personnel links.")
    except Exception as e:
        db.rollback()
        print("Error fixing users:", e)
    finally:
        db.close()

if __name__ == "__main__":
    fix_users()
