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

## 📘 Step-by-Step Usage Guide

### For Regular Users

1. **Registration**
   - Visit `/register/`
   - Fill in name, email, and password
   - Submit and wait for email verification

2. **Email Verification**
   - Visit `/verify-email/`
   - Enter the 6-digit OTP code from the email

3. **Login**
   - Visit `/login/`
   - Enter your email/username and password

4. **Profile Completion**
   - Go to `/profile/edit/`
   - Complete the required fields and upload a profile photo
   - Click **Save**

5. **Submit Legal Activity**
   - Go to `/submit-activity/`
   - Choose activity type or select "Other"
   - Fill out the activity details and upload proof image
   - Agree to the declaration and submit

6. **Dashboard Access**
   - Visit `/dashboard/` to view total approved hours and track submission status

7. **Password Reset**
   - Go to `/custom-password-reset/` and enter email
   - Enter OTP at `/custom-password-reset/code/`
   - Set new password at `/custom-password-reset/set/`

### For Admins

1. **User Management**
   - Visit `/admin/users/`
   - View profiles and submissions

2. **Activity Review**
   - Open submissions under each user
   - Click **Approve** or **Reject** with reason

3. **Dashboard Monitoring**
   - Go to `/admin/dashboard/`
   - Monitor metrics and review candidates for approval

### For Superusers

1. **Manage Accounts**
   - Navigate to `/superuser/manage-accounts/`
   - Perform actions: view all users, modify roles, deactivate/reset accounts

---

## 🔄 System Workflow Summary

- Registration requires verified email before login  
- Profile must be completed before dashboard access  
- All submissions default to "Pending"  
- Admins manually approve or reject activities  
- Users with 60+ approved hours are flagged for review  
- Uploaded files are stored in `/media/proofs/`  
- Password reset uses email + OTP code  

---

## 📌 Notes and Reminders

- **Do not upload confidential client data** in proof images or descriptions  
- Submissions missing data or valid proof will not be approved  
- Email verification is mandatory for login  
- **Only trusted users should be given admin access**  

---

## 👨‍💻 Developers

Developed by BSIT students of Xavier University:

- **Brett Rainiel Espiritu** – Project Leader  
- **Emilio Rafael A. Rubio** – Assistant Leader  
- **Nathaniel Enguio** – Documentation & Frontend  
- **Kian Francis A. Porras** – Backend Support  
- **Karlos Miguel R. Hiponia** – UI/UX & Routing  
- **Dave Justine B. Go** – Database Integration  

---

## 🏫 Institution

**Xavier University – Ateneo de Cagayan**  
College of Computer Studies & College of Law  
BSIT Capstone / Project-Based Subject  

---

## 📄 License

This project is for academic and educational purposes only. Contact the developers for reuse or deployment permission.

---

