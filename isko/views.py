from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from django.contrib import messages
from .forms import ( 
    UserRegisterForm, UserLoginForm, SQLQueryForm, HonorsFormSet, SiblingsFormSet, ApplicantForm, SiblingsForm, HonorsForm, UserForm
    )
from django.utils import timezone
from .models import User, Applicant, Honors, Siblings

from django.db import connection

def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
         return render(request, 'home.html')

def applicant(request):
    if request.method == 'POST':
        applicant_form = ApplicantForm(request.POST, user_email=request.user.email)
        
        if applicant_form.is_valid():
            applicant = applicant_form.save(commit=False)
            applicant.user = request.user
            applicant.save()
            return redirect('honors')
        else:
            print("Applicant form errors:", applicant_form.errors)
    else:
        applicant_form = ApplicantForm(user_email=request.user.email)

    return render(request, 'applicant.html', {
        'applicant_form': applicant_form,
    })

def honors(request):
    if request.method == 'POST':
        honors_formset = HonorsFormSet(request.POST, queryset=Honors.objects.none())

        print(honors_formset.is_valid())
        
        if honors_formset.is_valid():
            for form in honors_formset:
                if form.cleaned_data: 
                    honors = form.save(commit=False)
                    honors.applicant = request.user.applicant
                    honors.save()
            return redirect('siblings')
        else:
            print("Honors formset errors:", honors_formset.errors)
    else:
        honors_formset = HonorsFormSet(queryset=Honors.objects.none())

    return render(request, 'honors.html', {
        'honors_formset': honors_formset,
    })

def siblings(request):
    if request.method == 'POST':
        siblings_formset = SiblingsFormSet(request.POST, queryset=Siblings.objects.none())
        
        if siblings_formset.is_valid():
            for form in siblings_formset:
                if form.cleaned_data: 
                    siblings = form.save(commit=False)
                    siblings.applicant = request.user.applicant
                    siblings.save()
            return redirect('user_dashboard')
        else:
            print("Siblings formset errors:", siblings_formset.errors)
    else:
        siblings_formset = SiblingsFormSet(queryset=Siblings.objects.none())

    return render(request, 'siblings.html', {
        'siblings_formset': siblings_formset,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Your account has been created! You are now logged in.')
                return redirect('applicant')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'home.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
labels = {
    'sibling_name': 'Sibling Name',
    'sibling_scholarship': 'Scholarship',
    'sibling_age': 'Age',
    'sibling_course_year': 'Course and Year'
}
@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        try:
            applicant_details = request.user.applicant
            return render(request, 'user_dashboard.html')
        except Applicant.DoesNotExist:
            return redirect('applicant')
        
@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def query(request):
    if request.method == 'POST':
        form = SQLQueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    column_names = [col[0] for col in cursor.description]
                    messages.success(request, 'Query executed successfully.')
                return render(request, 'query.html', {'form': form, 'result': result, 'columns': column_names})
            except Exception as e:
                messages.error(request, f'Error executing query: {e}')
    else:
        form = SQLQueryForm()
    return render(request, 'query.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

def applicant_list(request):
    applicant = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicant})

def applicant_detail(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    return render(request, 'applicant_detail.html', {'detail': applicant})

def applicant_update(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantForm(instance=applicant)
    return render(request, 'applicant_form.html', {'form': form})

def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        applicant.delete()
        return redirect('applicant_list')
    return render(request, 'applicant_confirm_delete.html', {'applicant': applicant})

def honors_list(request):
    honors = Honors.objects.all()
    return render(request, 'honors_list.html', {'honors': honors})

def honors_detail(request, pk):
    honor = get_object_or_404(Honors, pk=pk)
    return render(request, 'honors_detail.html', {'honor': honor})

def honors_create(request):
    if request.method == 'POST':
        form = HonorsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('honors_list')
    else:
        form = HonorsForm()
    return render(request, 'honors_form.html', {'form': form})

def honors_update(request, pk):
    honor = get_object_or_404(Honors, pk=pk)
    if request.method == 'POST':
        form = HonorsForm(request.POST, instance=honor)
        if form.is_valid():
            form.save()
            return redirect('honors_list')
    else:
        form = HonorsForm(instance=honor)
    return render(request, 'honors_form.html', {'form': form})

def honors_delete(request, pk):
    honor = get_object_or_404(Honors, pk=pk)
    if request.method == 'POST':
        honor.delete()
        return redirect('honors_list')
    return render(request, 'honors_confirm_delete.html', {'honor': honor})

def siblings_list(request):
    siblings = Siblings.objects.all()
    return render(request, 'siblings_list.html', {'siblings': siblings})

def siblings_create(request):
    if request.method == 'POST':
        form = SiblingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('siblings_list')
    else:
        form = SiblingsForm()
    return render(request, 'siblings_form.html', {'form': form})

def siblings_update(request, pk):
    sibling = get_object_or_404(Siblings, pk=pk)
    if request.method == 'POST':
        form = SiblingsForm(request.POST, instance=sibling)
        if form.is_valid():
            form.save()
            return redirect('siblings_list')
    else:
        form = SiblingsForm(instance=sibling)
    return render(request, 'siblings_form.html', {'form': form})

def siblings_delete(request, pk):
    sibling = get_object_or_404(Siblings, pk=pk)
    if request.method == 'POST':
        sibling.delete()
        return redirect('siblings_list')
    return render(request, 'siblings_confirm_delete.html', {'siblings': siblings})

def manage(request):
    return render(request, 'manage.html')

def programs(request):
    return render(request, 'programs.html')

def about(request):
    return render(request, 'about.html')