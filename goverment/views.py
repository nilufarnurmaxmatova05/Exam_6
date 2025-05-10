from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.urls import reverse

from Exam_6 import settings
from .forms import MinistryForm, MinisterForm, DepartmentForm, UserRegistrationForm, UserProfileForm
from .models import Ministry, Minister, Department, UserProfile, PasswordResetCode
import logging

# Logger sozlamalari
logger = logging.getLogger(__name__)


def index(request):
    ministries = Ministry.objects.all()[:5]
    ministers = Minister.objects.all()[:5]
    return render(request, 'government/index.html', {
        'ministries': ministries,
        'ministers': ministers,
    })


# Ministry views
def ministry_list(request):
    query = request.GET.get('q', '')
    if query:
        ministries = Ministry.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        ministries = Ministry.objects.all()
    return render(request, 'government/ministry_list.html', {'ministries': ministries, 'query': query})


def ministry_detail(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    ministers = ministry.ministers.all()
    departments = ministry.departments.all()
    return render(request, 'government/ministry_detail.html', {
        'ministry': ministry,
        'ministers': ministers,
        'departments': departments,
    })


@login_required
def ministry_create(request):
    if request.method == 'POST':
        try:
            form = MinistryForm(request.POST, request.FILES)
            logger.debug(f"Form data: {request.POST}")
            logger.debug(f"Files: {request.FILES}")

            if form.is_valid():
                with transaction.atomic():
                    ministry = form.save()
                    logger.info(f"Ministry created with ID: {ministry.id}")
                    messages.success(request, "Vazirlik muvaffaqiyatli qo'shildi.")
                    return redirect('ministry_list')
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error creating ministry: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = MinistryForm()

    return render(request, 'government/ministry_form.html', {'form': form, 'action': 'Qo\'shish'})


@login_required
def ministry_update(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    if request.method == 'POST':
        try:
            form = MinistryForm(request.POST, request.FILES, instance=ministry)
            logger.debug(f"Form data: {request.POST}")
            logger.debug(f"Files: {request.FILES}")

            if form.is_valid():
                with transaction.atomic():
                    updated_ministry = form.save()
                    logger.info(f"Ministry updated with ID: {updated_ministry.id}")
                    messages.success(request, "Vazirlik ma'lumotlari muvaffaqiyatli yangilandi.")
                    return redirect('ministry_detail', pk=updated_ministry.pk)
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error updating ministry: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = MinistryForm(instance=ministry)

    return render(request, 'government/ministry_form.html', {'form': form, 'action': 'Tahrirlash'})


@login_required
def ministry_delete(request, pk):
    ministry = get_object_or_404(Ministry, pk=pk)
    if request.method == 'POST':
        try:
            ministry_name = ministry.name
            with transaction.atomic():
                ministry.delete()
                logger.info(f"Ministry deleted: {ministry_name}")
                messages.success(request, f"Vazirlik '{ministry_name}' muvaffaqiyatli o'chirildi.")
                return redirect('ministry_list')
        except Exception as e:
            logger.error(f"Error deleting ministry: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect('ministry_detail', pk=pk)

    return render(request, 'government/ministry_confirm_delete.html', {'ministry': ministry})


# Minister views
def minister_list(request):
    query = request.GET.get('q', '')
    if query:
        ministers = Minister.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(position__icontains=query) |
            Q(ministry__name__icontains=query)
        )
    else:
        ministers = Minister.objects.all()
    return render(request, 'government/minister_list.html', {'ministers': ministers, 'query': query})


def minister_detail(request, pk):
    minister = get_object_or_404(Minister, pk=pk)
    return render(request, 'government/minister_detail.html', {'minister': minister})


@login_required
def minister_create(request):
    if request.method == 'POST':
        try:
            form = MinisterForm(request.POST, request.FILES)
            if form.is_valid():
                with transaction.atomic():
                    minister = form.save()
                    logger.info(f"Minister created with ID: {minister.id}")
                    messages.success(request, "Vazir muvaffaqiyatli qo'shildi.")
                    return redirect('minister_list')
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error creating minister: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = MinisterForm()

    return render(request, 'government/minister_form.html', {'form': form, 'action': 'Qo\'shish'})


@login_required
def minister_update(request, pk):
    minister = get_object_or_404(Minister, pk=pk)
    if request.method == 'POST':
        try:
            form = MinisterForm(request.POST, request.FILES, instance=minister)
            if form.is_valid():
                with transaction.atomic():
                    updated_minister = form.save()
                    logger.info(f"Minister updated with ID: {updated_minister.id}")
                    messages.success(request, "Vazir ma'lumotlari muvaffaqiyatli yangilandi.")
                    return redirect('minister_detail', pk=updated_minister.pk)
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error updating minister: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = MinisterForm(instance=minister)

    return render(request, 'government/minister_form.html', {'form': form, 'action': 'Tahrirlash'})


@login_required
def minister_delete(request, pk):
    minister = get_object_or_404(Minister, pk=pk)
    if request.method == 'POST':
        try:
            minister_name = minister.full_name
            with transaction.atomic():
                minister.delete()
                logger.info(f"Minister deleted: {minister_name}")
                messages.success(request, f"'{minister_name}' muvaffaqiyatli o'chirildi.")
                return redirect('minister_list')
        except Exception as e:
            logger.error(f"Error deleting minister: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect('minister_detail', pk=pk)

    return render(request, 'government/minister_delete.html', {'minister': minister})


# Department views
def department_list(request):
    query = request.GET.get('q', '')
    if query:
        departments = Department.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ministry__name__icontains=query)
        )
    else:
        departments = Department.objects.all()
    return render(request, 'government/department_list.html', {'departments': departments, 'query': query})


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'government/department_detail.html', {'department': department})


@login_required
def department_create(request):
    if request.method == 'POST':
        try:
            form = DepartmentForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    department = form.save()
                    logger.info(f"Department created with ID: {department.id}")
                    messages.success(request, "Bo'lim muvaffaqiyatli qo'shildi.")
                    return redirect('department_list')
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error creating department: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = DepartmentForm()

    return render(request, 'government/department_form.html', {'form': form, 'action': 'Qo\'shish'})


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        try:
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                with transaction.atomic():
                    updated_department = form.save()
                    logger.info(f"Department updated with ID: {updated_department.id}")
                    messages.success(request, "Bo'lim ma'lumotlari muvaffaqiyatli yangilandi.")
                    return redirect('department_detail', pk=updated_department.pk)
            else:
                logger.warning(f"Form validation errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error updating department: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'government/department_form.html', {'form': form, 'action': 'Tahrirlash'})


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        try:
            department_name = department.name
            with transaction.atomic():
                department.delete()
                logger.info(f"Department deleted: {department_name}")
                messages.success(request, f"Bo'lim '{department_name}' muvaffaqiyatli o'chirildi.")
                return redirect('department_list')
        except Exception as e:
            logger.error(f"Error deleting department: {str(e)}")
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect('department_detail', pk=pk)

    return render(request, 'government/department_confirm_delete.html', {'department': department})


# User authentication views
def register(request):
    if request.method == 'POST':
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    user = form.save()
                    UserProfile.objects.create(user=user)
                    logger.info(f"User registered: {user.username}")
                    messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz. Endi tizimga kirishingiz mumkin.")
                    return redirect('login')
            else:
                logger.warning(f"Registration form errors: {form.errors}")
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            messages.error(request, f"Ro'yxatdan o'tishda xatolik yuz berdi: {str(e)}")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


class MyLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def profile(request):
    if request.method == 'POST':
        try:
            user_form = UserRegistrationForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                    logger.info(f"User profile updated: {request.user.username}")
                    messages.success(request, "Profil muvaffaqiyatli yangilandi.")
                    return redirect('profile')
            else:
                logger.warning(f"User form errors: {user_form.errors}")
                logger.warning(f"Profile form errors: {profile_form.errors}")

                for form in [user_form, profile_form]:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            messages.error(request, f"Profilni yangilashda xatolik yuz berdi: {str(e)}")
    else:
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Parol tiklash funksiyasi - kod yuborish
def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Emailni tekshirish
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                logger.warning(f"Password reset attempted for non-existent email: {email}")
                messages.error(request, "Bu email manzili bilan ro'yxatdan o'tgan foydalanuvchi topilmadi.")
                return redirect('password_reset_request')

            # 6 xonali kod yaratish
            reset_code = PasswordResetCode.generate_code(user)
            logger.info(f"Password reset code generated for user: {user.username}")

            # Email yuborish
            subject = "O'zbekiston Respublikasi Hukumati - Parol tiklash kodi"

            # HTML formatidagi xabar
            html_message = render_to_string('registration/password_reset_code_email.html', {
                'user': user,
                'code': reset_code.code,
                'domain': request.get_host(),
                'expires_at': reset_code.expires_at.strftime('%H:%M'),
            })

            # Oddiy matn formatidagi xabar
            plain_message = strip_tags(html_message)

            # Emailni yuborish
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(request, "Parolni tiklash kodi email manzilingizga yuborildi.")
            return redirect('password_reset_verify')
        except Exception as e:
            logger.error(f"Error in password reset request: {str(e)}")
            messages.error(request, f"Parolni tiklash so'rovida xatolik yuz berdi: {str(e)}")

    return render(request, 'registration/password_reset_request.html')


# Parol tiklash kodi tasdiqlash va yangi parol o'rnatish
def reset_password_verify(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            # Kodni tekshirish
            try:
                reset_code = PasswordResetCode.objects.get(code=code, is_used=False)

                # Kod amal qilish muddatini tekshirish
                if not reset_code.is_valid():
                    logger.warning(f"Expired password reset code used: {code}")
                    messages.error(request, "Kod eskirgan. Iltimos, yangi kod so'rang.")
                    return redirect('password_reset_request')

            except PasswordResetCode.DoesNotExist:
                logger.warning(f"Invalid password reset code used: {code}")
                messages.error(request, "Noto'g'ri kod kiritildi.")
                return redirect('password_reset_verify')

            # Parollarni tekshirish
            if password1 != password2:
                messages.error(request, "Parollar mos kelmadi.")
                return render(request, 'registration/password_reset_verify.html', {'code': code})

            if len(password1) < 8:
                messages.error(request, "Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
                return render(request, 'registration/password_reset_verify.html', {'code': code})

            # Parolni yangilash
            with transaction.atomic():
                user = reset_code.user
                user.set_password(password1)
                user.save()

                # Kodni ishlatilgan deb belgilash
                reset_code.is_used = True
                reset_code.save()

                logger.info(f"Password reset successful for user: {user.username}")

            messages.success(request,
                             "Parolingiz muvaffaqiyatli yangilandi. Endi yangi parol bilan tizimga kirishingiz mumkin.")
            return redirect('login')
        except Exception as e:
            logger.error(f"Error in password reset verification: {str(e)}")
            messages.error(request, f"Parolni tiklashda xatolik yuz berdi: {str(e)}")

    return render(request, 'registration/password_reset_verify.html')