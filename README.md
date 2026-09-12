# ระบบจัดเก็บข้อมูลบุคลากร คณะเทคโนโลยีสารสนเทศ มหาวิทยาลัยราชภัฏร้อยเอ็ด
**Faculty Personnel Management System (RERU IT)**

---

## ภาพรวมของระบบ (Project Overview)
Web Application สำหรับการบริหารจัดการ บันทึก ค้นหา รายงาน และประมวลผลสถิติข้อมูลบุคลากรของคณะเทคโนโลยีสารสนเทศ มหาวิทยาลัยราชภัฏร้อยเอ็ด รองรับการกำหนดสิทธิ์ผู้ใช้งานแบบ Role-Based Access Control (RBAC), RESTful API, Database Normalization, การส่งออกรายงาน (Excel/CSV/PDF) และทำงานผ่าน Docker Container

---

## สถาปัตยกรรมเทคโนโลยี (Tech Stack)
- **Frontend**: HTML5, CSS3, JavaScript (Modular ES), Tailwind CSS, Lucide Icons, Chart.js
- **Backend**: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy ORM, Passlib (Bcrypt), Python-JOSE (JWT)
- **Database**: MySQL 8.0 (`utf8mb4_unicode_ci`) พร้อม Foreign Keys & Indexing
- **Infrastructure**: Docker & Docker Compose (4 Services: `frontend`, `backend`, `mysql`, `phpmyadmin`)

---

## บัญชีผู้ใช้งานเริ่มต้นสำหรับทดสอบ (Demo Accounts)

| บทบาท (Role) | บัญชีผู้ใช้ (Username) | รหัสผ่าน (Password) | สิทธิ์การใช้งานหลัก |
| :--- | :--- | :--- | :--- |
| **ผู้ดูแลระบบ (ADMIN)** | `admin` | `admin123` | สิทธิ์สูงสุด CRUD ทุกข้อมูล, Master Data, Audit Logs, Users |
| **ผู้บริหาร (EXECUTIVE)** | `executive` | `exec123` | ดู Dashboard, กราฟสถิติ, ค้นหาบุคลากร, Export รายงาน |
| **บุคลากร (STAFF)** | `somchai.s` | `staff123` | ดูและแก้ไขข้อมูลประวัติตนเอง, อัปโหลด Avatar, เปลี่ยนรหัสผ่าน |

---

## ขั้นตอนการติดตั้งและรันระบบผ่าน Docker (Installation & Running)

### 1. คัดลอกไฟล์ Environment
```bash
cp .env.example .env
```

### 2. สั่งรัน Docker Compose
```bash
docker compose up -d --build
```

### 3. ตรวจสอบการทำงานของแต่ละเซอร์วิส
- **Frontend Web Application**: [http://localhost:3000](http://localhost:3000) (หรือ [http://localhost:80](http://localhost:80))
- **Backend REST API (FastAPI Docs)**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **phpMyAdmin (Database Management)**: [http://localhost:8080](http://localhost:8080)
  - Server: `mysql`
  - User: `root`
  - Password: `root_password_123` (หรือ user: `personnel_user` / pass: `personnel_pass123`)

---

## วิธีใช้งานระบบ (How to Use)

### 1. เริ่มระบบ
หลังจากทำตามขั้นตอนติดตั้งแล้ว ให้รันคำสั่งต่อไปนี้จาก root ของโปรเจ็กต์:

```bash
docker compose up -d --build
```

หากต้องการดู logs แบบ realtime:

```bash
docker compose logs -f
```

### 2. เข้าใช้งานหน้าเว็บ
เปิดเบราว์เซอร์แล้วไปที่:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API Docs: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- phpMyAdmin: [http://localhost:8080](http://localhost:8080)

### 3. เข้าสู่ระบบ
ใช้บัญชีทดสอบดังนี้:

| บทบาท | Username | Password |
| :--- | :--- | :--- |
| Admin | `admin` | `admin123` |
| Executive | `executive` | `exec123` |
| Staff | `somchai.s` | `staff123` |

หลังจากเข้าสู่ระบบแล้ว ผู้ใช้แต่ละบทบาทจะเห็นเมนูและสิทธิ์การเข้าถึงที่ต่างกันดังนี้:

- Admin: จัดการข้อมูลหลัก, ผู้ใช้งาน, Audit Logs, Dashboard, Reports
- Executive: ดู Dashboard, สถิติ, ค้นหาบุคลากร, Export รายงาน
- Staff: ดูข้อมูลประวัติตนเอง, อัปโหลด Avatar, เปลี่ยนรหัสผ่าน

### 4. การใช้งานพื้นฐาน

#### หน้า Dashboard
- ตรวจสอบสถิติเฉพาะบทบาทที่อนุญาต
- ดูจำนวนบุคลากร, สาขา, ตำแหน่ง, และข้อมูลสรุปอื่น ๆ

#### หน้า Personnel
- ค้นหาและเรียกดูข้อมูลบุคลากร
- เพิ่ม/แก้ไข/ลบข้อมูลบุคลากร (เฉพาะ Admin หรือผู้มีสิทธิ์ตามเงื่อนไข)
- อัปโหลดภาพประจำตัวหรือเอกสารที่เกี่ยวข้อง

#### หน้า Master Data
- เพิ่ม/จัดการ Departments, Branches, Positions, Personnel Types, Expertise
- ใช้ได้กับผู้มีสิทธิ์ Admin เท่านั้น

#### หน้า Reports
- ส่งออกข้อมูลเป็น Excel / CSV / PDF
- รองรับบทบาท Admin และ Executive

### 5. การหยุดและล้างระบบ

หยุด Container:

```bash
docker compose down
```

หยุดแล้วลบ volume ทั้งหมด (รวมข้อมูล MySQL):

```bash
docker compose down -v
```

---

## วิธีทดสอบระบบ (System Testing Guide)

### 1. ทดสอบการทำงานของ Container
ก่อนใช้งานจริง ให้ตรวจสอบว่า services ทุกตัวทำงานได้ตามปกติ:

```bash
docker compose ps
```

ผลที่คาดหวัง:

- `reru_it_mysql` → Running
- `reru_it_backend` → Running
- `reru_it_frontend` → Running
- `reru_it_phpmyadmin` → Running

หาก service ใดไม่ทำงาน ให้ดู log:

```bash
docker compose logs <service-name>
```

ตัวอย่าง:

```bash
docker compose logs backend
docker compose logs mysql
```

### 2. ทดสอบ Health Check ของ Backend
เปิด URL ต่อไปนี้เพื่อตรวจสอบว่า API ยัง Online:

- [http://localhost:8000/health](http://localhost:8000/health)
- [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

ผลที่คาดหวัง:

```json
{"status": "healthy"}
```

### 3. ทดสอบ Login
ใช้ API login ด้านล่างเพื่อยืนยันว่า JWT ทำงานได้:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

ผลที่คาดหวัง:
- API ต้องคืน `access_token`
- ใช้ token ที่ได้ไปเรียก API อื่นต่อไป

### 4. ทดสอบการเข้าถึง API ตาม Role
#### Admin
```bash
curl -X GET http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Executive
```bash
curl -X GET http://localhost:8000/api/v1/dashboard/stats \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Staff
```bash
curl -X GET http://localhost:8000/api/v1/personnel \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

ผลที่คาดหวัง:
- Admin สามารถเข้าถึง Users, Master Data, Audit Logs ได้
- Executive สามารถเข้าถึง Dashboard, Reports ได้ แต่ไม่สามารถจัดการ Users ได้
- Staff สามารถดูข้อมูลส่วนตัวได้ และไม่สามารถเข้าถึงข้อมูลระบบระดับจัดการได้

### 5. ทดสอบ Frontend Flow แบบ Manual
ทำตามลำดับต่อไปนี้:

1. เปิด [http://localhost:3000](http://localhost:3000)
2. เข้าสู่ระบบด้วยบัญชี `admin`
3. ตรวจสอบว่ามีเมนู Dashboard, Personnel, Master Data, Reports, Users
4. ไปที่ Personnel → เพิ่มข้อมูลบุคลากรใหม่
5. ตรวจสอบว่าข้อมูลปรากฏบนหน้า Personnel
6. ไปที่ Reports → ส่งออกไฟล์ Excel/CSV/PDF
7. ลงชื่อออกจากระบบแล้วลองเข้าสู่ระบบด้วยบัญชี `executive` หรือ `somchai.s`
8. ตรวจสอบว่ามีสิทธิ์เข้าถึงตามบทบาทจริง

### 6. ทดสอบการอัปโหลดไฟล์
ในหน้า Personnel หรือ Profile ให้ทำการอัปโหลด Avatar หรือไฟล์เอกสารที่รองรับ

สิ่งที่ควรตรวจสอบ:

- ไฟล์ถูกบันทึกลง folder `backend/uploads`
- ระบบเปลี่ยนชื่อไฟล์ให้ปลอดภัยแบบ UUID
- ไฟล์มีขนาดไม่เกิน 10MB
- ไฟล์ผิดชนิดจะถูกปฏิเสธโดยระบบ

### 7. ทดสอบการ Export รายงาน
เป็นการตรวจสอบการสร้างไฟล์รายงานจากระบบ:

- ดึง Dashboard Stats จาก API
- เข้าไปที่เมนู Reports และเลือก Export
- ตรวจสอบว่าไฟล์ดาวน์โหลดสำเร็จ
- เปิดไฟล์เพื่อตรวจสอบรูปแบบข้อมูลและคอลัมน์

### 8. ตัวอย่าง Checklist สำหรับ QA

- [ ] Container ทั้งหมด Running
- [ ] Backend Health Check คืน `healthy`
- [ ] Login ด้วย admin สำเร็จ
- [ ] Login ด้วย executive สำเร็จ
- [ ] Login ด้วย staff สำเร็จ
- [ ] Dashboard แสดงข้อมูลตามบทบาท
- [ ] Personnel search และ list ทำงาน
- [ ] เพิ่มบุคลากรสำเร็จ
- [ ] Export รายงานทำงาน
- [ ] อัปโหลดไฟล์ทำงาน
- [ ] RBAC ปฏิเสธการเข้าถึงที่ไม่ได้รับอนุญาต

### 9. หมายเหตุเกี่ยวกับ Automated Test
ในรอบนี้โครงการยังไม่มีชุด Automated Test ที่จัดเตรียมไว้ใน repository อย่างเป็นทางการ แต่สามารถทดสอบระบบได้ผ่าน workflow ดังกล่าวด้านบน (Manual Smoke Test / API Smoke Test)

หากต้องการเพิ่ม Automated Test ในภายหลัง สามารถใช้ `pytest` ร่วมกับ `TestClient` ของ FastAPI เพื่อทำการทดสอบ endpoint และ role-based access ได้ทันที

---

## โครงสร้างโฟลเดอร์โครงการ (Project Structure)

```
d:/9router/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── personnel.py
│   │   │   │   ├── academic.py
│   │   │   │   ├── master_data.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── audit_logs.py
│   │   │   │   └── users.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── audit_service.py
│   │   │   ├── export_service.py
│   │   │   └── file_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── personnel-list.html
│   ├── personnel-detail.html
│   ├── personnel-form.html
│   ├── master-data.html
│   ├── audit-logs.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── ui.js
│   │   └── components.js
│   ├── nginx.conf
│   └── Dockerfile
│
├── database/
│   ├── init.sql
│   └── seed_data.sql
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## มาตรการความปลอดภัย (Security Features)
- **SQL Injection Prevention**: ใช้ SQLAlchemy ORM Parameterized Binding ในทุก Query
- **XSS & Content Protection**: Escaping ข้อมูลและการจัดการ DOM ปลอดภัย
- **RBAC API Guards**: ตรวจสอบ Header `Bearer JWT` และระดับสิทธิ์ทุก Endpoint
- **Data Privacy**: Mask เลขประจำตัวประชาชน (เช่น `1-45XX-XXXXX-XX-X`) สำหรับผู้ที่ไม่มีสิทธิ์เข้าถึง
- **File Upload Protection**: ตรวจสอบนามสกุลไฟล์, MIME type, ขนาดไฟล์จำกัด 10MB และเปลี่ยนชื่อไฟล์แบบสุ่ม UUID ป้องกัน Path Traversal
