from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache

from .forms import RegisterForm, LoginForm, ActivityForm, UserProfileForm, PasswordResetRequestForm, PasswordResetCodeForm, PasswordResetSetForm
from .models import UserProfile, Activity, VerificationCode, PasswordResetCode

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Activity

def home(request):
    services = [
        {
            "title": "XUCLA",
            "description": "Xavier University Center for Legal Assistance.",
            "image_url": "images/XUCLALOGO.png",
            "link": "https://docs.google.com/forms/d/e/1FAIpQLSfdpXdIxgsakeEvda7KVLl0mLdzj7T63MpXhNQxTocVb_W8XQ/viewform"
        },
        {
            "title": "ULAS",
            "description": "Unified Legal Aid Service.",
            "image_url": "images/ulas.png",
            "link": ""
        },
    ]
    return render(request, "xucla/home.html", {"services": services})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('superuser_manage_accounts')
        elif request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_obj = None
            try:
                user_obj = User.objects.get(email=identifier)
            except User.DoesNotExist:
                try:
                    user_obj = User.objects.get(username=identifier)
                except User.DoesNotExist:
                    user_obj = None
            if user_obj and not user_obj.is_active:
                verification_code, created = VerificationCode.objects.get_or_create(user=user_obj)
                verification_code.code = VerificationCode.generate_code()
                verification_code.save()
                send_verification_email(user_obj, verification_code.code)
                request.session['email'] = user_obj.email
                messages.info(request, 'Your account is not yet verified. A new verification code has been sent to your email.')
                return redirect('verify_email')
            user = None
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('superuser_manage_accounts')
                elif user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_profile')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'xucla/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def send_verification_email(user, code):
    subject = 'XUCLA - Email Verification Required'
    context = {
        'full_name': user.get_full_name() or user.username,
        'code': code,
    }
    html_message = render_to_string('xucla/email_verification.html', context)
    plain_message = f"Dear {context['full_name']},\n\nThank you for registering with the Xavier University Center for Legal Assistance (XUCLA) platform.\n\nTo complete your registration and access our legal assistance services, please use the following verification code:\n\n{code}\n\nThis verification code will expire in 10 minutes for security purposes.\n\nIf you did not request this registration, please disregard this email.\n\nBest regards,\nXUCLA Administration\nXavier University Center for Legal Assistance"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                existing_user = User.objects.get(email=email)
                if not existing_user.is_active:
                    verification_code, created = VerificationCode.objects.get_or_create(user=existing_user)
                    verification_code.code = VerificationCode.generate_code()
                    verification_code.save()
                    send_verification_email(existing_user, verification_code.code)
                    request.session['email'] = email
                    messages.info(request, 'This email is already registered but not yet verified. A new verification code has been sent to your email.')
                    return redirect('verify_email')
                else:
                    messages.error(request, "This email address is already registered. Please use a different email or try logging in.")
                    return render(request, 'xucla/register.html', {'form': form})
            except User.DoesNotExist:
                pass
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.is_active = False
                user.save()
                profile = UserProfile.objects.create(
                    user=user,
                    nickname=request.POST.get('nickname', ''),
                    year_admitted=request.POST.get('year_admitted', ''),
                    office_name=request.POST.get('office_name', ''),
                    law_school=request.POST.get('law_school', ''),
                    work_cell=request.POST.get('work_cell', ''),
                    roll_number=request.POST.get('roll_number', ''),
                    sector=request.POST.get('sector', ''),
                    office_address=request.POST.get('office_address', ''),
                    profile_picture=request.FILES.get('profile_picture')
                )
                verification_code = VerificationCode.objects.create(
                    user=user,
                    code=VerificationCode.generate_code()
                )
                send_verification_email(user, verification_code.code)
                request.session['email'] = email
                messages.success(request, 'Registration successful! Please check your email for verification code.')
                return redirect('verify_email')
            except Exception as e:
                if 'user' in locals():
                    user.delete()
                messages.error(request, "An error occurred during registration. Please try again.")
                return render(request, 'xucla/register.html', {'form': form})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'xucla/register.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            verification = VerificationCode.objects.get(user__email=request.session.get('email'))
            if verification.verify(code):
                user = verification.user
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, 'Email verified successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid or expired verification code.')
        except VerificationCode.DoesNotExist:
            messages.error(request, 'Invalid verification attempt.')
    return render(request, 'xucla/verify_email.html')

def resend_verification(request):
    email = request.session.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            verification = VerificationCode.objects.get(user=user)
            verification.code = VerificationCode.generate_code()
            verification.save()
            send_verification_email(user, verification.code)
            messages.success(request, 'Verification code has been resent to your email.')
        except (User.DoesNotExist, VerificationCode.DoesNotExist):
            messages.error(request, 'Invalid email address.')
    return redirect('verify_email')

@login_required
def dashboard_view(request):
    activity_filter = request.GET.get("activity_type")
    if activity_filter and activity_filter != "All":
        activities = Activity.objects.filter(user=request.user, activity_type=activity_filter, status='approved').order_by('-date')
    else:
        activities = Activity.objects.filter(user=request.user).order_by('-date')
    total_hours = sum(a.hours_rendered for a in activities)
    activity_dates = [a.date.strftime('%Y-%m-%d') for a in activities]
    activity_hours = [a.hours_rendered for a in activities]
    all_activities = Activity.objects.filter(user=request.user, status='approved')
    total_hours_all = sum(a.hours_rendered for a in all_activities)
    return render(request, "xucla/dashboard.html", {
        "activities": activities,
        "filter": activity_filter,
        "total_hours": total_hours,
        "activity_dates": activity_dates,
        "activity_hours": activity_hours,
        "total_hours_all": total_hours_all,
    })

@login_required
def activity_form_view(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.status = 'pending'
            activity.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('dashboard')
    else:
        form = ActivityForm()
    return render(request, 'xucla/activity_form.html', {'form': form})

@login_required
def user_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'xucla/user_profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'xucla/edit_profile.html', {'form': form, 'profile': profile})

@staff_member_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'xucla/admin_user_list.html', {'users': users})

@staff_member_required
def admin_user_detail(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = UserProfile.objects.filter(user=user).first()
    activities = Activity.objects.filter(user=user).order_by('-date')
    approved_activities = activities.filter(status='approved')
    total_hours = sum(a.hours_rendered for a in approved_activities)
    profiles = UserProfile.objects.select_related('user')
    user_hours = {}
    for p in profiles:
        user_hours[p.user.id] = Activity.objects.filter(
            user=p.user,
            status='approved'
        ).aggregate(Sum('hours_rendered'))['hours_rendered__sum'] or 0
    pending_profiles = [
        p for p in profiles
        if ((user_hours[p.user.id] < 60) or (user_hours[p.user.id] >= 60 and not p.is_approved))
        and p.user.is_active
        and (p.user.first_name or p.user.last_name or p.user.email)
        and not p.user.is_staff
        and not p.user.is_superuser
    ]
    completed_profiles = [
        p for p in profiles
        if user_hours[p.user.id] >= 60
        and p.is_approved
        and p.user.is_active
        and (p.user.first_name or p.user.last_name or p.user.email)
        and not p.user.is_staff
        and not p.user.is_superuser
    ]
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            profile.is_approved = True
            profile.save()
            subject = 'XUCLA - 60 Hours Fulfilled & Approved'
            context = {
                'full_name': user.get_full_name() or user.username,
                'email': user.email,
                'hours': total_hours,
            }
            html_message = render_to_string('xucla/email_approval.html', context)
            plain_message = (
                f"Dear {context['full_name']},\n\n"
                "Congratulations! You have been approved and have fulfilled your 60 hours of service. "
                "Thank you for your dedication to the Unified Legal Aid Service (ULAS).\n\n"
                "Best regards,\n"
                "XUCLA Administration\n"
                "Xavier University Center for Legal Assistance"
            )
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message
            )
            messages.success(request, 'User approved successfully!', extra_tags='admin_action')
            return redirect('admin_user_detail', user_id=user.id)
        elif action == 'reject':
            reason = request.POST.get('rejection_reason', '').strip()
            profile.is_approved = False
            profile.save()
            subject = 'XUCLA - Approval Not Granted'
            context = {
                'full_name': user.get_full_name() or user.username,
                'email': user.email,
                'reason': reason,
            }
            html_message = render_to_string('xucla/email_rejection.html', context)
            plain_message = (
                f"Dear {context['full_name']},\n\n"
                f"We regret to inform you that your approval was not granted. Reason: {reason}\n\n"
                "Please contact the XUCLA Administration for any concerns or inquiries.\n\n"
                "Best regards,\n"
                "XUCLA Administration\n"
                "Xavier University Center for Legal Assistance"
            )
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message
            )
            messages.success(request, 'User marked as not approved and notified.', extra_tags='admin_action')
            return redirect('admin_user_detail', user_id=user.id)
    return render(request, 'xucla/admin_user_detail.html', {
        'user_obj': user,
        'profile': profile,
        'activities': activities,
        'total_hours': total_hours,
        'pending_profiles': pending_profiles,
        'completed_profiles': completed_profiles,
        'user_hours': user_hours,
    })

@staff_member_required
def admin_dashboard(request):
    profiles = UserProfile.objects.select_related('user')
    user_hours = {}
    notifications = []
    for profile in profiles:
        total_hours = Activity.objects.filter(user=profile.user, status='approved').aggregate(Sum('hours_rendered'))['hours_rendered__sum'] or 0
        user_hours[profile.user.id] = total_hours
        if total_hours >= 60 and not profile.is_approved:
            notifications.append(f"{profile.user.first_name} {profile.user.last_name} has now 60 hours of work")
    pending_profiles = [p for p in profiles if ((user_hours[p.user.id] < 60) or (user_hours[p.user.id] >= 60 and not p.is_approved)) and p.user.is_active and (p.user.first_name or p.user.last_name or p.user.email) and not p.user.is_staff and not p.user.is_superuser]
    completed_profiles = [p for p in profiles if user_hours[p.user.id] >= 60 and p.is_approved and p.user.is_active and (p.user.first_name or p.user.last_name or p.user.email) and not p.user.is_staff and not p.user.is_superuser]
    user_count = profiles.exclude(user__is_staff=True).exclude(user__is_superuser=True).count()
    pending_count = len(pending_profiles)
    completed_count = len(completed_profiles)
    return render(request, 'xucla/admin_dashboard.html', {
        'pending_profiles': pending_profiles,
        'completed_profiles': completed_profiles,
        'user_hours': user_hours,
        'user_count': user_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'notifications': notifications,
    })

@user_passes_test(lambda u: u.is_superuser)
def superuser_manage_accounts(request):
    users = User.objects.all()
    admins = User.objects.filter(is_staff=True)
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        if action == 'delete_user' and user_id:
            User.objects.filter(pk=user_id).delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('superuser_manage_accounts')
        if action == 'make_admin' and user_id:
            user = User.objects.get(pk=user_id)
            user.is_staff = True
            user.save()
            messages.success(request, 'User promoted to admin!')
            return redirect('superuser_manage_accounts')
        if action == 'remove_admin' and user_id:
            user = User.objects.get(pk=user_id)
            user.is_staff = False
            user.save()
            messages.success(request, 'Admin rights removed!')
            return redirect('superuser_manage_accounts')
    return render(request, 'xucla/superuser_manage_accounts.html', {'users': users, 'admins': admins})

@ratelimit(key='post:email', rate='10/h', block=True)
def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_user_model().objects.get(email=email)
                code = PasswordResetCode.generate_code()
                PasswordResetCode.objects.create(user=user, code=code)
                subject = 'Your XUCLA Password Reset Code'
                context = {
                    'full_name': user.get_full_name() or user.username,
                    'code': code,
                }
                html_message = render_to_string('xucla/email_password_reset_code.html', context)
                message = f"Dear {context['full_name']},\n\nYour password reset code is: {code}\n\nThis code will expire in 10 minutes."
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, html_message=html_message)
                request.session['reset_email'] = email
                messages.success(request, 'If an account exists with that email, a reset code has been sent.')
                return redirect('password_reset_code')
            except get_user_model().DoesNotExist:
                messages.success(request, 'If an account exists with that email, a reset code has been sent.')
                return redirect('password_reset_code')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'xucla/custom_password_reset_request.html', {'form': form})

@ratelimit(key='post:session', rate='10/h', block=True)
def password_reset_code_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset_request')
    lockout_key = f"reset_code_lockout_{email}"
    failed_attempts = cache.get(lockout_key, 0)
    if failed_attempts >= 5:
        messages.error(request, 'Too many failed attempts. Please try again in 1 hour.')
        return redirect('password_reset_request')
    if request.method == 'POST':
        form = PasswordResetCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = get_user_model().objects.get(email=email)
                reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).last()
                if reset_code and not reset_code.is_expired():
                    request.session['reset_code'] = code
                    cache.set(lockout_key, 0, 3600)
                    return redirect('password_reset_set')
                else:
                    failed_attempts += 1
                    cache.set(lockout_key, failed_attempts, 3600)
                    messages.error(request, f'Invalid or expired code. {5 - failed_attempts} attempts remaining.')
            except get_user_model().DoesNotExist:
                messages.error(request, 'Invalid or expired code.')
    else:
        form = PasswordResetCodeForm()
    return render(request, 'xucla/custom_password_reset_code.html', {'form': form, 'email': email})

def password_reset_set_view(request):
    email = request.session.get('reset_email')
    code = request.session.get('reset_code')
    if not (email and code):
        messages.error(request, 'Invalid or expired reset session. Please try again.')
        return redirect('password_reset_request')
    try:
        user = get_user_model().objects.get(email=email)
        reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).last()
        if not reset_code or reset_code.is_expired():
            messages.error(request, 'Invalid or expired code.')
            return redirect('password_reset_code')
    except get_user_model().DoesNotExist:
        messages.error(request, 'Invalid or expired code.')
        return redirect('password_reset_request')
    if request.method == 'POST':
        form = PasswordResetSetForm(user, request.POST)
        if form.is_valid():
            form.save()
            reset_code.is_used = True
            reset_code.save()
            subject = 'Your XUCLA password was changed'
            context = {
                'full_name': user.get_full_name() or user.username,
            }
            html_message = render_to_string('xucla/email_password_changed.html', context)
            message = 'This is a notification that your password was just changed. If you did not do this, please contact support immediately.'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message
            )
            messages.success(request, 'Your password has been reset. You may now log in.')
            return redirect('login')
    else:
        form = PasswordResetSetForm(user)
    return render(request, 'xucla/custom_password_reset_set.html', {
        'form': form,
        'email': email
    })
@staff_member_required
def approve_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.status = 'approved'
    activity.save()
    messages.success(request, 'Activity approved.')
    return redirect('admin_user_detail', user_id=activity.user.id)

@staff_member_required
def reject_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.status = 'rejected'
    activity.save()
    messages.success(request, 'Activity rejected.')
    return redirect('admin_user_detail', user_id=activity.user.id)
