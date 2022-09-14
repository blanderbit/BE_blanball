from project.constaints import *

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    '''user manager'''
    def create_admin(self,email:str,phone:str, password=None):
        ''' user admin manager'''
        if email is None:
            raise TypeError(NO_EMAIL_REGISTRATION_ERROR)
        adminUser = self.model(phone=phone,email=self.normalize_email(email))
        adminUser.is_verified = 1
        adminUser.set_password(password)
        adminUser.role = "Admin"
        adminUser.save()
        return adminUser

    def create_user(self, email:str,phone:str, password=None,*agrs,**kwargs):
        '''default user manager'''
        if email is None:
            raise TypeError(NO_EMAIL_REGISTRATION_ERROR)
        user = self.model(phone=phone,email=self.normalize_email(email),*agrs,**kwargs)
        user.set_password(password)
        user.role = "User"
        user.save()
        return user