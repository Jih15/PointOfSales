from dotenv import load_dotenv
load_dotenv()

from app.database.connection import SessionLocal, init_db
from app.http.models.user import User
from app.http.models.user_detail import UserDetail
from app.core.security.security import hash_password

def seed():
    init_db()
    db = SessionLocal()

    try: 
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print ("Admin already exist, skip.")
            return
        
        user = User(
            username  = "admin",
            email     = "admin@mail.com",
            password  = hash_password("Admin1234"),
            is_active = True,
        )

        db.add(user)
        db.flush()

        detail = UserDetail(
            id_user   = user.id_user,
            full_name = "Super Admin",
            gender    = "male",
            phone     = "08123456789",
            address   = "Kantor Pusat",
            role      = "admin",            
        )

        db.add(detail)
        db.commit()

        print("✅ Seed berhasil!")
        print("   username : admin")
        print("   password : Admin1234")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Gagal: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()