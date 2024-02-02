from .import views
from django.urls import path

urlpatterns =[
             path('userhome',views.userhome,name='userhome'),
             path('logout',views.logout,name='logout'),
             path('showuser',views.showuser,name='showuser'),
             path('user_details/<int:id>',views.user_details,name='user_details'),
             path('edit_user/<int:id>',views.edit_user,name='edit_user'),
             path('update_user/<int:id>',views.update_user,name='update_user'),
            path('user_delete/<int:id>',views.user_delete,name='user_delete'),
            path('search_view',views.search_view,name='search_view'),
            path('search_profile',views.search_profile,name='search_profile'),
            path('user_search_details/<int:id>',views.user_search_details,name='user_search_details'),
            path('user_profile_advance/<int:id>',views.user_profile_advance,name='user_profile_advance'),
            path('visitor_profile',views.visitor_profile,name='visitor_profile'),
            path('message_add/<int:id>',views.message_add,name='message_add'),
            path('add_message/<int:id>',views.add_message,name='add_message'),
            path('message_view',views.message_view,name='message_view'),
            path('message_delete/<int:id>',views.message_delete,name='message_delete'),
            path('password',views.password,name='password'),
            path('change_password',views.change_password,name='change_password'),
            path('message_request/<int:id>',views.message_request,name='message_request'),
            path('message_request_view',views.message_request_view,name='message_request_view'),
            path('message_accept/<int:id>',views.message_accept,name='message_accept'),
            path('notification',views.notification,name='notification'),
            path('message_reject/<int:id>',views.message_reject,name='message_reject'),
            path('image_edit',views.image_edit,name='image_edit'),
            path('delete_image/<int:id>',views.delete_image,name='delete_image'),
            path('image_add',views.image_add,name='image_add')
           
            
             
              
              ]