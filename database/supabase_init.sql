-- ====================================================================
-- Database Schema for Personnel Management System (Supabase / PostgreSQL)
-- ====================================================================

-- 1. Roles Table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
);

-- 3. Departments Table (หน่วยงาน/คณะ)
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    code VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Branches Table (สาขาวิชา/ฝ่าย)
CREATE TABLE IF NOT EXISTS branches (
    id SERIAL PRIMARY KEY,
    department_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_branches_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- 5. Positions Table (ตำแหน่งงาน)
CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Personnel Types Table (ประเภทบุคลากร)
CREATE TABLE IF NOT EXISTS personnel_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Personnel Table (ข้อมูลบุคลากรหลัก)
CREATE TABLE IF NOT EXISTS personnel (
    id SERIAL PRIMARY KEY,
    user_id INT NULL UNIQUE,
    personnel_code VARCHAR(50) NOT NULL UNIQUE,
    prefix_th VARCHAR(50) NOT NULL,
    first_name_th VARCHAR(100) NOT NULL,
    last_name_th VARCHAR(100) NOT NULL,
    prefix_en VARCHAR(50) NULL,
    first_name_en VARCHAR(100) NULL,
    last_name_en VARCHAR(100) NULL,
    citizen_id VARCHAR(50) NULL,
    birth_date DATE NULL,
    gender VARCHAR(20) DEFAULT 'ชาย',
    nationality VARCHAR(50) DEFAULT 'ไทย',
    religion VARCHAR(50) DEFAULT 'พุทธ',
    marital_status VARCHAR(50) DEFAULT 'โสด',
    department_id INT NOT NULL,
    branch_id INT NULL,
    position_id INT NOT NULL,
    personnel_type_id INT NOT NULL,
    start_work_date DATE NULL,
    appoint_date DATE NULL,
    work_status VARCHAR(50) DEFAULT 'ปฏิบัติงาน',
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(50) NULL,
    internal_phone VARCHAR(20) NULL,
    address VARCHAR(255) NULL,
    subdistrict VARCHAR(100) NULL,
    district VARCHAR(100) NULL,
    province VARCHAR(100) NULL,
    zipcode VARCHAR(20) NULL,
    avatar_url VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_personnel_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_personnel_dept FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    CONSTRAINT fk_personnel_branch FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL,
    CONSTRAINT fk_personnel_pos FOREIGN KEY (position_id) REFERENCES positions(id) ON DELETE RESTRICT,
    CONSTRAINT fk_personnel_type FOREIGN KEY (personnel_type_id) REFERENCES personnel_types(id) ON DELETE RESTRICT
);

-- 8. Education Histories Table (ประวัติการศึกษา)
CREATE TABLE IF NOT EXISTS education_histories (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    degree_level VARCHAR(50) NOT NULL,
    degree_name VARCHAR(150) NOT NULL,
    field_of_study VARCHAR(150) NOT NULL,
    institution VARCHAR(200) NOT NULL,
    country VARCHAR(100) DEFAULT 'ไทย',
    graduation_year INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_edu_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 9. Work Experiences Table (ประวัติการทำงาน)
CREATE TABLE IF NOT EXISTS work_experiences (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    organization VARCHAR(200) NOT NULL,
    position VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_work_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 10. Academic Positions Table (ตำแหน่งทางวิชาการ)
CREATE TABLE IF NOT EXISTS academic_positions (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    position_title VARCHAR(100) NOT NULL,
    appointed_date DATE NULL,
    order_number VARCHAR(100) NULL,
    document_path VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_academic_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 11. Expertise Table (ความเชี่ยวชาญ)
CREATE TABLE IF NOT EXISTS expertise (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Personnel Expertise (ตารางเชื่อมความเชี่ยวชาญ)
CREATE TABLE IF NOT EXISTS personnel_expertise (
    personnel_id INT NOT NULL,
    expertise_id INT NOT NULL,
    PRIMARY KEY (personnel_id, expertise_id),
    CONSTRAINT fk_pe_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE,
    CONSTRAINT fk_pe_expertise FOREIGN KEY (expertise_id) REFERENCES expertise(id) ON DELETE CASCADE
);

-- 13. Researches Table (ผลงานวิจัย)
CREATE TABLE IF NOT EXISTS researches (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    title VARCHAR(300) NOT NULL,
    research_type VARCHAR(100) DEFAULT 'งานวิจัยประยุกต์',
    year INT NOT NULL,
    funding_source VARCHAR(200) NULL,
    budget DECIMAL(12, 2) DEFAULT 0.00,
    doi VARCHAR(150) NULL,
    url VARCHAR(255) NULL,
    abstract_detail TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_res_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 14. Publications Table (ผลงานตีพิมพ์)
CREATE TABLE IF NOT EXISTS publications (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    article_title VARCHAR(300) NOT NULL,
    authors VARCHAR(300) NOT NULL,
    journal_conference_name VARCHAR(250) NOT NULL,
    publication_year INT NOT NULL,
    volume VARCHAR(50) NULL,
    issue VARCHAR(50) NULL,
    pages VARCHAR(50) NULL,
    doi VARCHAR(150) NULL,
    url VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pub_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 15. Trainings Table (ประวัติการอบรม/สัมมนา)
CREATE TABLE IF NOT EXISTS trainings (
    id SERIAL PRIMARY KEY,
    personnel_id INT NOT NULL,
    course_name VARCHAR(250) NOT NULL,
    organizer VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    hours INT DEFAULT 0,
    location VARCHAR(200) NULL,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_train_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 16. Uploaded Files Table
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    personnel_id INT NULL,
    file_category VARCHAR(50) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    stored_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_files_personnel FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

-- 17. Audit Logs Table (บันทึกประวัติการทำรายการ)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NULL,
    username VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    module VARCHAR(50) NOT NULL,
    record_id VARCHAR(100) NULL,
    ip_address VARCHAR(50) NULL,
    user_agent VARCHAR(255) NULL,
    description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Audit Logs
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs (created_at);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs (action);
CREATE INDEX IF NOT EXISTS idx_audit_module ON audit_logs (module);


-- ====================================================================
-- SEED DATA
-- ====================================================================

-- 1. Insert Roles
INSERT INTO roles (id, name, description) VALUES
(1, 'ADMIN', 'ผู้ดูแลระบบ มีสิทธิ์จัดการข้อมูลทั้งหมดและกำหนดค่าระบบ'),
(2, 'EXECUTIVE', 'ผู้บริหาร มีสิทธิ์ดูภาพรวม Dashboard รายงาน และสถิติต่างๆ'),
(3, 'STAFF', 'บุคลากรทั่วไป มีสิทธิ์ดูและแก้ไขข้อมูลส่วนตัวของตนเอง')
ON CONFLICT (id) DO NOTHING;
SELECT setval('roles_id_seq', (SELECT MAX(id) FROM roles));

-- 2. Insert Users (Password: admin123, exec123, staff123 hashed with bcrypt)
INSERT INTO users (id, username, email, password_hash, role_id, is_active) VALUES
(1, 'admin', 'admin@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 1, TRUE),
(2, 'executive', 'dean.it@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 2, TRUE),
(3, 'somchai.s', 'somchai.s@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, TRUE),
(4, 'wichai.k', 'wichai.k@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, TRUE),
(5, 'kanya.p', 'kanya.p@reru.ac.th', '$2b$12$y1l8W5XJ8oGgYj7ElnXpSez15cWqU5u1F3nU/e9f3bYj2w8t/NqK.', 3, TRUE)
ON CONFLICT (id) DO NOTHING;
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- 3. Insert Departments
INSERT INTO departments (id, name, code) VALUES
(1, 'คณะเทคโนโลยีสารสนเทศ', 'IT-FAC'),
(2, 'สำนักงานคณบดีคณะเทคโนโลยีสารสนเทศ', 'IT-DEAN')
ON CONFLICT (id) DO NOTHING;
SELECT setval('departments_id_seq', (SELECT MAX(id) FROM departments));

-- 4. Insert Branches
INSERT INTO branches (id, department_id, name, code) VALUES
(1, 1, 'สาขาวิชาวิทยาการคอมพิวเตอร์ (CS)', 'CS'),
(2, 1, 'สาขาวิชาเทคโนโลยีสารสนเทศ (IT)', 'IT'),
(3, 1, 'สาขาวิชาวิศวกรรมซอฟต์แวร์ (SE)', 'SE'),
(4, 1, 'สาขาวิชานวัตกรรมดิจิทัลและปัญญาประดิษฐ์ (AI-DI)', 'AI-DI'),
(5, 2, 'งานบริหารงานทั่วไปและสารบรรณ', 'ADM'),
(6, 2, 'งานบริการการศึกษาและวิชาการ', 'EDU')
ON CONFLICT (id) DO NOTHING;
SELECT setval('branches_id_seq', (SELECT MAX(id) FROM branches));

-- 5. Insert Positions
INSERT INTO positions (id, name) VALUES
(1, 'อาจารย์ผู้สอน'),
(2, 'หัวหน้าสาขาวิชา'),
(3, 'รองคณบดีฝ่ายวิชาการ'),
(4, 'คณบดีคณะเทคโนโลยีสารสนเทศ'),
(5, 'นักวิชาการคอมพิวเตอร์'),
(6, 'เจ้าหน้าที่บริหารงานทั่วไป'),
(7, 'นักวิชาการศึกษา')
ON CONFLICT (id) DO NOTHING;
SELECT setval('positions_id_seq', (SELECT MAX(id) FROM positions));

-- 6. Insert Personnel Types
INSERT INTO personnel_types (id, name) VALUES
(1, 'ข้าราชการพลเรือนในสถาบันอุดมศึกษา'),
(2, 'พนักงานมหาวิทยาลัยสายวิชาการ'),
(3, 'พนักงานมหาวิทยาลัยสายสนับสนุน'),
(4, 'พนักงานราชการ'),
(5, 'ลูกจ้างชั่วคราว')
ON CONFLICT (id) DO NOTHING;
SELECT setval('personnel_types_id_seq', (SELECT MAX(id) FROM personnel_types));

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
ON CONFLICT (id) DO NOTHING;
SELECT setval('expertise_id_seq', (SELECT MAX(id) FROM expertise));

-- The remaining personnel data can be seeded using the backend python script (seed_real_personnel.py)
-- Or you can add the personnel records manually here.
