from project.constaints import *
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    '''user manager'''
    def create_admin(self,email, password=None):
        ''' user admin manager'''
        if email is None:
            raise TypeError(NO_EMAIL_REGISTRATION_ERROR)
        adminUser = self.model(email=self.normalize_email(email))
        adminUser.role_id = 1
        adminUser.is_verified = 1
        adminUser.set_password(password)
        adminUser.save()
        return adminUser

    def create_user(self, email,phone, password=None,*agrs,**kwargs):
        '''default user manager'''
        if email is None:
            raise TypeError(NO_EMAIL_REGISTRATION_ERROR)
        user = self.model(phone=phone,email=self.normalize_email(email),*agrs,**kwargs)
        user.role_id = 2 #3
        user.set_password(password)
        user.save()
        return user