# 🤖 AI-Based Student Attendance Management System

A web-based **AI-Based Student Attendance Management System** developed using Python, Flask, SQLite, HTML, CSS, and Machine Learning.

This system helps manage students, record daily attendance, calculate attendance percentage, identify low attendance, maintain attendance history, and provide AI-based attendance prediction.

---

## 📌 Project Overview

The AI-Based Student Attendance Management System is designed to simplify and automate the student attendance management process.

The system provides an easy-to-use interface for managing student details and attendance records.

### Main Functions

- 👨‍🎓 Add and manage students
- 📅 Mark daily attendance
- 📊 Calculate attendance percentage
- ⚠️ Detect low attendance
- 🤖 Predict attendance using Machine Learning
- 📜 View attendance history
- 💾 Store data using SQLite
- 📈 Display attendance dashboard

---

## 🎯 Objectives

The main objectives of this project are:

1. To automate student attendance management.
2. To reduce manual attendance calculation.
3. To maintain attendance records digitally.
4. To calculate attendance percentage automatically.
5. To identify students with low attendance.
6. To provide Machine Learning-based attendance prediction.
7. To provide a simple dashboard for attendance monitoring.

---

## ✨ Features

### 👨‍🎓 Student Management

- Add student
- Store student name
- Store roll number
- View student list
- Delete student

### 📅 Daily Attendance

- Select attendance date
- Mark Present or Absent
- Save attendance records
- Prevent duplicate attendance for the same date by replacing the saved attendance for that date

### 📊 Attendance Summary

- Calculate attendance percentage
- Display individual student attendance
- Show low attendance alert
- Show good attendance status

### 🤖 AI/ML Prediction

The system uses **Linear Regression** from Scikit-learn to generate an estimated attendance prediction based on previous attendance records.

### 📈 Dashboard

The dashboard displays:

- 👨‍🎓 Total Students
- ✅ Today Present
- ❌ Today Absent
- 📅 Total Attendance Days

### 📜 Attendance History

Attendance history displays:

- Date
- Student Name
- Roll Number
- Present / Absent Status

### 💾 Database

SQLite is used to store:

- Student details
- Attendance records

---

## 🧠 Machine Learning

The project uses **Linear Regression** for the attendance prediction feature.

Attendance is converted into numerical values:

```text
Present = 1
Absent  = 0

## 🔗 Project Links

- 🌐 [Live Application](https://ai-student-attendance-management.onrender.com)
- 💻 [GitHub Repository](https://github.com/asanm104anm10410422213011/AI-Student-Attendance-Management)
