from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, student_id, username, password, **kwargs):
        if not student_id or len(student_id) != 9 or not student_id.isdigit():
            raise ValueError('Users must have a 9-digit numeric student ID')
        
        user = self.model(
            student_id=student_id,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    student_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=100)
    password_check = models.CharField(max_length=100)  

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 student_id으로 설정 (student_id로 로그인)
    USERNAME_FIELD = 'student_id'