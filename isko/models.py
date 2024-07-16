from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

def validate_sex(value):
    if value not in ['M', 'F']:
        raise ValidationError(f'{value} is not a valid choice. Valid choices are: M, F')

def validate_status(value):
    if value not in ['S', 'M', 'W', 'Se']:
        raise ValidationError(f'{value} is not a valid choice. Valid choices are: S, M, W, Se')

def validate_highest_year(value):
    if value not in ['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']:
        raise ValidationError(f'{value} is not a valid choice. Valid choices are: Grade 7, Grade 8, Grade 9, Grade 10, Grade 11, Grade 12')

def validate_parent_status(value):
    if value not in ['L', 'D']:
        raise ValidationError(f'{value} is not a valid choice. Valid choices are: L, D')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    applicant_id = models.AutoField(primary_key=True)
    applicant_name = models.CharField(max_length=80)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(99), MinValueValidator(1)])
    sex = models.CharField(max_length=1, validators=[validate_sex])
    status = models.CharField(max_length=2, validators=[validate_status])
    religion = models.CharField(max_length=45)
    citizenship = models.CharField(max_length=45)
    birthday = models.DateField()
    birthplace = models.CharField(max_length=45)
    telephone_number = models.CharField(max_length=15, null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=45)
    home_address = models.CharField(max_length=100)
    highschool_name = models.CharField(max_length=45)
    highschool_address = models.CharField(max_length=100)
    highest_year = models.CharField(max_length=10, validators=[validate_highest_year])
    gwa = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(99.99), MinValueValidator(90.00)])
    graduation_date = models.DateField()
    father_status = models.CharField(max_length=1, validators=[validate_parent_status])
    father_name = models.CharField(max_length=80)
    father_address = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=30)
    father_education = models.CharField(max_length=25)
    mother_status = models.CharField(max_length=1, validators=[validate_parent_status])
    mother_name = models.CharField(max_length=80)
    mother_address = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=30)
    mother_education = models.CharField(max_length=25)
    gross_income = models.DecimalField(max_digits=9, decimal_places=2)
    no_of_children = models.PositiveIntegerField(validators=[MaxValueValidator(99), MinValueValidator(0)])
    school_enroll = models.CharField(max_length=50)
    first_choice = models.CharField(max_length=50)
    second_choice = models.CharField(max_length=50)
    third_choice = models.CharField(max_length=50)

class Honors(models.Model):
    honors_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    honors_received = models.CharField(max_length=45)
    honors_school = models.CharField(max_length=70)
    honors_date = models.DateField()

class Siblings(models.Model):
    sibling_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    sibling_name = models.CharField(max_length=50, null=True, blank=True)
    sibling_scholarship = models.CharField(max_length=45, null=True, blank=True) 
    sibling_age = models.PositiveIntegerField(validators=[MaxValueValidator(999), MinValueValidator(1)], null=True, blank=True)
    sibling_course_year = models.CharField(max_length=45, null=True, blank=True) 
    
def validate_choice(value, valid_choices):
    if value not in valid_choices:
        raise ValidationError(f'Invalid value: {value}. Valid choices are: {", ".join(valid_choices)}.')
