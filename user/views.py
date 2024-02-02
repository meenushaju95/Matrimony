from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.core.mail import send_mail
from adminuser.models import Packages,Maritalstatus,Religion,Cast,Usermember,Image,Payment
from user.models import Visitor,Message,Message_Request
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User,auth
from datetime import timedelta
from django.utils import timezone 

import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
import re
from datetime import datetime
from django.db.models import Q


def userhome(request):
    user = Usermember.objects.get(user=request.user)
    um = Usermember.objects.get(user=request.user)
    um.expiry_date = user.Joining_date + timedelta(days=10)
    msgc = Message.objects.filter(Receiver=um,is_read=False).count()
    msgrq = Message_Request.objects.filter(Receiver=um,is_read=False).count()
    mqn = Message_Request.objects.filter(Sender=user,is_accept=True,is_notify=False).count()
    pay  = Payment.objects.get(user=user)
    return render(request,'userhome.html',{'user':user,'msg':msgc,'pay':pay,'um':um,'mr':msgrq,'mqn':mqn})
def logout(request):
    auth.logout(request)
    return redirect('home')
def showuser(request):
    users = Usermember.objects.get(user=request.user)
    return render(request,'showuser.html',{'user':users})
def user_details(request,id):
    users = Usermember.objects.get(id=id)
    return render(request,'user_datails.html',{'user':users})
def edit_user(request,id):
    usr = Usermember.objects.get(id=id)
    religion = Religion.objects.all()
    casts = Cast.objects.all()
    ms = Maritalstatus.objects.all()
    return render(request,'edit_user.html',{'user':usr,'religion':religion,'casts':casts,'ms':ms})
def validate_mobile_number(mobile_number):
    
    mobile_number_regex = r'^\+?1?\d{9,15}$'

    
    return bool(re.match(mobile_number_regex, mobile_number))
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))
def update_user(request,id):
    if request.method == 'POST':
        ur = Usermember.objects.get(id=id)
        ur.user.first_name = request.POST['fname']
        ur.user.last_name = request.POST['lname']
        ur.user.username = request.POST['uname']
        ur.Status = request.POST['status']
        ur.Age = request.POST['age']
        ur.Height = request.POST['height']
        ur.Gender = request.POST['gender']
        ur.user.email = request.POST['email']
        ur.Place = request.POST['place']
        ur.District = request.POST['district']
        ur.Designation = request.POST['designation']
        ur.Contact = request.POST['contact']
        rel = request.POST['religion']
        religion = Religion.objects.get(id=rel)
        ur.religion=religion
        ct = request.POST['cast']
        cast = Cast.objects.get(id=ct)
        ur.cast=cast
        ur.Father_name = request.POST['father_name']
        ur.Father_occupation = request.POST['father_occupation']
        ur.Mother_name = request.POST['mother_name']
        ur.Mother_occupation = request.POST['mother_occupation']
        ur.Sibling_name = request.POST['sibling_name']
        ur.Sibling_status = request.POST['sb_status']
        if not is_valid_email(ur.user.email):
                messages.error(request, "Invalid email address.")
                return redirect('edit_user',id=id)
 
        if not validate_mobile_number(ur.Contact):
                messages.error(request, "Invalid mobile number. Please enter a valid mobile number.")
                return redirect('edit_user',id=id)
        

        ur.save()
        ur.user.save()
        
        return redirect('showuser')
    
def user_delete(request,id):
    ur = Usermember.objects.get(id=id)
    ur.delete()
    ur.user.delete()
    return redirect('home')
def search_view(request):
    religion = Religion.objects.all()
    casts = Cast.objects.all()
    age_range = range(18,36)
    ms = Maritalstatus.objects.all()
    
    return render(request,'search_view.html',{'religion':religion,'casts':casts,'age_range':age_range,'ms':ms})
def search_profile(request):
    if 'member_id_search' in request.POST:
         try:
            mi = request.POST['memberid']
           
            user = Usermember.objects.get(user=request.user)
            if user.Gender == 'male':
                um = Usermember.objects.get(Member_id=mi,Gender='female')
                return render(request, 'search_profile.html', {'user': um, 'not_found': False})
            elif user.Gender == 'female':
                um = Usermember.objects.get(Member_id=mi,Gender='male')
                return render(request, 'search_profile.html', {'user': um, 'not_found': False})
            else:
                return redirect('search_view')
         except Usermember.DoesNotExist:
        # User with the specified member ID does not exist
            return render(request, 'search_profile.html', {'not_found': True})
    if 'regular_search' in request.POST:
        age_from = int( request.POST.get('agefrom')  )
        age_to =int( request.POST.get('ageto'))
        religion = request.POST.get('religion_regular')  
        cast = request.POST.get('cast_regular')  
        marital_status =  request.POST.get('mstatus')
        print(age_from, age_to, religion, cast, marital_status)

        um = Usermember.objects.get(user=request.user)
        gd = um.Gender
        
        if um.Gender == 'male':
            users = Usermember.objects.filter(Gender='female',religion=religion,cast=cast,Age__gte=age_from,Age__lte=age_to,Status=marital_status)
            print(users)
           
            
            
            return render(request, 'search_profiless.html', {'users': users})
        elif um.Gender == 'female':
            
            
            profiles = Usermember.objects.filter(Gender='male',religion=religion,cast=cast,Age__gte=age_from,Age__lte=age_to,Status=marital_status)
            return render(request, 'search_profiless.html', {'users': profiles})
        else:
            return redirect('search_view')

        

    
    if 'advance_search' in request.POST:
        age_from = int( request.POST.get('agefrom')  )
        age_to =int( request.POST.get('ageto'))
        religion = request.POST.get('religion_advanced')  
        cast = request.POST.get('cast_advanced')  
        marital_status =  request.POST.get('mstatus')
        dst = request.POST.get('district')

        um = Usermember.objects.get(user=request.user)
        
        
        if um.Gender == 'male':
            users = Usermember.objects.filter(Gender='female',religion=religion,cast=cast,Age__gte=age_from,Age__lte=age_to,Status=marital_status,District=dst)
            print(users)
           
            
            
            return render(request, 'search_profiless.html', {'users': users})
        elif um.Gender == 'female':
            
            
            profiles = Usermember.objects.filter(Gender='male',religion=religion,cast=cast,Age__gte=age_from,Age__lte=age_to,Status=marital_status,District=dst)
            return render(request, 'search_profiless.html', {'users': profiles})
        else:
            return redirect('search_view')

        

    return redirect('search_view')

   

   

def user_search_details(request,id):
    user = Usermember.objects.get(id=id)
    return render(request,'user_search_details.html',{'user':user})
def user_profile_advance(request,id):
    visited_user = get_object_or_404(Usermember, id=id)
    visitor_user = Usermember.objects.get(user=request.user)

    time = timezone.localtime(timezone.now())
    
    visitor_record = Visitor.objects.filter(Visited=visited_user, Visitor=visitor_user).first()

    if visitor_record:
       
        visitor_record.Time = time
        visitor_record.save()
    else:
        
        vi=Visitor(Visited=visited_user, Visitor=visitor_user, Time=time)
        vi.save()
    try:
         msgrq = Message_Request.objects.get(
            (Q(Sender=visitor_user) & Q(Receiver=visited_user)) | (Q(Sender=visited_user) & Q(Receiver=visitor_user))
        )
    except Message_Request.DoesNotExist:
        msgrq = None

    return render(request, 'user_profile_advance.html', {'user': visited_user, 'request': msgrq})

    return render(request,'user_profile_advance.html',{'user':visited_user,'request':msgrq})
def visitor_profile(request):
    user = Usermember.objects.get(user=request.user)
    visitors = Visitor.objects.filter(Visited=user).order_by('-Time')
    print(visitors)
    
    return render(request,'visitor_profile.html',{'visitors':visitors})
    
   
def message_add(request,id):
    
    return render(request,'message.html',{'reciver_id':id})
def add_message(request,id):
    
    if request.method == 'POST':
            reciever = Usermember.objects.get(id=id)
            sender = Usermember.objects.get(user=request.user)
            message = request.POST['message']
            time = timezone.localtime(timezone.now())
            msg = Message(Sender=sender,Receiver=reciever,Content=message,time=time)
            msg.save()
            messages.success(request,'Message sent')
            return redirect('message_add',id=id)
        

def message_view(request):
    user = Usermember.objects.get(user=request.user)
    msgs = Message.objects.filter(Receiver=user).order_by('-time')
    for mg in msgs:
        mg.is_read=True
        mg.save()
    return render(request,'message_view.html',{'msg':msgs})
def message_delete(request,id):
    msg = Message.objects.get(id=id)
    msg.delete()
    return redirect('message_view')
def password(request):
    return render(request,'password.html')
def change_password(request):
    if request.method == 'POST':
        crpswd = request.POST['crpassword']
        pswd = request.POST['password']
        cpswd = request.POST['cpassword']

        if not request.user.check_password(crpswd):
            messages.error(request, 'Current password is incorrect.')
            return redirect('password')

        if len(pswd) < 6:
            messages.error(request, 'New password must be at least 6 characters long.')
            return redirect('password')

        if not any(char.isdigit() for char in pswd):
            messages.error(request, 'New password must contain at least one digit.')
            return redirect('password')

        if not any(char.isalpha() for char in pswd):
            messages.error(request, 'New password must contain at least one letter.')
            return redirect('password')

        if not any(char in string.punctuation for char in pswd):
            messages.error(request, 'New password must contain at least one special character.')
            return redirect('password')

        if pswd != cpswd:
            messages.error(request, 'New password and confirm new password do not match.')
            return redirect('password')

        request.user.set_password(pswd)
        request.user.save()

        messages.success(request, 'Password updated successfully.')
        return redirect('login_view')

    return render(request, 'password.html')
def message_request(request,id):
        reciever = Usermember.objects.get(id=id)
        sender = Usermember.objects.get(user=request.user)
       
        
        msg_request, created = Message_Request.objects.get_or_create(Sender=sender, Receiver=reciever, defaults={'is_request': True})
    
        if not created:
        
            msg_request.time = timezone.localtime(timezone.now())
            msg_request.is_request = True
            msg_request.save()

        
        return redirect('user_profile_advance',id=id)
def message_request_view(request):
    user = Usermember.objects.get(user=request.user)
    msgrq = Message_Request.objects.filter(Receiver=user,is_read=False).order_by('-time')

    
    return render(request, 'message_request_view.html', {'request': msgrq})
def message_accept(request,id):
    user = Usermember.objects.get(user=request.user)
    msgrq = get_object_or_404(Message_Request, Sender=id, Receiver=user)
    msgrq.is_accept = True
    msgrq.is_read = True

    msgrq.save()
    
    return redirect('message_request_view')
def notification(request):
    user = Usermember.objects.get(user=request.user)
    mq = Message_Request.objects.filter(Sender=user,is_accept=True,is_notify=False)
    for m in mq:
        m.is_notify = True
        m.save()
    
    
    return render(request,'msg_notification.html',{'request':mq})
def message_reject(request,id):
    user=Usermember.objects.get(user=request.user)
    mqr = Message_Request.objects.get(Sender=id,Receiver=user)
    mqr.delete()
    return redirect('message_request_view')
def image_edit(request):
    user= Usermember.objects.get(user=request.user)
    imgs = user.images.all()
    return render(request,'image_edit.html',{'img':imgs})
def delete_image(request,id):
    img = Image.objects.get(id=id)
    img.delete()
    return redirect('image_edit')
def image_add(request):
    if request.method == 'POST':
        images=request.FILES.getlist('image')
        um = Usermember.objects.get(user=request.user)
        for image in images:
            um.Image=image
        um.save()
        for image in images:
            image_instance = Image.objects.create(image=image)
            um.images.add(image_instance)
    return redirect('image_edit')




