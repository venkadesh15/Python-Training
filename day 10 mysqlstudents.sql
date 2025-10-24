-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS schooldb;

-- Use the created database
USE schooldb;

-- Drop existing table (optional, to start fresh)
DROP TABLE IF EXISTS students;

-- Create table for storing student records
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    average FLOAT NOT NULL,
    grade VARCHAR(2) NOT NULL
);

-- Insert sample student records
INSERT INTO students (name, age, average, grade) VALUES
('Ravi', 20, 88.5, 'A'),
('Priya', 19, 76.0, 'B'),
('Arun', 21, 59.0, 'C');

-- Display all student records
SELECT * FROM students;

-- Update a student record
UPDATE students
SET name = 'Kumar', age = 22, average = 91.2, grade = 'A'
WHERE id = 1;

-- Delete a specific student record
DELETE FROM students WHERE id = 2;

-- Delete all student records
DELETE FROM students;

-- Drop the table (optional, only if resetting)
-- DROP TABLE students;
