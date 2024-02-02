from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core.mail import send_mail
from adminuser.models import Packages,Maritalstatus,Religion,Cast,Usermember,Image,Payment
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User,auth
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta
import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
import re

def home(request):
    return render(request,'home.html')
def login_view(request):
    return render(request,'login.html')
def signup(request):
    ms = Maritalstatus.objects.all()
    religion = Religion.objects.all()
    casts = Cast.objects.all()
    return render(request,'signup.html',{'ms':ms,'religion':religion,'casts':casts})
def adminhome(request):
    pending_user=Usermember.objects.filter(is_approved=False)
    pc=pending_user.count()
    return render(request,'adminhome.html',{'pc':pc})
def logincheck(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        usr = authenticate(request, username=username, password=password)

        if usr is not None:
            if usr.is_staff:
                login(request, usr)
                return redirect('adminhome')
            elif usr.is_active:
                um = Usermember.objects.get(user=usr)
                pkg = Payment.objects.get(user=um)
                date_joined = um.Joining_date
                current_date = datetime.now().date()
                days_since_joining = (current_date - date_joined).days

                if days_since_joining >= 10:
                    messages.info(request, "Your package has expired. Please renew your package.")
                    return render(request, 'renew_package.html', {'user': um, 'pkg': pkg})
                else:
                    auth.login(request, usr)
                    request.session['user_id'] = usr.id
                    return redirect('userhome')
            else:
                messages.info(request, "Your account is not active.")
                return redirect('login_view')
        else:
            messages.info(request, "Invalid username or password. Try again!")
            return redirect('login_view')
def  addpackage(request):
    return render(request,'package.html')
def packageadd(request):
     if request.method == 'POST':
        n=request.POST['pname']
        d = request.POST['description']
        f = request.POST['fee']
        
        pkg = Packages(Package_name=n,Package_description=d,Package_fee=f)
        pkg.save()
        messages.success(request, 'Package added successfully!')
        return redirect('addpackage')
def package_details(request):
    pkg = Packages.objects.all()
    return render(request,'package_details.html',{'pkg':pkg})
def edit_package(request,id):
    pkg = Packages.objects.get(id=id)
    return render(request,'edit_package.html',{'pkg':pkg})
def update_package(request,id):
   pkg = Packages.objects.get(id=id)
   if request.method == 'POST':
        pkg.Package_name_name = request.POST['pname']
        pkg.Package_description= request.POST['description']
        pkg.Package_fee = request.POST['fee']
        pkg.save()
        return redirect('package_details')
   
def delete_package(request,id):
    pkg = Packages.objects.get(id=id)
    
    pkg.delete()
    
    return redirect('package_details')
def package_view(request):
    pkg = Packages.objects.all()
    
    return render(request,'package_view.html',{'pkg':pkg})

def validate_mobile_number(mobile_number):
    
    mobile_number_regex = r'^\+?1?\d{9,15}$'

    
    return bool(re.match(mobile_number_regex, mobile_number))
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))
def adduser(request):
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        un = request.POST['uname']
        status = request.POST['status']
        age = request.POST['age']
        height = request.POST['height']
        gender = request.POST['gender']
        email = request.POST['email']
        place = request.POST['place']
        district = request.POST['district']
        designation = request.POST['designation']
        contact = request.POST['contact']
        rel = request.POST['religion']
        religion = Religion.objects.get(id=rel)
        ct = request.POST['cast']
        cast = Cast.objects.get(id=ct)
        fan = request.POST['father_name']
        fo = request.POST['father_occupation']
        mn = request.POST['mother_name']
        mo = request.POST['mother_occupation']
        sn = request.POST['sibling_name']
        ss = request.POST['sb_status']
        jd = request.POST['joining_date']
        images = request.FILES.getlist('image')
        

        # Check if email is in the correct format
        if not is_valid_email(email):
            messages.error(request, "Invalid email address. Please enter a valid email.")
            return redirect('signup')

        # Check if mobile number is in the correct format
        if not validate_mobile_number(contact):
            messages.error(request, "Invalid mobile number. Please enter a valid mobile number.")
            return redirect('signup')

        # Check if the username already exists
        if User.objects.filter(username=un).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('signup')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address already exists. Please use a different email.")
            return redirect('signup')

        # Create user and usermember if all checks pass
        user = User.objects.create_user(
            first_name=fn,
            last_name=ln,
            email=email,
            username=un,
            
        )
        user.save()
        um = Usermember(user=user,Status=status,Age=age,Height=height,Gender=gender,Place=place,District=district,Designation=designation,Contact=contact,religion=religion,cast=cast,Father_name=fan,Father_occupation=fo,Mother_name=mn,Mother_occupation=mo,Sibling_name=sn,Sibling_status=ss,Joining_date=jd )
        for image in images:
            um.Image=image
        um.save()
        for image in images:
            image_instance = Image.objects.create(image=image)
            um.images.add(image_instance)

        request.session['user_id'] = user.id
        return redirect('package_view')
    
def payment(request,id):
    pkg = Packages.objects.get(id=id)
    
    user_id = request.session.get('user_id')
    user = Usermember.objects.get(user=user_id)
    user.expiry_date = user.Joining_date + timedelta(days=10)
    return render(request,'payment.html',{'pkg':pkg,'user':user})
def payment_success(request,id):
    if request.method == 'POST':
        pay = request.POST['pay']
        user_id = request.session.get('user_id')
        user = Usermember.objects.get(user=user_id)
        pkg = Packages.objects.get(id=id)
        payment, created = Payment.objects.get_or_create(user=user, package=pkg, defaults={'Payment_method': pay})

    
        if not created:
            payment.Payment_method = pay
            payment.save()
            payment.save()
        
        email = user.user.email
        subject="Registration succesfull!"        
        send_mail(subject,"Registration Succesfull! Your profile is checked and varified by the admin shorltly!",settings.EMAIL_HOST_USER,[email])
       
        return render(request,'payment_success.html')
def approve(request):
    pending_users = Usermember.objects.filter(is_approved=False)
    return render(request, 'approve.html', {'pu': pending_users})
def approve_user(request,id):
      user_member = Usermember.objects.get(user=id)
      user = User.objects.get(id=id)
      user_member.is_approved = True
      
      if user_member.is_approved:
           password =str(random.randint(100000,9999999))
           member_id =str(random.randint(1000,9999)) 
           email = user_member.user.email
           subject ='Your account approved'
           message =  f'Your account has been approved.\nUsername: {user_member.user.username}\nPassword: {password}\nMember ID:{member_id}'
           send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
           user.set_password(password)
           user_member.Member_id=member_id
           user_member.save()   
           user.save()         
      return redirect('approve')
def disapprove_user(request,id):
    user_member=Usermember.objects.get(user=id)
    user_member.delete()
    user_member.user.delete()
    return redirect('approve')
def user_record(request):
    users = Usermember.objects.filter(is_approved=True)
    for user in users:
        user.expiry_date = user.Joining_date + timedelta(days=10)
    return render(request,'user_record.html',{'users':users})
def delete_user(request,id):
    user_member = Usermember.objects.get(user=id)
    user_member.delete()
    user_member.user.delete()
    return redirect(user_record)
def logout(request):
    auth.logout(request)
    return redirect('home')
def renew_success(request,uid,pid):
    if request.method == 'POST':
        pay = request.POST['pay']
       
        user = Usermember.objects.get(user=uid)
        pkg = Packages.objects.get(id=pid)
       
        existing_payment = Payment.objects.filter(user=user).first()

        if existing_payment:
            user.Joining_date = timezone.now().date()
            user.save()
        else:
            payment = Payment(Payment_method=pay, user=user, package=pkg)
            payment.save()

        return render(request, 'renew_success.html')
        
    


    


