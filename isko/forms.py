from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Applicant, Honors, Siblings
from datetime import date
from crispy_forms.helper import FormHelper

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class SQLQueryForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea)

class SQLForm(forms.Form):
    sql_code = forms.CharField(widget=forms.HiddenInput())

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_superuser']

class UserAdminForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'is_staff', 'is_superuser']

class ApplicantForm(forms.ModelForm):
    SEX_CHOICES = [
        ('', 'Please select'),
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    STATUS_CHOICES = [
        ('', 'Please select'),
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('Se', 'Separated')
    ]
    
    HIGHEST_YEAR_CHOICES = [
        ('', 'Please select'),
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'),
        ('Grade 11', 'Grade 11'),
        ('Grade 12', 'Grade 12')
    ]

    PARENT_STATUS = [
        ('', 'Please select'),
        ('L', 'Living'),
        ('D', 'Dead')
    ]
    
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    highest_year = forms.ChoiceField(choices=HIGHEST_YEAR_CHOICES)
    mother_status = forms.ChoiceField(choices=PARENT_STATUS)
    father_status = forms.ChoiceField(choices=PARENT_STATUS)

    class Meta:
        model = Applicant
        fields = [
            'applicant_name', 'age', 'sex', 'status', 'religion', 'citizenship', 'birthday', 
            'birthplace', 'telephone_number', 'mobile_number', 'email_address', 'home_address', 
            'highschool_name', 'highschool_address', 'highest_year', 'graduation_date', 'gwa',
            'father_status', 'father_name', 'father_address', 'father_occupation', 'father_education',
            'mother_status', 'mother_name', 'mother_address', 'mother_occupation', 'mother_education',
            'gross_income', 'no_of_children', 'school_enroll', 'first_choice', 'second_choice', 'third_choice'
        ]
        labels = {
        'applicant_name': 'Applicant Name',
        'age': 'Age',
        'sex': 'Sex',
        'status': 'Status',
        'religion': 'Religion',
        'citizenship': 'Citizenship',
        'birthday': 'Birthday',
        'birthplace': 'Birthplace',
        'telephone_number': 'Telephone Number',
        'mobile_number': 'Mobile Number',
        'email_address': 'Email Address',
        'home_address': 'Home Address',
        'highschool_name': 'High School Name',
        'highschool_address': 'High School Address',
        'highest_year': 'Highest Year',
        'graduation_date': 'Graduation Date',
        'gwa': 'GWA',
        'father_status': 'Father Status',
        'father_name': 'Father Name',
        'father_address': 'Father Address',
        'father_occupation': 'Father Occupation',
        'father_education': 'Father Education',
        'mother_status': 'Mother Status',
        'mother_name': 'Mother Name',
        'mother_address': 'Mother Address',
        'mother_occupation': 'Mother Occupation',
        'mother_education': 'Mother Education',
        'gross_income': 'Gross Income',
        'no_of_children': 'Number of Children in the Family',
        'school_enroll': 'School Enrolled',
        'first_choice': 'First Choice',
        'second_choice': 'Second Choice',
        'third_choice': 'Third Choice',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)
        super().__init__(*args, **kwargs)
        if user_email:
            self.fields['email_address'].initial = user_email
            self.fields['email_address'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label})

class ApplicantAdminForm(forms.ModelForm):
    SEX_CHOICES = [
        ('', 'Please select'),
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    STATUS_CHOICES = [
        ('', 'Please select'),
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('Se', 'Separated')
    ]
    
    HIGHEST_YEAR_CHOICES = [
        ('', 'Please select'),
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
        ('Grade 10', 'Grade 10'),
        ('Grade 11', 'Grade 11'),
        ('Grade 12', 'Grade 12')
    ]

    PARENT_STATUS = [
        ('', 'Please select'),
        ('L', 'Living'),
        ('D', 'Dead')
    ]
    
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    highest_year = forms.ChoiceField(choices=HIGHEST_YEAR_CHOICES)
    mother_status = forms.ChoiceField(choices=PARENT_STATUS)
    father_status = forms.ChoiceField(choices=PARENT_STATUS)

    class Meta:
        model = Applicant
        fields = [
            'user', 'applicant_name', 'age', 'sex', 'status', 'religion', 'citizenship', 'birthday', 
            'birthplace', 'telephone_number', 'mobile_number', 'email_address', 'home_address', 
            'highschool_name', 'highschool_address', 'highest_year', 'graduation_date', 'gwa',
            'father_status', 'father_name', 'father_address', 'father_occupation', 'father_education',
            'mother_status', 'mother_name', 'mother_address', 'mother_occupation', 'mother_education',
            'gross_income', 'no_of_children', 'school_enroll', 'first_choice', 'second_choice', 'third_choice'
        ]
        labels = {
        'user': 'User',
        'applicant_name': 'Applicant Name',
        'age': 'Age',
        'sex': 'Sex',
        'status': 'Status',
        'religion': 'Religion',
        'citizenship': 'Citizenship',
        'birthday': 'Birthday',
        'birthplace': 'Birthplace',
        'telephone_number': 'Telephone Number',
        'mobile_number': 'Mobile Number',
        'email_address': 'Email Address',
        'home_address': 'Home Address',
        'highschool_name': 'High School Name',
        'highschool_address': 'High School Address',
        'highest_year': 'Highest Year',
        'graduation_date': 'Graduation Date',
        'gwa': 'GWA',
        'father_status': 'Father Status',
        'father_name': 'Father Name',
        'father_address': 'Father Address',
        'father_occupation': 'Father Occupation',
        'father_education': 'Father Education',
        'mother_status': 'Mother Status',
        'mother_name': 'Mother Name',
        'mother_address': 'Mother Address',
        'mother_occupation': 'Mother Occupation',
        'mother_education': 'Mother Education',
        'gross_income': 'Gross Income',
        'no_of_children': 'Number of Children in the Family',
        'school_enroll': 'School Enrolled',
        'first_choice': 'First Choice',
        'second_choice': 'Second Choice',
        'third_choice': 'Third Choice',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label}) 

class HonorsForm(forms.ModelForm):
    class Meta:
        model = Honors
        fields = ['honors_received', 'honors_school', 'honors_date']
        labels = {
        'honors_received': 'Honors Received',
        'honors_school': 'School Name',
        'honors_date': 'Date Received'
            }
        widgets = {
            'honors_date': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.empty_permitted = False
            field.widget.attrs.update({
                'placeholder': field.label,
            })

class RequiredFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

class HonorsAdminForm(forms.ModelForm):
    class Meta:
        model = Honors
        fields = ['applicant', 'honors_received', 'honors_school', 'honors_date']
        labels = {
            'applicant': 'Applicant',
            'honors_received': 'Honors Received',
            'honors_school': 'School Name',
            'honors_date': 'Date Received'
        }
        widgets = {
            'honors_date': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': field.label,
            })
            


class SiblingsForm(forms.ModelForm):
    class Meta:
        model = Siblings
        fields = ['sibling_name', 'sibling_scholarship', 'sibling_age', 'sibling_course_year']
        labels = {
            'sibling_name': 'Siblings Name',
            'sibling_scholarship': 'Scholarship',
            'sibling_age': 'Age',
            'sibling_course_year': 'Course and Year'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': field.label,
            })

class SiblingsAdminForm(forms.ModelForm):
    class Meta:
        model = Siblings
        fields = ['applicant', 'sibling_name', 'sibling_scholarship', 'sibling_age', 'sibling_course_year']
        labels = {
            'applicant': 'Applicant',
            'sibling_name': 'Siblings Name',
            'sibling_scholarship': 'Scholarship',
            'sibling_age': 'Age',
            'sibling_course_year': 'Course and Year'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs.update({
                    'placeholder': field.label,
                })


HonorsFormSet = modelformset_factory(Honors, form=HonorsForm, formset=RequiredFormSet, extra=1)
SiblingsFormSet = modelformset_factory(Siblings, form=SiblingsForm, extra=1)