import sys
import os
from datetime import date

from app.core.database import SessionLocal
from app.models.personnel import Personnel
from app.models.academic import (
    EducationHistory,
    WorkExperience,
    AcademicPosition,
    Research,
    Publication,
    Training
)
from app.models.master_data import Department, Branch, Position, PersonnelType, Expertise
from app.models.user import User

def seed_faculty_data():
    db = SessionLocal()
    try:
        print("Starting real faculty data import from IT2566.pdf...")

        # 1. Clear existing dummy personnel records and their child data
        existing_personnel = db.query(Personnel).all()
        for p in existing_personnel:
            db.delete(p)
        db.commit()
        print(f"Cleared {len(existing_personnel)} old dummy personnel records.")

        # Ensure branches exist
        it_branch = db.query(Branch).filter(Branch.name.like("%เทคโนโลยีสารสนเทศ%")).first()
        branch_id = it_branch.id if it_branch else 2

        dept = db.query(Department).filter(Department.name.like("%คณะเทคโนโลยีสารสนเทศ%")).first()
        dept_id = dept.id if dept else 1

        pos_lecturer = db.query(Position).filter(Position.name == "อาจารย์ผู้สอน").first()
        pos_head = db.query(Position).filter(Position.name == "หัวหน้าสาขาวิชา").first()
        pos_lecturer_id = pos_lecturer.id if pos_lecturer else 1
        pos_head_id = pos_head.id if pos_head else 2

        pt_academic = db.query(PersonnelType).filter(PersonnelType.name.like("%สายวิชาการ%")).first()
        pt_academic_id = pt_academic.id if pt_academic else 2
        pt_special = db.query(PersonnelType).filter(PersonnelType.name.like("%พนักงานราชการ%")).first()
        pt_special_id = pt_special.id if pt_special else 4

        # Query all expertise objects for linking
        all_exp = {e.name: e for e in db.query(Expertise).all()}

        # 2. Define real faculty data from PDF
        teachers_data = [
            {
                "code": "IT-256601",
                "prefix_th": "ผศ.",
                "first_name_th": "เชี่ยวชาญ",
                "last_name_th": "ยางศิลา",
                "prefix_en": "Asst. Prof.",
                "first_name_en": "Cheawchan",
                "last_name_en": "Yangsila",
                "citizen_id": "3451000589123",
                "birth_date": date(1980, 5, 14),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_head_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2007, 6, 1),
                "appoint_date": date(2015, 8, 15),
                "email": "cheawchan.y@reru.ac.th",
                "phone": "081-789-2345",
                "internal_phone": "401",
                "address": "101 หมู่ 12 ถ.ร้อยเอ็ด-วาปีปทุม ต.เกาะแก้ว อ.เสลภูมิ จ.ร้อยเอ็ด 45120",
                "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Internet of Things (IoT) & Embedded Systems", "Web & Mobile Application Development", "Cyber Security & Network Defense"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "วิทยาการคอมพิวเตอร์", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2549},
                    {"level": "ปริญญาตรี", "name": "ค.บ.", "field": "คอมพิวเตอร์ศึกษา", "inst": "สถาบันราชภัฏบุรีรัมย์", "year": 2544}
                ],
                "academic_positions": [
                    {"title": "ผู้ช่วยศาสตราจารย์ สาขาวิชาวิทยาการคอมพิวเตอร์", "order": "มรภ.รอ. 112/2558", "date": date(2015, 8, 15)}
                ],
                "researches": [
                    {
                        "title": "ระบบแจ้งเตือนการโจรกรรมรถยนต์และระบบติดตามรถยนต์ต้นทุนต่ำผ่านโทรศัพท์มือถือโดยใช้ GPS, GSM, Arduino และ FCM",
                        "type": "วิจัยประยุกต์",
                        "year": 2562,
                        "funding": "กองทุนวิจัย มหาวิทยาลัยราชภัฏร้อยเอ็ด",
                        "budget": 120000.0,
                        "url": "https://cheawchan.reru.ac.th/~it/images/major/IT2566.pdf"
                    }
                ],
                "publications": [
                    {
                        "title": "ระบบแจ้งเตือนการโจรกรรมรถยนต์และระบบติดตามรถยนต์ต้นทุนต่ำผ่านโทรศัพท์มือถือโดยใช้จีพีเอส, จีเอสเอ็ม, อาดูโน่ และเอฟซีเอ็ม",
                        "authors": "เชี่ยวชาญ ยางศิลา",
                        "journal": "วารสารวิชาการวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยราชภัฏนครสวรรค์ (TCI กลุ่มที่ 1)",
                        "year": 2562,
                        "volume": "11(13)",
                        "pages": "15-30",
                        "url": "https://ph01.tci-thaijo.org/index.php/nsruresearch"
                    }
                ],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2007, 6, 1), "end": None, "desc": "จัดการเรียนการสอนและพัฒนานวัตกรรม IoT"},
                    {"pos": "ประธานหลักสูตรวิทยาศาสตรบัณฑิต (เทคโนโลยีสารสนเทศ)", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2018, 1, 1), "end": None, "desc": "บริหารจัดการหลักสูตร มคอ.2 และงานประกันคุณภาพการศึกษา"}
                ],
                "trainings": [
                    {"course": "การพัฒนา Internet of Things และ Embedded AI สู่ภาคอุตสาหกรรม", "org": "สำนักงานนวัตกรรมแห่งชาติ (NIA)", "start": date(2023, 3, 10), "end": date(2023, 3, 12), "hours": 18, "loc": "ออนไลน์ Zoom"}
                ]
            },
            {
                "code": "IT-256602",
                "prefix_th": "ผศ.ดร.",
                "first_name_th": "นิธิศ",
                "last_name_th": "วังโน",
                "prefix_en": "Asst. Prof. Dr.",
                "first_name_en": "Nithit",
                "last_name_en": "Wangno",
                "citizen_id": "3451000508472",
                "birth_date": date(1981, 9, 20),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2008, 5, 1),
                "appoint_date": date(2017, 3, 20),
                "email": "nithit.w@reru.ac.th",
                "phone": "086-456-7890",
                "internal_phone": "402",
                "address": "250 ถ.เทวาภิบาล ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Computer Vision & Image Processing", "Artificial Intelligence & Machine Learning", "Data Science & Big Data"],
                "educations": [
                    {"level": "ปริญญาเอก", "name": "ปร.ด.", "field": "เทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2563},
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "เทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2552},
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "วิทยาการคอมพิวเตอร์", "inst": "สถาบันราชภัฏเพชรบุรีวิทยาลงกรณ์ (ในพระบรมราชูปถัมภ์)", "year": 2545}
                ],
                "academic_positions": [
                    {"title": "ผู้ช่วยศาสตราจารย์ สาขาวิชาเทคโนโลยีสารสนเทศ", "order": "มรภ.รอ. 045/2560", "date": date(2017, 3, 20)}
                ],
                "researches": [
                    {
                        "title": "การประมวลผลภาพถ่ายดิจิทัลเพื่อกำจัดหมอกควันด้วยเทคนิคไฮบริดสำหรับระบบเฝ้าระวังอัจฉริยะ",
                        "type": "วิจัยพื้นฐาน",
                        "year": 2563,
                        "funding": "สำนักงานคณะกรรมการส่งเสริมวิทยาศาสตร์ วิจัยและนวัตกรรม (สกสว.)",
                        "budget": 250000.0,
                        "url": None
                    }
                ],
                "publications": [
                    {
                        "title": "Hybrid Algorithm of Dark Chanel Prior and Guided filter for Single Image Dehazing",
                        "authors": "WangNo, N., & Pichai, S.",
                        "journal": "Creative Science",
                        "year": 2563,
                        "volume": "12(2)",
                        "pages": "182–189",
                        "url": "https://ph01.tci-thaijo.org/index.php/csj"
                    }
                ],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2008, 5, 1), "end": None, "desc": "สอนด้าน Image Processing, Computer Vision และ AI"}
                ],
                "trainings": [
                    {"course": "Advanced Deep Learning for Computer Vision", "org": "NECTEC", "start": date(2023, 7, 5), "end": date(2023, 7, 7), "hours": 20, "loc": "กรุงเทพมหานคร"}
                ]
            },
            {
                "code": "IT-256603",
                "prefix_th": "ดร.",
                "first_name_th": "ธีรพล",
                "last_name_th": "สืบชมภู",
                "prefix_en": "Dr.",
                "first_name_en": "Theeraphon",
                "last_name_en": "Suebchomphu",
                "citizen_id": "3451000701984",
                "birth_date": date(1982, 11, 8),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2009, 6, 1),
                "appoint_date": date(2009, 6, 1),
                "email": "theeraphon.s@reru.ac.th",
                "phone": "089-123-4567",
                "internal_phone": "403",
                "address": "45/1 ถ.สุริยเดชบำรุง ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Web & Mobile Application Development", "Database Management Systems", "Software Engineering & Agile"],
                "educations": [
                    {"level": "ปริญญาเอก", "name": "ปร.ด.", "field": "สารสนเทศศึกษา", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2560},
                    {"level": "ปริญญาโท", "name": "ค.อ.ม.", "field": "คอมพิวเตอร์และเทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี", "year": 2548},
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "วิทยาการคอมพิวเตอร์", "inst": "สถาบันราชภัฏรำไพพรรณี", "year": 2546}
                ],
                "academic_positions": [],
                "researches": [
                    {
                        "title": "การพัฒนาแอปพลิเคชันเส้นทางศึกษาธรรมชาติป่าชุมชนเฉลิมพระเกียรติป่าโคกท่าสีและป่าชุมชนบ้านหนองเม็ก",
                        "type": "วิจัยและพัฒนา",
                        "year": 2565,
                        "funding": "สำนักงานการวิจัยแห่งชาติ (วช.)",
                        "budget": 350000.0,
                        "url": None
                    }
                ],
                "publications": [
                    {
                        "title": "การพัฒนาแอปพลิเคชันเส้นทางศึกษาธรรมชาติป่าชุมชนเฉลิมพระเกียรติป่าโคกท่าสีและป่าชุมชนบ้านหนองเม็ก",
                        "authors": "ธีรพล สืบชมภู และ ประมูล สุขสกาวผ่อง",
                        "journal": "วารสารวิชาการการประยุกต์ใช้เทคโนโลยีสารสนเทศ มหาวิทยาลัยราชภัฏมหาสารคาม",
                        "year": 2565,
                        "volume": "8(1)",
                        "pages": "44-54",
                        "url": "https://ph02.tci-thaijo.org/index.php/jait"
                    }
                ],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2009, 6, 1), "end": None, "desc": "สอนและวิจัยด้านสารสนเทศศาสตร์และการพัฒนาโมบายแอปพลิเคชัน"}
                ],
                "trainings": [
                    {"course": "Cross-Platform Mobile App Development with Flutter", "org": "DEPA", "start": date(2023, 5, 20), "end": date(2023, 5, 22), "hours": 18, "loc": "ออนไลน์"}
                ]
            },
            {
                "code": "IT-256604",
                "prefix_th": "ดร.",
                "first_name_th": "ประมูล",
                "last_name_th": "สุขสกาวผ่อง",
                "prefix_en": "Dr.",
                "first_name_en": "Pramool",
                "last_name_en": "Suksakaophong",
                "citizen_id": "3860500049281",
                "birth_date": date(1978, 3, 12),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2006, 8, 1),
                "appoint_date": date(2006, 8, 1),
                "email": "pramool.s@reru.ac.th",
                "phone": "081-345-6789",
                "internal_phone": "404",
                "address": "88/2 หมู่ 5 ต.เหนือเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Data Science & Big Data", "Database Management Systems", "Cloud Computing & DevOps"],
                "educations": [
                    {"level": "ปริญญาเอก", "name": "ปร.ด.", "field": "เทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "year": 2562},
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "เทคโนโลยีสารสนเทศ", "inst": "สถาบันเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "year": 2545},
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "การบริหารการบิน", "inst": "มหาวิทยาลัยอีสเทิร์นเอเชีย", "year": 2550},
                    {"level": "ปริญญาตรี", "name": "ค.อ.บ.", "field": "เทคโนโลยีคอมพิวเตอร์", "inst": "สถาบันเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "year": 2542}
                ],
                "academic_positions": [],
                "researches": [
                    {
                        "title": "การสกัดกฎความสัมพันธ์ด้วยกราฟความถี่สำหรับไอเทมที่เกิดขึ้นน้อยในชุดข้อมูลขนาดใหญ่",
                        "type": "วิจัยพื้นฐาน",
                        "year": 2561,
                        "funding": "ทุนวิจัยระดับบัณฑิตศึกษา มจพ.",
                        "budget": 150000.0,
                        "url": None
                    }
                ],
                "publications": [
                    {
                        "title": "ARMFEG: Association Rule Mining by Frequency-Edge-Graph for Rare Items",
                        "authors": "Suksakaophong P., Meesad P. and Unger H.",
                        "journal": "The 14th International Conference on Computing and Information Technology (IC2IT)",
                        "year": 2561,
                        "volume": "14",
                        "pages": "13-22",
                        "url": "https://link.springer.com"
                    }
                ],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2006, 8, 1), "end": None, "desc": "สอนวิชา Database Systems, Data Mining และ Big Data Analytics"}
                ],
                "trainings": [
                    {"course": "Big Data Engineering with Apache Spark & Kafka", "org": "Software Park Thailand", "start": date(2023, 8, 15), "end": date(2023, 8, 17), "hours": 24, "loc": "นนทบุรี"}
                ]
            },
            {
                "code": "IT-256605",
                "prefix_th": "อ.",
                "first_name_th": "เข็มชาติ",
                "last_name_th": "สังฆะคาม",
                "prefix_en": "Ajarn",
                "first_name_en": "Khemchat",
                "last_name_en": "Sangkhakham",
                "citizen_id": "3452000451829",
                "birth_date": date(1982, 4, 18),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_special_id,
                "start_work_date": date(2018, 1, 1),
                "appoint_date": date(2018, 1, 1),
                "email": "khemchat.s@globalhouse.co.th",
                "phone": "043-519-777",
                "internal_phone": "405",
                "address": "บมจ. สยามโกลบอลเฮ้าส์ 232 หมู่ 19 ต.รอบเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Software Engineering & Agile", "Cloud Computing & DevOps", "Database Management Systems"],
                "educations": [
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "วิศวกรรมศาสตร์ (อุตสาหการ)", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2548}
                ],
                "academic_positions": [],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "รองประธานเจ้าหน้าที่บริหาร", "org": "บริษัท สยามโกลบอลเฮ้าส์ จำกัด (มหาชน)", "start": date(2005, 5, 1), "end": None, "desc": "บริหารงานด้านปฏิบัติการและเทคโนโลยีสารสนเทศขององค์กร"},
                    {"pos": "อาจารย์พิเศษและกรรมการพัฒนาหลักสูตร", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2018, 1, 1), "end": None, "desc": "ร่วมผลิตบัณฑิต CWIE และหลักสูตรเทคโนโลยีสารสนเทศ"}
                ],
                "trainings": [
                    {"course": "Executive Enterprise Architecture & Cloud Transformation", "org": "สมาคมผู้บริหารเทคโนโลยีสารสนเทศ", "start": date(2023, 2, 18), "end": date(2023, 2, 19), "hours": 14, "loc": "กรุงเทพฯ"}
                ]
            },
            {
                "code": "IT-256606",
                "prefix_th": "อ.",
                "first_name_th": "กล้า",
                "last_name_th": "ภูมิพยัคฆ์",
                "prefix_en": "Ajarn",
                "first_name_en": "Kla",
                "last_name_en": "Phumphayak",
                "citizen_id": "3451000341294",
                "birth_date": date(1983, 7, 25),
                "gender": "ชาย",
                "marital_status": "โสด",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2010, 6, 1),
                "appoint_date": date(2010, 6, 1),
                "email": "kla.p@reru.ac.th",
                "phone": "087-654-3210",
                "internal_phone": "406",
                "address": "120 ถ.แจ้งสนิท ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Internet of Things (IoT) & Embedded Systems", "Cyber Security & Network Defense"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "ค.อ.ม.", "field": "เทคโนโลยีคอมพิวเตอร์", "inst": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "year": 2551},
                    {"level": "ปริญญาตรี", "name": "ค.บ.", "field": "คอมพิวเตอร์ศึกษา", "inst": "สถาบันราชภัฏบุรีรัมย์", "year": 2545}
                ],
                "academic_positions": [],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2010, 6, 1), "end": None, "desc": "สอนวิชาระบบเครือข่ายคอมพิวเตอร์และ IoT"}
                ],
                "trainings": [
                    {"course": "Cisco Certified Network Associate (CCNA) Security", "org": "Cisco Networking Academy", "start": date(2023, 4, 1), "end": date(2023, 4, 5), "hours": 30, "loc": "ออนไลน์"}
                ]
            },
            {
                "code": "IT-256607",
                "prefix_th": "ผศ.",
                "first_name_th": "จารุวรรณ",
                "last_name_th": "แสงปลาด",
                "prefix_en": "Asst. Prof.",
                "first_name_en": "Jaruwan",
                "last_name_en": "Sangplad",
                "citizen_id": "3451000628174",
                "birth_date": date(1981, 12, 5),
                "gender": "หญิง",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2008, 10, 1),
                "appoint_date": date(2016, 5, 20),
                "email": "jaruwan.s@reru.ac.th",
                "phone": "085-432-1098",
                "internal_phone": "407",
                "address": "67 หมู่ 3 ต.ดงลาน อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Web & Mobile Application Development", "Database Management Systems"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "ค.อ.ม.", "field": "คอมพิวเตอร์และเทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี", "year": 2550},
                    {"level": "ปริญญาตรี", "name": "ค.บ.", "field": "คอมพิวเตอร์ศึกษา", "inst": "สถาบันราชภัฏมหาสารคาม", "year": 2544}
                ],
                "academic_positions": [
                    {"title": "ผู้ช่วยศาสตราจารย์ สาขาวิชาคอมพิวเตอร์และเทคโนโลยีสารสนเทศ", "order": "มรภ.รอ. 068/2559", "date": date(2016, 5, 20)}
                ],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2008, 10, 1), "end": None, "desc": "สอนวิชาการพัฒนาเว็บแอปพลิเคชันและฐานข้อมูล"}
                ],
                "trainings": [
                    {"course": "Full-Stack Modern Web Frameworks (Node.js & React)", "org": "SIPA / DEPA", "start": date(2023, 6, 12), "end": date(2023, 6, 14), "hours": 18, "loc": "ขอนแก่น"}
                ]
            },
            {
                "code": "IT-256608",
                "prefix_th": "อ.",
                "first_name_th": "ณัฐธิดา",
                "last_name_th": "บุตรพรม",
                "prefix_en": "Ajarn",
                "first_name_en": "Natthida",
                "last_name_en": "Butprom",
                "citizen_id": "3451000819234",
                "birth_date": date(1988, 2, 17),
                "gender": "หญิง",
                "marital_status": "โสด",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2014, 8, 1),
                "appoint_date": date(2014, 8, 1),
                "email": "natthida.b@reru.ac.th",
                "phone": "084-321-0987",
                "internal_phone": "408",
                "address": "15/4 ถ.รณชัยชาญยุทธ ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Artificial Intelligence & Machine Learning", "Data Science & Big Data"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "วิทยาการคอมพิวเตอร์", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2555},
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "วิทยาการคอมพิวเตอร์", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2551}
                ],
                "academic_positions": [],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2014, 8, 1), "end": None, "desc": "สอนวิชา Machine Learning, AI และ Data Structures"}
                ],
                "trainings": [
                    {"course": "Applied Machine Learning with Scikit-Learn & PyTorch", "org": "AIAT (สมาคมปัญญาประดิษฐ์ประเทศไทย)", "start": date(2023, 9, 8), "end": date(2023, 9, 10), "hours": 20, "loc": "ออนไลน์"}
                ]
            },
            {
                "code": "IT-256609",
                "prefix_th": "ผศ.",
                "first_name_th": "ประหยัด",
                "last_name_th": "สุพะกำ",
                "prefix_en": "Asst. Prof.",
                "first_name_en": "Prayad",
                "last_name_en": "Suphakam",
                "citizen_id": "3451000492817",
                "birth_date": date(1979, 8, 29),
                "gender": "ชาย",
                "marital_status": "สมรส",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2007, 7, 1),
                "appoint_date": date(2015, 11, 10),
                "email": "prayad.s@reru.ac.th",
                "phone": "083-210-9876",
                "internal_phone": "409",
                "address": "112 หมู่ 7 ต.ปอภาร อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Software Engineering & Agile", "Cyber Security & Network Defense"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "วิทยาการคอมพิวเตอร์", "inst": "มหาวิทยาลัยขอนแก่น", "year": 2550},
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "วิทยาการคอมพิวเตอร์", "inst": "สถาบันราชภัฏมหาสารคาม", "year": 2544}
                ],
                "academic_positions": [
                    {"title": "ผู้ช่วยศาสตราจารย์ สาขาวิชาวิทยาการคอมพิวเตอร์", "order": "มรภ.รอ. 134/2558", "date": date(2015, 11, 10)}
                ],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2007, 7, 1), "end": None, "desc": "สอนวิชาวิศวกรรมซอฟต์แวร์และการรักษาความปลอดภัยระบบ"}
                ],
                "trainings": [
                    {"course": "Cyber Threat Intelligence & Incident Response", "org": "NCSA (สกมช.)", "start": date(2023, 10, 4), "end": date(2023, 10, 6), "hours": 20, "loc": "ออนไลน์"}
                ]
            },
            {
                "code": "IT-256610",
                "prefix_th": "อ.",
                "first_name_th": "วาทินี",
                "last_name_th": "ดวงอ่อนนาม",
                "prefix_en": "Ajarn",
                "first_name_en": "Watinee",
                "last_name_en": "Duang-onnam",
                "citizen_id": "3451000918273",
                "birth_date": date(1985, 6, 11),
                "gender": "หญิง",
                "marital_status": "โสด",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2012, 11, 1),
                "appoint_date": date(2012, 11, 1),
                "email": "watinee.d@reru.ac.th",
                "phone": "082-109-8765",
                "internal_phone": "410",
                "address": "79/3 ถ.ผดุงพานิช ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Database Management Systems", "Web & Mobile Application Development"],
                "educations": [
                    {"level": "ปริญญาโท", "name": "วท.ม.", "field": "เทคโนโลยีสารสนเทศ", "inst": "มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ", "year": 2554},
                    {"level": "ปริญญาตรี", "name": "วท.บ.", "field": "ระบบสารสนเทศเพื่อการจัดการ", "inst": "มหาวิทยาลัยมหาสารคาม", "year": 2548}
                ],
                "academic_positions": [],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2012, 11, 1), "end": None, "desc": "สอนวิชาการจัดการสารสนเทศและระบบฐานข้อมูล"}
                ],
                "trainings": [
                    {"course": "NoSQL Database & Cloud Datastores Architecture", "org": "AWS Academy", "start": date(2023, 11, 14), "end": date(2023, 11, 15), "hours": 12, "loc": "ออนไลน์"}
                ]
            },
            {
                "code": "IT-256611",
                "prefix_th": "อ.",
                "first_name_th": "ฉัตรฐพล",
                "last_name_th": "ต้นสุวรรณ",
                "prefix_en": "Ajarn",
                "first_name_en": "Chatthaphon",
                "last_name_en": "Tonsuwan",
                "citizen_id": "3451000736152",
                "birth_date": date(1984, 10, 3),
                "gender": "ชาย",
                "marital_status": "โสด",
                "department_id": dept_id,
                "branch_id": branch_id,
                "position_id": pos_lecturer_id,
                "personnel_type_id": pt_academic_id,
                "start_work_date": date(2011, 7, 1),
                "appoint_date": date(2011, 7, 1),
                "email": "chatthaphon.t@reru.ac.th",
                "phone": "081-098-7654",
                "internal_phone": "411",
                "address": "33 หมู่ 9 ต.สีแก้ว อ.เมือง จ.ร้อยเอ็ด 45000",
                "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
                "expertise": ["Web & Mobile Application Development", "Database Management Systems"],
                "educations": [
                    {"level": "ปริญญาตรี", "name": "บธ.บ.", "field": "คอมพิวเตอร์ธุรกิจ", "inst": "มหาวิทยาลัยมหาสารคาม", "year": 2547}
                ],
                "academic_positions": [],
                "researches": [],
                "publications": [],
                "work_exp": [
                    {"pos": "อาจารย์ประจำสาขาวิชาเทคโนโลยีสารสนเทศ", "org": "คณะเทคโนโลยีสารสนเทศ มรภ.ร้อยเอ็ด", "start": date(2011, 7, 1), "end": None, "desc": "สอนวิชาคอมพิวเตอร์ธุรกิจและเทคโนโลยีสารสนเทศเพื่อการจัดการ"}
                ],
                "trainings": [
                    {"course": "Digital Business Transformation with Modern IT", "org": "ETDA", "start": date(2023, 12, 1), "end": date(2023, 12, 2), "hours": 12, "loc": "ออนไลน์"}
                ]
            }
        ]

        created_objs = []
        for idx, t in enumerate(teachers_data, start=1):
            p = Personnel(
                id=idx,
                personnel_code=t["code"],
                prefix_th=t["prefix_th"],
                first_name_th=t["first_name_th"],
                last_name_th=t["last_name_th"],
                prefix_en=t["prefix_en"],
                first_name_en=t["first_name_en"],
                last_name_en=t["last_name_en"],
                citizen_id=t["citizen_id"],
                birth_date=t["birth_date"],
                gender=t["gender"],
                nationality="ไทย",
                religion="พุทธ",
                marital_status=t["marital_status"],
                department_id=t["department_id"],
                branch_id=t["branch_id"],
                position_id=t["position_id"],
                personnel_type_id=t["personnel_type_id"],
                start_work_date=t["start_work_date"],
                appoint_date=t["appoint_date"],
                work_status="ปฏิบัติงาน",
                email=t["email"],
                phone=t["phone"],
                internal_phone=t["internal_phone"],
                address=t["address"],
                subdistrict="ในเมือง",
                district="เมือง",
                province="ร้อยเอ็ด",
                zipcode="45000",
                avatar_url=t["avatar_url"]
            )

            # Link expertise
            for exp_name in t.get("expertise", []):
                if exp_name in all_exp:
                    p.expertise_list.append(all_exp[exp_name])

            # Link educations
            for edu in t.get("educations", []):
                p.education_histories.append(EducationHistory(
                    degree_level=edu["level"],
                    degree_name=edu["name"],
                    field_of_study=edu["field"],
                    institution=edu["inst"],
                    country="ไทย",
                    graduation_year=edu["year"]
                ))

            # Link academic positions
            for acad in t.get("academic_positions", []):
                p.academic_positions.append(AcademicPosition(
                    position_title=acad["title"],
                    order_number=acad.get("order"),
                    appointed_date=acad.get("date")
                ))

            # Link researches
            for res in t.get("researches", []):
                p.researches.append(Research(
                    title=res["title"],
                    research_type=res["type"],
                    year=res["year"],
                    funding_source=res["funding"],
                    budget=res["budget"],
                    url=res["url"]
                ))

            # Link publications
            for pub in t.get("publications", []):
                p.publications.append(Publication(
                    article_title=pub["title"],
                    authors=pub["authors"],
                    journal_conference_name=pub["journal"],
                    publication_year=pub["year"],
                    volume=pub.get("volume"),
                    pages=pub.get("pages"),
                    url=pub.get("url")
                ))

            # Link work experiences
            for w in t.get("work_exp", []):
                p.work_experiences.append(WorkExperience(
                    position=w["pos"],
                    organization=w["org"],
                    start_date=w["start"],
                    end_date=w.get("end"),
                    description=w.get("desc")
                ))

            # Link trainings
            for tr in t.get("trainings", []):
                p.trainings.append(Training(
                    course_name=tr["course"],
                    organizer=tr["org"],
                    start_date=tr["start"],
                    end_date=tr["end"],
                    hours=tr["hours"],
                    location=tr.get("loc")
                ))

            db.add(p)
            created_objs.append(p)

        db.commit()
        print(f"Successfully inserted {len(created_objs)} real faculty members into database!")

        # Update staff user to point to personnel ID 1 (ผศ.เชี่ยวชาญ ยางศิลา)
        staff_user = db.query(User).filter(User.username == "staff").first()
        if staff_user and len(created_objs) > 0:
            staff_user.personnel_id = created_objs[0].id
            db.commit()
            print(f"Updated staff user link to personnel ID {created_objs[0].id} (ผศ.เชี่ยวชาญ ยางศิลา)")

    except Exception as e:
        db.rollback()
        print(f"Error during import: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_faculty_data()
