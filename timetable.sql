CREATE DATABASE TT;
USE TT;

CREATE TABLE schedule (
    DAY VARCHAR(255),
    P1 VARCHAR(255),
    P2 VARCHAR(255),
    P3 VARCHAR(255),
    P4 VARCHAR(255),
    BREAK VARCHAR(5) DEFAULT "BREAK",
    P5 VARCHAR(255),
    P6 VARCHAR(255),
    P7 VARCHAR(255),
    P8 VARCHAR(255)
);
SELECT * FROM schedule;

CREATE TABLE teacher (
    TEACHER_NAME VARCHAR(255) PRIMARY KEY,
    TEACHER_WORKING INT
);

CREATE TABLE course (
    COURSE_CODE VARCHAR(255) PRIMARY KEY,
    PROGRAM_NAME VARCHAR(255),
    COURSE_CREDIT INT,
    COURSE_TYPE VARCHAR(255),
    COURSE_SEM INT,
    COURSE_DURATION INT 
);

CREATE TABLE teacher_course_allocation (
    TEACHER_NAME VARCHAR(255),
    COURSE_CODE VARCHAR(255),
    PRIMARY KEY (TEACHER_NAME, COURSE_CODE),
    INDEX fk_teacher_idx (TEACHER_NAME),
    INDEX fk_course_idx (COURSE_CODE),
    FOREIGN KEY (TEACHER_NAME) REFERENCES teacher (TEACHER_NAME) ON DELETE CASCADE,
    FOREIGN KEY (COURSE_CODE) REFERENCES course (COURSE_CODE) ON DELETE CASCADE
);

SELECT * FROM course;
SELECT * FROM teacher;
SELECT * FROM teacher_course_allocation;


DROP TABLE teacher;
DROP TABLE course;
DROP TABLE teacher_course_allocation;
commit;