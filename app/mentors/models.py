from django.contrib.auth.models import AbstractUser
from django.db import models
from Crypto.Cipher import AES
from django.conf import settings


class UserRoles(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    MENTOR = "MENTOR", "Mentor"


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=100, unique=True, blank=True, null=True)
    role = models.CharField(
        max_length=100, choices=UserRoles.choices, default=UserRoles.STUDENT
    )
    students = models.ManyToManyField(
        "self",
        related_name="mentors",
        symmetrical=False,
    )

    def add_student(self, user):
        if self.role == UserRoles.MENTOR:
            self.students.add(user)

    def add_mentor(self, user):
        if self.role == UserRoles.STUDENT:
            if not self.mentors.count():
                self.mentors.add(user)

    def get_decrypted_password(self):
        # use eval to convert bytes string representation to bytes, need think more
        # and change to something more secure
        _, nonce, hash = self.password.split("$", 2)
        cipher = AES.new(
            settings.PASSWORD_ENCRYPTION_KEY, AES.MODE_EAX, nonce=nonce.encode()
        )
        hash = eval(hash)
        decoded_password = cipher.decrypt(hash).decode()
        return decoded_password

    def __str__(self):
        return self.username
