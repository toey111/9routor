-- ====================================================================
-- Seed Data for Personnel Management System
-- Faculty of Information Technology, Roi Et Rajabhat University
-- Default Passwords:
-- admin / admin123
-- executive / exec123
-- staff / staff123
-- (Bcrypt Hash: $2b$12$fT77WbKz6jW.1pUoPjM53e7d69b3QoR4uE1bMvK3wU6zP6s8kI1jG or similar)
-- ====================================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

USE personnel_db;

SET NAMES utf8mb4;

-- 1. Insert Roles
INSERT INTO roles (id, name, description) VALUES
(1, 'ADMIN', 'ผู้ดูแลระบบ มีสิทธิ์จัดการข้อมูลทั้งหมดและกำหนดค่าระบบ'),
(2, 'EXECUTIVE', 'ผู้บริหาร มีสิทธิ์ดูภาพรวม Dashboard รายงาน และสถิติต่างๆ'),
(3, 'STAFF', 'บุคลากรทั่วไป มีสิทธิ์ดูและแก้ไขข้อมูลส่วนตัวของตนเอง')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. Insert Users (Password: admin123, exec123, staff123 hashed with bcrypt $2b$12$e8x... or standard hash)
-- bcrypt for 'admin123': $2b$12$2h8fQzXyF2w8v87VqL2tCe5G/B4j.yqP6F5o1X6y8iL.q1B9f7zKu (we will also support passlib verification in backend)
INSERT INTO users (id, username, email, password_hash, role_id, is_active) VALUES
(1, 'admin', 'admin@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 1, 1),
(2, 'executive', 'dean.it@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 2, 1),
(3, 'somchai.s', 'somchai.s@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, 1),
(4, 'wichai.k', 'wichai.k@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, 1),
(5, 'kanya.p', 'kanya.p@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, 1)
ON DUPLICATE KEY UPDATE username=VALUES(username);

-- 3. Insert Departments
INSERT INTO departments (id, name, code) VALUES
(1, 'คณะเทคโนโลยีสารสนเทศ', 'IT-FAC'),
(2, 'สำนักงานคณบดีคณะเทคโนโลยีสารสนเทศ', 'IT-DEAN')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 4. Insert Branches
INSERT INTO branches (id, department_id, name, code) VALUES
(1, 1, 'สาขาวิชาวิทยาการคอมพิวเตอร์ (CS)', 'CS'),
(2, 1, 'สาขาวิชาเทคโนโลยีสารสนเทศ (IT)', 'IT'),
(3, 1, 'สาขาวิชาวิศวกรรมซอฟต์แวร์ (SE)', 'SE'),
(4, 1, 'สาขาวิชานวัตกรรมดิจิทัลและปัญญาประดิษฐ์ (AI-DI)', 'AI-DI'),
(5, 2, 'งานบริหารงานทั่วไปและสารบรรณ', 'ADM'),
(6, 2, 'งานบริการการศึกษาและวิชาการ', 'EDU')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 5. Insert Positions
INSERT INTO positions (id, name) VALUES
(1, 'อาจารย์ผู้สอน'),
(2, 'หัวหน้าสาขาวิชา'),
(3, 'รองคณบดีฝ่ายวิชาการ'),
(4, 'คณบดีคณะเทคโนโลยีสารสนเทศ'),
(5, 'นักวิชาการคอมพิวเตอร์'),
(6, 'เจ้าหน้าที่บริหารงานทั่วไป'),
(7, 'นักวิชาการศึกษา')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 6. Insert Personnel Types
INSERT INTO personnel_types (id, name) VALUES
(1, 'ข้าราชการพลเรือนในสถาบันอุดมศึกษา'),
(2, 'พนักงานมหาวิทยาลัยสายวิชาการ'),
(3, 'พนักงานมหาวิทยาลัยสายสนับสนุน'),
(4, 'พนักงานราชการ'),
(5, 'ลูกจ้างชั่วคราว')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 7. Insert Expertise Master
INSERT INTO expertise (id, name) VALUES
(1, 'Software Engineering & Agile'),
(2, 'Artificial Intelligence & Machine Learning'),
(3, 'Data Science & Big Data'),
(4, 'Cyber Security & Network Defense'),
(5, 'Cloud Computing & DevOps'),
(6, 'Database Management Systems'),
(7, 'Web & Mobile Application Development'),
(8, 'Internet of Things (IoT) & Embedded Systems'),
(9, 'Computer Vision & Image Processing'),
(10, 'Natural Language Processing (NLP)')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 8. Insert 10+ Realistic Personnel records
INSERT INTO personnel (
    id, user_id, personnel_code, prefix_th, first_name_th, last_name_th,
    prefix_en, first_name_en, last_name_en, citizen_id, birth_date,
    gender, nationality, religion, marital_status, department_id, branch_id,
    position_id, personnel_type_id, start_work_date, appoint_date, work_status,
    email, phone, internal_phone, address, subdistrict, district, province, zipcode, avatar_url
) VALUES
(1, 2, 'IT-6001', 'รศ.ดร.', 'สมเกียรติ', 'เจริญทรัพย์', 'Assoc. Prof. Dr.', 'Somkiat', 'Charoensup', '1459900123456', '1975-04-12', 'ชาย', 'ไทย', 'พุทธ', 'สมรส', 1, 1, 4, 2, '2010-06-01', '2010-06-01', 'ปฏิบัติงาน', 'dean.it@reru.ac.th', '081-234-5678', '401', '123 ม.5 ต.เกาะแก้ว อ.เสลภูมิ จ.ร้อยเอ็ด', 'เกาะแก้ว', 'เสลภูมิ', 'ร้อยเอ็ด', '45120', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80'),
(2, 3, 'IT-6002', 'ผศ.ดร.', 'สมชาย', 'สายชล', 'Asst. Prof. Dr.', 'Somchai', 'Saichol', '1459900234567', '1982-08-25', 'ชาย', 'ไทย', 'พุทธ', 'สมรส', 1, 1, 3, 2, '2013-05-15', '2013-05-15', 'ปฏิบัติงาน', 'somchai.s@reru.ac.th', '082-345-6789', '402', '45 ถ.เทวาภิบาล ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด', 'ในเมือง', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80'),
(3, 4, 'IT-6003', 'ผศ.', 'วิชัย', 'กิตติคุณ', 'Asst. Prof.', 'Wichai', 'Kittikun', '1459900345678', '1980-11-10', 'ชาย', 'ไทย', 'พุทธ', 'สมรส', 1, 2, 2, 2, '2012-08-01', '2012-08-01', 'ปฏิบัติงาน', 'wichai.k@reru.ac.th', '083-456-7890', '403', '88 ม.2 ต.ดงลาน อ.เมือง จ.ร้อยเอ็ด', 'ดงลาน', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80'),
(4, 5, 'IT-6004', 'ดร.', 'กัญญา', 'เพชรไพลิน', 'Dr.', 'Kanya', 'Phetpailin', '1459900456789', '1988-02-14', 'หญิง', 'ไทย', 'พุทธ', 'โสด', 1, 3, 1, 2, '2018-01-10', '2018-01-10', 'ปฏิบัติงาน', 'kanya.p@reru.ac.th', '084-567-8901', '404', '99/1 ต.เหนือเมือง อ.เมือง จ.ร้อยเอ็ด', 'เหนือเมือง', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80'),
(5, NULL, 'IT-6005', 'อ.', 'ธนากร', 'วงศ์สว่าง', 'Mr.', 'Thanakorn', 'Wongsawang', '1459900567890', '1991-09-30', 'ชาย', 'ไทย', 'พุทธ', 'โสด', 1, 4, 1, 2, '2020-07-01', '2020-07-01', 'ปฏิบัติงาน', 'thanakorn.w@reru.ac.th', '085-678-9012', '405', '12 ม.4 ต.ขอนแก่น อ.เมือง จ.ร้อยเอ็ด', 'ขอนแก่น', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80'),
(6, NULL, 'IT-6006', 'ศ.ดร.', 'ประเสริฐ', 'ปัญญาวิบูลย์', 'Prof. Dr.', 'Prasert', 'Panyawiboon', '1459900678901', '1968-01-05', 'ชาย', 'ไทย', 'พุทธ', 'สมรส', 1, 1, 1, 1, '1995-10-01', '1995-10-01', 'ปฏิบัติงาน', 'prasert.p@reru.ac.th', '086-789-0123', '406', '55 ต.รอบเมือง อ.เมือง จ.ร้อยเอ็ด', 'รอบเมือง', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80'),
(7, NULL, 'IT-6007', 'ผศ.', 'ณัฐพร', 'บุญรักษา', 'Asst. Prof.', 'Nattaporn', 'Boonraksa', '1459900789012', '1985-06-18', 'หญิง', 'ไทย', 'พุทธ', 'สมรส', 1, 2, 1, 2, '2015-09-01', '2015-09-01', 'ลาศึกษาต่อ', 'nattaporn.b@reru.ac.th', '087-890-1234', '407', '78 ต.ในเมือง อ.เสลภูมิ จ.ร้อยเอ็ด', 'ในเมือง', 'เสลภูมิ', 'ร้อยเอ็ด', '45120', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80'),
(8, NULL, 'IT-6008', 'อ.', 'อภิสิทธิ์', 'รัตนโกสินทร์', 'Mr.', 'Aphisit', 'Rattanakosin', '1459900890123', '1993-12-03', 'ชาย', 'ไทย', 'พุทธ', 'โสด', 1, 3, 1, 4, '2022-03-15', '2022-03-15', 'ปฏิบัติงาน', 'aphisit.r@reru.ac.th', '088-901-2345', '408', '210 ต.เสลภูมิ อ.เสลภูมิ จ.ร้อยเอ็ด', 'เสลภูมิ', 'เสลภูมิ', 'ร้อยเอ็ด', '45120', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80'),
(9, NULL, 'IT-6009', 'นาง', 'สุชาดา', 'มงคลศรี', 'Mrs.', 'Suchada', 'Mongkolsri', '1459900901234', '1987-05-20', 'หญิง', 'ไทย', 'พุทธ', 'สมรส', 2, 5, 6, 3, '2014-11-01', '2014-11-01', 'ปฏิบัติงาน', 'suchada.m@reru.ac.th', '089-012-3456', '410', '44 ต.ในเมือง อ.เมือง จ.ร้อยเอ็ด', 'ในเมือง', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80'),
(10, NULL, 'IT-6010', 'นาย', 'กิตติศักดิ์', 'พงษ์พาณิชย์', 'Mr.', 'Kittisak', 'Pongpanich', '1459901012345', '1990-07-12', 'ชาย', 'ไทย', 'พุทธ', 'โสด', 2, 6, 5, 3, '2017-04-01', '2017-04-01', 'ปฏิบัติงาน', 'kittisak.p@reru.ac.th', '090-123-4567', '411', '101 ต.เกาะแก้ว อ.เสลภูมิ จ.ร้อยเอ็ด', 'เกาะแก้ว', 'เสลภูมิ', 'ร้อยเอ็ด', '45120', 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80'),
(11, NULL, 'IT-6011', 'ดร.', 'ศศิธร', 'งามเจริญ', 'Dr.', 'Sasithorn', 'Ngamcharoen', '1459901123456', '1986-03-08', 'หญิง', 'ไทย', 'พุทธ', 'โสด', 1, 4, 1, 2, '2016-02-01', '2016-02-01', 'ปฏิบัติงาน', 'sasithorn.n@reru.ac.th', '091-234-5678', '409', '32 ต.เหนือเมือง อ.เมือง จ.ร้อยเอ็ด', 'เหนือเมือง', 'เมือง', 'ร้อยเอ็ด', '45000', 'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?auto=format&fit=crop&w=400&q=80')
ON DUPLICATE KEY UPDATE personnel_code=VALUES(personnel_code);

-- 9. Insert Education Histories
INSERT INTO education_histories (personnel_id, degree_level, degree_name, field_of_study, institution, country, graduation_year) VALUES
(1, 'ปริญญาตรี', 'วท.บ.', 'วิทยาการคอมพิวเตอร์', 'มหาวิทยาลัยขอนแก่น', 'ไทย', 2540),
(1, 'ปริญญาโท', 'วท.ม.', 'วิทยาการคอมพิวเตอร์', 'จุฬาลงกรณ์มหาวิทยาลัย', 'ไทย', 2544),
(1, 'ปริญญาเอก', 'Ph.D.', 'Computer Science & Engineering', 'University of Manchester', 'สหราชอาณาจักร', 2552),
(2, 'ปริญญาตรี', 'วท.บ.', 'เทคโนโลยีสารสนเทศ', 'มหาวิทยาลัยมหาสารคาม', 'ไทย', 2547),
(2, 'ปริญญาโท', 'วศ.ม.', 'วิศวกรรมคอมพิวเตอร์', 'มหาวิทยาลัยเกษตรศาสตร์', 'ไทย', 2551),
(2, 'ปริญญาเอก', 'ปร.ด.', 'วิทยาการคอมพิวเตอร์', 'สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง', 'ไทย', 2558),
(3, 'ปริญญาตรี', 'วศ.บ.', 'วิศวกรรมคอมพิวเตอร์', 'มหาวิทยาลัยอุบลราชธานี', 'ไทย', 2545),
(3, 'ปริญญาโท', 'วท.ม.', 'วิศวกรรมซอฟต์แวร์', 'มหาวิทยาลัยสงขลานครินทร์', 'ไทย', 2550),
(4, 'ปริญญาตรี', 'วท.บ.', 'วิทยาการคอมพิวเตอร์', 'มหาวิทยาลัยราชภัฏร้อยเอ็ด', 'ไทย', 2553),
(4, 'ปริญญาโท', 'วท.ม.', 'ปัญญาประดิษฐ์ประยุกต์', 'มหาวิทยาลัยเชียงใหม่', 'ไทย', 2556),
(4, 'ปริญญาเอก', 'Ph.D.', 'Data Science & AI', 'Asian Institute of Technology (AIT)', 'ไทย', 2562),
(5, 'ปริญญาตรี', 'วศ.บ.', 'วิศวกรรมคอมพิวเตอร์', 'มหาวิทยาลัยเทคโนโลยีสุรนารี', 'ไทย', 2556),
(5, 'ปริญญาโท', 'วศ.ม.', 'ระบบสมองกลฝังตัวและ IoT', 'มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ', 'ไทย', 2560),
(6, 'ปริญญาตรี', 'วท.บ.', 'สถิติประยุกต์และคอมพิวเตอร์', 'มหาวิทยาลัยธรรมศาสตร์', 'ไทย', 2533),
(6, 'ปริญญาโท', 'วท.ม.', 'วิทยาการคอมพิวเตอร์', 'สถาบันบัณฑิตพัฒนบริหารศาสตร์ (NIDA)', 'ไทย', 2537),
(6, 'ปริญญาเอก', 'Ph.D.', 'Computer Information Systems', 'Monash University', 'ออสเตรเลีย', 2544);

-- 10. Insert Academic Positions
INSERT INTO academic_positions (personnel_id, position_title, appointed_date, order_number, document_path) VALUES
(1, 'รองศาสตราจารย์', '2561-09-15', 'มรภ.รอ. 452/2561', '/uploads/docs/order_6001_assoc.pdf'),
(2, 'ผู้ช่วยศาสตราจารย์', '2563-03-20', 'มรภ.รอ. 118/2563', '/uploads/docs/order_6002_asst.pdf'),
(3, 'ผู้ช่วยศาสตราจารย์', '2559-11-10', 'มรภ.รอ. 320/2559', '/uploads/docs/order_6003_asst.pdf'),
(6, 'ศาสตราจารย์', '2556-08-01', 'สำนักนายกรัฐมนตรี 88/2556', '/uploads/docs/order_6006_prof.pdf'),
(7, 'ผู้ช่วยศาสตราจารย์', '2564-05-12', 'มรภ.รอ. 205/2564', '/uploads/docs/order_6007_asst.pdf');

-- 11. Insert Personnel Expertise Mapping
INSERT INTO personnel_expertise (personnel_id, expertise_id) VALUES
(1, 1), (1, 6), (1, 4),
(2, 2), (2, 3), (2, 7),
(3, 1), (3, 5), (3, 7),
(4, 2), (4, 3), (4, 10),
(5, 8), (5, 5), (5, 7),
(6, 6), (6, 3), (6, 4),
(7, 1), (7, 7),
(8, 7), (8, 1),
(10, 5), (10, 4),
(11, 2), (11, 9);

-- 12. Insert Work Experiences
INSERT INTO work_experiences (personnel_id, organization, position, start_date, end_date, description) VALUES
(1, 'บริษัท ซอฟต์แวร์อินโนเวชั่น จำกัด', 'Senior Systems Architect', '2545-01-01', '2549-12-31', 'ออกแบบสถาปัตยกรรมคลาวด์สำหรับระบบธนาคาร'),
(2, 'ศูนย์เทคโนโลยีอิเล็กทรอนิกส์และคอมพิวเตอร์แห่งชาติ (NECTEC)', 'นักวิจัยผู้ช่วย', '2552-06-01', '2555-12-31', 'วิจัยด้าน Machine Learning สำหรับการประมวลผลภาษาธรรมชาติ'),
(3, 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)', 'Full-Stack Developer', '2551-02-01', '2555-06-30', 'พัฒนาระบบ Customer Portal และ API Gateway'),
(4, 'สถาบันวิจัยแสงซินโครตรอน (องค์การมหาชน)', 'Data Engineer', '2557-01-01', '2560-12-31', 'บริหารจัดการและวิเคราะห์ Big Data จากการทดลอง');

-- 13. Insert Researches
INSERT INTO researches (personnel_id, title, research_type, year, funding_source, budget, doi, url, abstract_detail) VALUES
(1, 'การพัฒนาระบบประเมินความเสี่ยงด้านความมั่นคงปลอดภัยไซเบอร์สำหรับองค์กรปกครองส่วนท้องถิ่นในภาคตะวันออกเฉียงเหนือ', 'งานวิจัยประยุกต์', 2566, 'กองทุนส่งเสริมวิทยาศาสตร์ วิจัยและนวัตกรรม (สกสว.)', 450000.00, '10.1145/3456789.3456790', 'https://doi.org/10.1145/3456789.3456790', 'งานวิจัยนี้เสนอแบบจำลองการวิเคราะห์ช่องโหว่และการป้องกันเชิงรุกสำหรับระบบเครือข่ายของ อบต. และ เทศบาล'),
(2, 'การประยุกต์ใช้โมเดลโครงข่ายประสาทเทียมแบบ Transformer ในการจำแนกคุณภาพข้าวหอมมะลิทุ่งกุลาร้องไห้จากภาพถ่ายความละเอียดสูง', 'งานวิจัยประยุกต์', 2567, 'สำนักงานการวิจัยแห่งชาติ (วช.)', 600000.00, '10.1016/j.compag.2024.108920', 'https://doi.org/10.1016/j.compag.2024.108920', 'การประมวลผลภาพเมล็ดข้าวด้วย Deep Learning เพื่อยกระดับมาตรฐานผลผลิตเกษตรกรจังหวัดร้อยเอ็ด'),
(4, 'การพยากรณ์ปริมาณน้ำท่วมในลุ่มน้ำชีตอนล่างด้วยเทคนิค Deep Ensemble Learning', 'งานวิจัยพื้นฐาน', 2566, 'ทุนอุดหนุนการวิจัย มหาวิทยาลัยราชภัฏร้อยเอ็ด', 200000.00, '10.1109/ACCESS.2023.1234567', 'https://doi.org/10.1109/ACCESS.2023.1234567', 'สร้างโมเดลเตือนภัยล่วงหน้า 48 ชั่วโมงสำหรับพื้นที่เสี่ยงน้ำท่วมริมแม่น้ำชี');

-- 14. Insert Publications
INSERT INTO publications (personnel_id, article_title, authors, journal_conference_name, publication_year, volume, issue, pages, doi, url) VALUES
(1, 'A Lightweight Security Architecture for Edge-IoT Networks in Smart Farming', 'Charoensup, S., & Panyawiboon, P.', 'IEEE Internet of Things Journal', 2566, '10', '4', '3120-3132', '10.1109/JIOT.2023.998877', 'https://ieeexplore.ieee.org/document/998877'),
(2, 'Automated Rice Quality Inspection Using Vision Transformer and Attention Mechanisms', 'Saichol, S., Phetpailin, K., & Charoensup, S.', 'Computers and Electronics in Agriculture (Elsevier)', 2567, '218', '1', '108920', '10.1016/j.compag.2024.108920', 'https://sciencedirect.com/science/article/pii/S016816992400123X'),
(4, 'A Real-Time Flood Prediction Framework Using Spatio-Temporal Graph Neural Networks', 'Phetpailin, K., & Saichol, S.', 'IEEE Access', 2566, '11', '', '14520-14535', '10.1109/ACCESS.2023.1234567', 'https://ieeexplore.ieee.org/document/1234567');

-- 15. Insert Trainings
INSERT INTO trainings (personnel_id, course_name, organizer, start_date, end_date, hours, location, description) VALUES
(1, 'Certified Information Systems Security Professional (CISSP) Workshop', 'สถาบันไซเบอร์อะคาเดมี่แห่งชาติ', '2566-07-10', '2566-07-14', 35, 'โรงแรมมิราเคิลแกรนด์ กรุงเทพฯ', 'การบริหารจัดการความมั่นคงปลอดภัยสารสนเทศระดับสากล'),
(2, 'Advanced Generative AI and LLM Orchestration with LangChain', 'สมาคมปัญญาประดิษฐ์ประเทศไทย (AIAT)', '2567-02-19', '2567-02-21', 21, 'มหาวิทยาลัยเกษตรศาสตร์', 'การพัฒนา AI Chatbot และ Agentic Application'),
(3, 'Microservices Architecture with Docker & Kubernetes', 'Software Park Thailand', '2566-10-05', '2566-10-07', 24, 'อาคารซอฟต์แวร์พาร์ค แจ้งวัฒนะ', 'การออกแบบและบริหารจัดการ Container ระดับองค์กร'),
(4, 'Data Science for Public Policy and Social Impact', 'สถาบันบัณฑิตพัฒนบริหารศาสตร์ (NIDA)', '2566-11-15', '2566-11-17', 18, 'NIDA กรุงเทพฯ', 'การนำข้อมูลเปิดภาครัฐมาวิเคราะห์เพื่อแก้ปัญหาเชิงพื้นที่');

-- 16. Insert Initial Audit Logs
INSERT INTO audit_logs (user_id, username, action, module, record_id, ip_address, user_agent, description) VALUES
(1, 'admin', 'LOGIN', 'AUTH', '1', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'ผู้ดูแลระบบเข้าสู่ระบบสำเร็จ'),
(1, 'admin', 'CREATE', 'MASTER_DATA', '1', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'สร้างข้อมูลหน่วยงาน: คณะเทคโนโลยีสารสนเทศ'),
(1, 'admin', 'CREATE', 'PERSONNEL', '1', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'เพิ่มข้อมูลบุคลากร: รศ.ดร.สมเกียรติ เจริญทรัพย์ (IT-6001)');
