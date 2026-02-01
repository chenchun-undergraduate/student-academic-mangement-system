CREATE DATABASE IF NOT EXISTS Class_GPA_Management_SYS_db;
USE Class_GPA_Management_SYS_db;


CREATE TABLE IF NOT EXISTS courses (
    course_id    INT PRIMARY KEY AUTO_INCREMENT,
    course_code  VARCHAR(50),
    course_name  VARCHAR(200) NOT NULL,
    credit       DECIMAL(1) NOT NULL,
    category     VARCHAR(50),
    remark       TEXT
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# score_row: precent grades
# grade_point >= 2.4 pass
# status: Normal / Retake / Correction / InProgress

CREATE TABLE IF NOT EXISTS grades_current (
    grade_id      INT PRIMARY KEY AUTO_INCREMENT,
    course_id     INT NOT NULL,
    grade_point   DECIMAL(3,2),    
    term          VARCHAR(30),      
    status        VARCHAR(20) DEFAULT 'Normal',
    comment       TEXT,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_grades_course
      FOREIGN KEY (course_id) REFERENCES courses(course_id)
      ON DELETE CASCADE
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


# store course change history
CREATE TABLE IF NOT EXISTS grade_changes (
    change_id       INT PRIMARY KEY AUTO_INCREMENT,
    course_id       INT NOT NULL,
    old_grade_point DECIMAL(3,2),
    new_grade_point DECIMAL(3,2),
    change_type     VARCHAR(20),    
    change_time     DATETIME DEFAULT CURRENT_TIMESTAMP,
    comment         TEXT,

    CONSTRAINT fk_changes_course
      FOREIGN KEY (course_id) REFERENCES courses(course_id)
      ON DELETE CASCADE
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


# relational table between selected course and it's pre course
# both course_id and prereq_course_id reference courses.course_id
CREATE TABLE IF NOT EXISTS course_prerequisites (
    id               INT PRIMARY KEY AUTO_INCREMENT,
    course_id        INT NOT NULL,  
    prereq_course_id INT NOT NULL,  

    CONSTRAINT fk_prereq_course
      FOREIGN KEY (course_id) REFERENCES courses(course_id)
      ON DELETE CASCADE,

    CONSTRAINT fk_prereq_required
      FOREIGN KEY (prereq_course_id) REFERENCES courses(course_id)
      ON DELETE CASCADE,

    CONSTRAINT uq_course_prereq UNIQUE (course_id, prereq_course_id)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DELIMITER $$

# ------------ the trigger record the data when we insert a GPA
CREATE TRIGGER insert_trigger
AFTER INSERT ON grades_current
FOR EACH ROW
BEGIN
    INSERT INTO grade_changes (
        course_id,
        old_grade_point,
        new_grade_point,
        change_type,
        change_time,
        comment
    ) VALUES (
        NEW.course_id,
        NULL,
        NEW.grade_point,
        NEW.status,            
        NOW(),
        NEW.comment           
    );
END$$

# ----------- the trigger record the data when we update GPA
CREATE TRIGGER update_trigger
BEFORE UPDATE ON grades_current
FOR EACH ROW
BEGIN
    INSERT INTO grade_changes (
        course_id,
        old_grade_point,
        new_grade_point,
        change_type,
        change_time,
        comment
    ) VALUES (
        NEW.course_id,
        OLD.grade_point,
        NEW.grade_point,
        NEW.status,      
        NOW(),
        NEW.comment
    );

    SET NEW.updated_at = NOW();
END$$

DELIMITER ;




# enter the courses and set the the course name, credit, and category(required/ major)
use Class_GPA_Management_SYS_db;

INSERT INTO courses (course_code, course_name, credit, category)
VALUES
('ESL0303', 'ESL 0303 Academic oral presentation I', 3, 'Required'),
('ESL0305', 'ESL 0305 Academic written terminology I', 3, 'Required'),
('GE1000', 'GE 1000 Transition to Kean', 1, 'Required'),
('ENG1300', 'ENG 1300 English essays by non-native speakers I', 6, 'Required'),
('CPS1231', 'CPS 1231 Foundations of Computer Science', 4, 'Major'),

('ESL0403', 'ESL 0403 Academic oral presentation II', 3, 'Required'),
('ESL0405', 'ESL 0405 Academic written terminology II', 3, 'Required'),
('MATH2110', 'MATH 2110 Discrete structure', 3, 'Required'),
('ENG1430', 'ENG 1430 English essays by non-native speakers II', 6, 'Required'),
('CPS2231', 'CPS 2231 Computer Programming', 4, 'Major'),

('CPS2232', 'CPS 2232 Data Structures', 4, 'Major'),
('CPS2390', 'CPS 2390 Organization and Structure', 3, 'Major'),
('MATH2995', 'MATH 2995 Matrices and Linear Algebra', 3, 'Required'),
('MATH2415', 'MATH 2415 Calculus I', 4, 'Required'),
('GE2024', 'GE 2024 Research and Technology', 3, 'Required'),

('HIST1062', 'HIST 1062 World History', 3, 'Required'),
('TECH2920', 'TECH 2920 Computer System', 3, 'Major'),
('CPS3250', 'CPS 3250 Computer operating system', 3, 'Major'),
('MATH2416', 'MATH 2416 Calculus II', 4, 'Required'),
('COMM1402', 'COMM 1402 Verbal communication', 3, 'Required'),
('ENG2403', 'ENG 2403 English essays by non-native speakers III', 3, 'Required'),

('CPS3440', 'CPS 3440 Algorithm Analysis', 3, 'Major'),
('MATH2526', 'MATH 2526 Applied Statistics', 3, 'Required'),
('ENG3091', 'ENG 3091 Technical writing', 3, 'Required'),
('LABSCI1', 'Lab Science I', 4, 'Required'),
('CPS_ELEC', 'CPS Elective 3xxx/4xxx', 3, 'Major'),

('CPS3962', 'CPS 3962 Object-oriented analysis and design', 3, 'Major'),
('CPS_ELEC1', 'CPS elective #1 Computer elective courses I', 3, 'Major'),
('CPS4150', 'CPS 4150 Computer Architecture', 4, 'Major'),
('LABSCI2', 'Lab Science II', 3, 'Required'),
('COMM3590', 'COMM 3590', 3, 'Required'),

('CPS4222', 'CPS 4222 Network Principles', 3, 'Major'),
('MATH_ELEC1', 'CPS elective or MATH 3xxx (Fall)', 3, 'require'),
('GE_HUM_ELEC', 'GE Humanity elective General education humanities elective courses', 3, 'Required'),
('CPS_ELEC2', 'CPS elective #2', 3, 'Major'),
('MATH_ELEC2', 'CPS elective or MATH 3xxx (Fall second)', 3, 'require'),

('CPS4951', 'CPS 4951 Advanced Projects', 3, 'Major'),
('CPS_ELEC3', 'CPS elective #3', 3, 'Major'),
('GE_SOCSCI_ELEC', 'GE Social Sci. elective General Social Sciences', 3, 'Required'),
('CPS_ELEC4', 'CPS elective #4', 3, 'Major'),
('CPS_ELEC5', 'CPS elective #5', 3, 'Major');


# This table is useful for quickly registering course IDs to course_prerequisites 
#via mapping for a large number of prerequisite courses.
CREATE TABLE IF NOT EXISTS course_prereq_mapping (
    course_code      VARCHAR(50),
    prereq_course_code VARCHAR(50)
);

INSERT INTO course_prereq_mapping (prereq_course_code,course_code) VALUES
('CPS1231', 'CPS2231'),
('ESL0303', 'ESL0403'),
('ESL0305', 'ESL0405'),
('ENG1430', 'ENG2403'),
('CPS2231', 'CPS2232'),
('CPS2231','CPS2390'),
('MATH2415','MATH2416'),
('MATH2415','MATH_ELEC1'),
('MATH2415','MATH_ELEC2'),
('ENG2403','ENG3091'),
('CPS2232','CPS_ELEC'),
('CPS2232','CPS_ELEC1'),
('CPS2232','CPS_ELEC2'),
('CPS2232','CPS_ELEC3'),
('CPS2232','CPS_ELEC4'),
('CPS2232','CPS_ELEC5'),
('LABSCI1','LABSCI2'),
('CPS2232','CPS3250'),
('CPS2390','CPS3250'),
('CPS3250','CPS4222'),
('COMM1402','COMM3590'),
('CPS2232','CPS3962'),
('CPS2232','CPS4150')
;

INSERT INTO course_prerequisites (course_id, prereq_course_id)
SELECT
    course.course_id,
    prereq.course_id
FROM
    course_prereq_mapping AS x
    JOIN courses AS course ON course.course_code = x.course_code
    JOIN courses AS prereq ON prereq.course_code = x.prereq_course_code;


# see all tables
select * from course_prerequisites;
select * from courses;
select * from grade_changes;
select * from grades_current;
select * from course_prereq_mapping;


# --------------------------- delete function --------------
# delete four table values
-- TRUNCATE table course_prerequisites;
-- TRUNCATE table grade_changes;
-- TRUNCATE table grades_current;
-- TRUNCATE table course_prereq_mapping;

# drop all the row in courses table
-- SET SQL_SAFE_UPDATES = 0;
-- DELETE FROM courses;
-- ALTER TABLE courses AUTO_INCREMENT = 1;
-- SET SQL_SAFE_UPDATES = 1;


# ------------------ insert course or prerequisites course individual
# assume we don't konw the individual id in courses table we only
# konw the relationship between each course
-- INSERT INTO course_prerequisites (course_id, prereq_course_id)
-- SELECT 
--        course.course_id, 
--        pre.course_id
-- FROM courses AS pre, courses AS course
-- WHERE pre.course_code = 'CPS2232' AND course.course_code = 'CPS4150';

# insert value into courses
# INSERT INTO courses (course_code, course_name, credit, category)
# VALUES('','',0,'');

# don't run it 
# DROP schema Class_GPA_Management_SYS_db;