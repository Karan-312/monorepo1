# 📘 DSA Revision Tracker

A smart and dynamic desktop application to **track, plan, and optimize your DSA (Data Structures & Algorithms) revision journey** — designed for consistency, clarity, and performance.

---

## 🚀 Overview

Keeping track of your DSA progress can be overwhelming — especially with hundreds of problems to solve and revise. **DSA Revision Tracker** is built to automate your revision flow and help you stay on top of your prep by:

- Managing multiple revisions for each problem
- Adapting reminder schedules based on your performance
- Offering a clean, database-friendly interface for long-term tracking

---

## ✨ Features

### 🗂️ 1. Multi-Revision Tracking
Track up to **four revision attempts** per problem:
- Enter date of each try
- Specify whether you solved it yourself or needed help
- Log the time taken per attempt

###🔔 Intelligent Review Reminder System (Dynamic)
-No static 1-day or 3-day cycles here — the app uses a performance-based scheduling engine to adapt revision dates dynamically.
-Here's how it works:
-After every revision, your attempt is marked as either:
✅ Myself (self-solved)
❌ Help (needed help)

###These checkboxes across the 4 attempts are scored:

-> +2 points for each Myself
-> +1 point for each Help

Based on your total score (max 8), your performance rating is calculated:
-Excellent (7–8) → next review in 30 days
-Good (5–6) → next review in 14 days
-Mid (3–4) → next review in 7 days
-Poor (1–2) → next review in 3 days
-Skipped (0) → next review in 1 day
-Your next review date is then auto-calculated and shown in the Next Review column.

### Each time you check off a completed reminder, the app recalculates the next revision date accordingly.

### 📊 3. Performance Analyzer
Track how your problem-solving evolves over time with:
- Auto-generated *Last Performance* indicators
- Adaptive *Next Review* dates

### 💾 4. Data Persistence
- **Save All Rows** and **Load All Rows** anytime
- Easily manage your full revision history

### 🖱️ 5. Smooth UI
- Add new questions with one click
- No need for mouse-heavy navigation
- Fast keyboard-friendly interaction

---

## 🧠 Ideal For

- Students preparing for tech interviews
- Practicing Leetcode, Striver's Sheet, Love Babbar, etc.
- Anyone trying to build a long-term, revision-first DSA routine

---



## 📦 How to Use

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/DSA-Revision-Tracker.git

--------------------------------------------------------------------------------------------------------------
**UPDATES UNDERWAY**
** Still i am working on the Ui and also i am working on the logics to be the bit more advacned and dynamic .
** the notification system is file opening specific i am working on it to make it global across the system .
** the last performance coloumn will be updated with a more robust logic .
