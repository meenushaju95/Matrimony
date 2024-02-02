from .import views
from django.urls import path

urlpatterns =[
              path('',views.home,name='home'),
              path('login_view',views.login_view,name='login_view'),
              path('signup',views.signup,name='signup'),
              path('adminhome',views.adminhome,name='adminhome'),
              path('logincheck',views.logincheck,name='logincheck'),
              path('addpackage',views.addpackage,name='addpackage'),
              path('packageadd',views.packageadd,name='packageadd'),
              path('package_dtails',views.package_details,name='package_details'),
              path('edit_package/<int:id>',views.edit_package,name='edit_package'),
              path('update_package/<int:id>',views.update_package,name='update_package'),
              path('delete_package/<int:id>',views.delete_package,name='delete_package'),
              path('package_view',views.package_view,name='package_view'),
              path('payment/<int:id>',views.payment,name='payment'),
              path('adduser',views.adduser,name='adduser'),
              path('payment_success/<int:id>',views.payment_success,name='payment_success'),
              path('approve',views.approve,name='approve'),
              path('approve_user/<int:id>',views.approve_user,name='approve_user'),
              path('disapprove_user/<int:id>',views.disapprove_user,name='disapprove_user'),
              path('user_record',views.user_record,name='user_record'),
              path('delete_user/<int:id>',views.delete_user,name='delete_user'),
              path('logout',views.logout,name='logout'),
              path('renew_success/<int:uid>/<int:pid>',views.renew_success,name='renew_success')
             
              
              
              
              ]