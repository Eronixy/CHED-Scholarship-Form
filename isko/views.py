from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ( 
    UserRegisterForm, UserLoginForm, SQLQueryForm, HonorsFormSet, SiblingsFormSet, ApplicantForm, SiblingsForm, HonorsForm, UserForm, ApplicantAdminForm, HonorsAdminForm, SiblingsAdminForm, UserAdminForm
    )
from .models import User, Applicant, Honors, Siblings
from django.db import connection
from django.apps import apps

def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    return rows, columns

def problem1(request):
    results, columns = run_query("SELECT applicant_name, school_enroll, first_choice, gwa FROM ched.isko_applicant WHERE gwa >= 90 AND first_choice IN ('BS in Computer Science', 'BS in Information Technology') AND school_enroll = 'Polytechnic University of the Philippines' ORDER BY gwa DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem2(request):
    results, columns = run_query("SELECT applicant_name, mother_name, mother_status, father_name, father_status, no_of_children, gross_income FROM ched.isko_applicant WHERE (mother_status = 'L' OR father_status = 'L') AND no_of_children > 2 ORDER BY gross_income DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem3(request):
    results, columns = run_query("SELECT applicant_name, home_address, school_enroll, first_choice, gwa FROM ched.isko_applicant WHERE gwa >= 90 AND first_choice NOT IN ('BS in Computer Science', 'BS in Information Technology') AND school_enroll = 'Polytechnic University of the Philippines' AND home_address NOT LIKE '%manila%' ORDER BY gwa DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem4(request):
    results, columns = run_query("SELECT citizenship, COUNT(applicant_id) AS ApplicantCount, AVG(gwa) AS AverageGrade FROM ched.isko_applicant WHERE ((citizenship = 'Filipino' AND home_address LIKE '%Manila%') OR (citizenship NOT LIKE 'Filipino' AND home_address NOT LIKE '%Manila%')) AND gwa > 90 GROUP BY citizenship HAVING AVG(gwa) > 92 ORDER BY AVG(gwa) DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem5(request):
    results, columns = run_query("SELECT sex, COUNT(applicant_id) AS applicant_count, AVG(gross_income) AS avg_gross_income, AVG(gwa) AS avg_gwa FROM ched.isko_applicant WHERE age BETWEEN 18 AND 25 AND school_enroll = 'Polytechnic University of the Philippines' GROUP BY sex ORDER BY avg_gross_income DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem6(request):
    results, columns = run_query("SELECT applicant_id, GROUP_CONCAT(honors_received ORDER BY honors_date SEPARATOR ', ') AS honors_received, COUNT(honors_id) AS total_honors FROM ched.isko_honors WHERE honors_date BETWEEN '2024-04-01' AND '2024-06-30' GROUP BY applicant_id HAVING COUNT(honors_id) > 1 ORDER BY total_honors DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem7(request):
    results, columns = run_query("SELECT school_enroll, AVG(gwa) AS Average_Grade, COUNT(*) AS Applicant_Count FROM ched.isko_applicant WHERE gwa > (SELECT AVG(gwa) FROM ched.isko_applicant) AND (citizenship = 'Filipino' OR gross_income > 500000) GROUP BY school_enroll HAVING AVG(gwa) > 95 ORDER BY AVG(gwa) DESC, school_enroll ASC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem8(request):
    results, columns = run_query("SELECT A.applicant_id, A.applicant_name, A.citizenship, A.highschool_name, A.gwa, A.school_enroll, COUNT(H.honors_id) AS Total_honors, S.sibling_name AS Sibling_with_DOST_scholarship FROM ched.isko_applicant AS A, ched.isko_honors AS H, ched.isko_siblings AS S WHERE A.applicant_id = H.applicant_id AND A.applicant_id = S.applicant_id AND S.sibling_scholarship = 'DOST Scholarship' GROUP BY A.applicant_id, A.applicant_name, A.citizenship, A.highschool_name, A.gwa, A.school_enroll, S.sibling_name HAVING COUNT(H.honors_id) > 1 ORDER BY Total_honors DESC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem9(request):
    results, columns = run_query("SELECT a.applicant_id, a.applicant_name, COUNT(h.honors_received)AS no_of_honors_received, s.sibling_name, s.sibling_scholarship FROM ched.isko_applicant AS a, ched.isko_honors AS h, ched.isko_siblings AS s WHERE (a.applicant_id = h.applicant_id AND a.applicant_id = s.applicant_id) AND a.citizenship = 'Filipino' AND a.gwa >= 91 AND s.sibling_scholarship NOT LIKE '%DOST%' GROUP BY a.applicant_id, a.applicant_name, s.sibling_name, s.sibling_scholarship HAVING COUNT(h.honors_id) > 1 ORDER BY a.applicant_id ASC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def problem10(request):
    results, columns = run_query("SELECT a.applicant_id, a.applicant_name, COUNT(DISTINCT s.sibling_id) AS total_siblings, COUNT(DISTINCT h.honors_id) AS total_honors, MAX(s.sibling_age) AS oldest_sibling_age, MIN(s.sibling_age) AS youngest_sibling_age FROM ched.isko_applicant AS a, ched.isko_honors AS h, ched.isko_siblings AS s WHERE a.applicant_id = h.applicant_id AND a.applicant_id = s.applicant_id AND s.sibling_course_year LIKE '%BS%' AND a.citizenship = 'Filipino' AND YEAR(a.graduation_date) = 2024 GROUP BY a.applicant_id HAVING total_honors > 1 ORDER BY a.applicant_id ASC;")
    return render(request, 'result.html', {'results': results, 'columns': columns})

def result(request):
    return render(request, 'result.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    else:
         return render(request, 'home.html')

@login_required
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

@login_required
def honors(request):
    if request.method == 'POST':
        honors_formset = HonorsFormSet(request.POST, queryset=Honors.objects.none())
        
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

@login_required
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
                for message in messages.get_messages(request):
                    print(f'Message: {message}')
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
            honors_details = Honors.objects.filter(applicant=applicant_details)
            if honors_details.exists():
                return render(request, 'user_dashboard.html', {'honors_details': honors_details})
            else:
                return redirect('honors') 
        except Applicant.DoesNotExist:
            return redirect('applicant')
        
@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
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


@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def user_create(request):
    if request.method == 'POST':
        form = UserAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserAdminForm()
    return render(request, 'user_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
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

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def applicant_list(request):
    applicant = Applicant.objects.all()
    return render(request, 'applicant_list.html', {'applicants': applicant})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def applicant_create(request):
    if request.method == 'POST':
        form = ApplicantAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('applicant_list')
    else:
        form = ApplicantAdminForm()
    return render(request, 'applicant_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
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

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        applicant.delete()
        return redirect('applicant_list')
    return render(request, 'applicant_confirm_delete.html', {'applicant': applicant})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def honors_list(request):
    honors = Honors.objects.all()
    return render(request, 'honors_list.html', {'honors': honors})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def honors_detail(request, pk):
    honor = get_object_or_404(Honors, pk=pk)
    return render(request, 'honors_detail.html', {'honor': honor})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def honors_create(request):
    if request.method == 'POST':
        form = HonorsAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('honors_list')
    else:
        form = HonorsAdminForm()
    return render(request, 'honors_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
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

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def honors_delete(request, pk):
    honor = get_object_or_404(Honors, pk=pk)
    if request.method == 'POST':
        honor.delete()
        return redirect('honors_list')
    return render(request, 'honors_confirm_delete.html', {'honor': honor})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def siblings_list(request):
    siblings = Siblings.objects.all()
    return render(request, 'siblings_list.html', {'siblings': siblings})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def siblings_create(request):
    if request.method == 'POST':
        form = SiblingsAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('siblings_list')
    else:
        form = SiblingsAdminForm()
    return render(request, 'siblings_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
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

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def siblings_delete(request, pk):
    sibling = get_object_or_404(Siblings, pk=pk)
    if request.method == 'POST':
        sibling.delete()
        return redirect('siblings_list')
    return render(request, 'siblings_confirm_delete.html', {'siblings': sibling})

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def manage(request):
    return render(request, 'manage.html')

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def admin_about(request):
    return render(request, 'admin_about.html')

@login_required
@user_passes_test(lambda u: u.is_superuser == 1)
def admin_programs(request):
    return render(request, 'admin_programs.html')

def programs(request):
    if request.user.is_superuser:
        return redirect('admin_programs')
    else:
        return render(request, 'programs.html')

def about(request):
    if request.user.is_superuser:
        return redirect('admin_about')
    else:
        return render(request, 'about.html')