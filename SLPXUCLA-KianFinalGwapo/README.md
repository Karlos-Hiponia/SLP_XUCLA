# Ulas Tracking System

The **Ulas Tracking System** is a web-based platform developed to support the **Unified Legal Aid Service (ULAS)** program under the **Clinical Legal Education Program (CLEP)** at **Xavier University's College of Law**.  
This system facilitates efficient tracking and management of the mandatory 60-hour pro bono legal service rendered by law student-practitioners.

---

## 📌 Purpose

This platform ensures:

- Proper documentation of legal aid hours  
- Easy access and submission of reports by student-practitioners  
- Streamlined monitoring for administrators  
- Compliance with legal education program mandates  

---

## 👥 User Roles and Responsibilities

### Superuser

- Full administrative access to all system features  
- Manages all user accounts and roles  
- Can assign admin privileges or deactivate users  
- Accesses the Superuser Account Management page  

### Admin

- Reviews and manages user-submitted activities  
- Approves or rejects submitted activities with proper documentation  
- Accesses the Admin Dashboard and User Management views  

### Regular User

- Registers for an account with basic information  
- Verifies email via a one-time passcode (OTP)  
- Completes profile with personal and academic details  
- Submits detailed reports of legal activities  
- Monitors status of submissions and cumulative hours  

---

## ⚙️ Core Functional Features

| Feature                 | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| Registration            | New users can register with name, email, and password                       |
| Email Verification      | A 6-digit OTP code is sent to the user’s email to confirm identity          |
| Secure Login            | Verified users can securely access their dashboard                          |
| Profile Management      | Users fill out additional personal, academic, and professional details       |
| Activity Submission     | Submit legal activities via structured forms with required data             |
| Admin Approval Workflow | Admins approve or reject submissions with proper reasoning                  |
| Dashboard Access        | View activity history, status, and hours rendered                           |
| Password Reset          | Users can reset passwords through a 3-step verification flow                |
| Superuser Management    | Superusers can manage user accounts and roles                               |

---


## 🔄 System Workflow Summary

- Registration requires verified email before login  
- Profile must be completed before dashboard access  
- All submissions default to "Pending"  
- Admins manually approve or reject activities  
- Users with 60+ approved hours are flagged for review  
- Uploaded files are stored in `/media/proofs/`  
- Password reset uses email + OTP code  


