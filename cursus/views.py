from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Projet, Post, Program, Module, Lesson, Enrollment, Semester, Session
from utilisateur.models import Utilisateur
from .forms import ProgramForm, CourseForm, PostForm, StudentAddForm, LecturerAddForm

# --- CORE VIEWS ---

def home(request):
    items = Post.objects.all().order_by('-updated_date')
    return render(request, 'core/index.html', {'title': 'Accueil', 'items': items})

@login_required
def dashboard(request):
    context = {
        'title': 'Tableau de bord',
        'student_count': Utilisateur.objects.filter(type_utilisateur='ETU').count(),
        'lecturer_count': Utilisateur.objects.filter(type_utilisateur='INS').count(),
        'superuser_count': Utilisateur.objects.filter(is_superuser=True).count(),
        'course_count': Course.objects.count(),
        'males_count': Utilisateur.objects.filter(gender='M').count(), 
        'females_count': Utilisateur.objects.filter(gender='F').count(),
    }
    return render(request, 'core/dashboard.html', context)

# --- PROGRAM VIEWS ---

@login_required
def programs(request):
    all_programs = Program.objects.all()
    return render(request, 'course/program_list.html', {'filter': {'qs': all_programs}})

@login_required
def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    courses = Course.objects.filter(program=program)
    return render(request, 'course/program_single.html', {'program': program, 'courses': courses})

@login_required
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programme ajouté avec succès.')
            return redirect('programs')
    else:
        form = ProgramForm()
    return render(request, 'course/program_add.html', {'form': form})

@login_required
def edit_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programme modifié.')
            return redirect('programs')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'course/program_add.html', {'form': form})

@login_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    program.delete()
    messages.success(request, 'Programme supprimé.')
    return redirect('programs')

# --- COURSE VIEWS ---

@login_required
def user_course_list(request):
    courses = Course.objects.all()
    programs = Program.objects.all()
    context = {'courses': courses, 'programs': programs}
    if request.user.is_student:
        context['taken_courses'] = Enrollment.objects.filter(student=request.user)
        context['student'] = request.user
    return render(request, 'course/user_course_list.html', context)

@login_required
def course_single(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = Module.objects.filter(course=course)
    lecturers = [course.instructeur] 
    context = {
        'course': course,
        'modules': modules,
        'lecturers': lecturers,
        'title': course.titre,
    }
    return render(request, 'course/course_single.html', context)

@login_required
def course_add(request, slug):
    program = get_object_or_404(Program, pk=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.program = program
            course.save()
            messages.success(request, 'Cours ajouté avec succès.')
            return redirect('program_detail', pk=program.pk)
    else:
        form = CourseForm(initial={'program': program})
    return render(request, 'course/course_add.html', {'form': form, 'program': program})

@login_required
def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès.')
            return redirect('course_single', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/course_add.html', {'form': form, 'title': 'Modifier le cours'})

@login_required
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course.delete()
    messages.success(request, 'Cours supprimé.')
    return redirect('user_course_list')

# --- ACCOUNT VIEWS ---

@login_required
def lecturer_list(request):
    lecturers = Utilisateur.objects.filter(type_utilisateur='INS')
    return render(request, 'accounts/lecturer_list.html', {'filter': {'qs': lecturers}})

@login_required
def student_list(request):
    students = Utilisateur.objects.filter(type_utilisateur='ETU')
    return render(request, 'accounts/student_list.html', {'filter': {'qs': students}})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étudiant ajouté.')
            return redirect('student_list')
    else:
        form = StudentAddForm()
    return render(request, 'accounts/add_student.html', {'form': form})

@login_required
def add_lecturer(request):
    if request.method == 'POST':
        form = LecturerAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instructeur ajouté.')
            return redirect('lecturer_list')
    else:
        form = LecturerAddForm()
    return render(request, 'accounts/add_staff.html', {'form': form})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Utilisateur, pk=pk, type_utilisateur='ETU')
    if request.method == 'POST':
        form = StudentAddForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil étudiant mis à jour.')
            return redirect('student_list')
    else:
        form = StudentAddForm(instance=student)
    return render(request, 'accounts/edit_student.html', {'form': form})

@login_required
def staff_edit(request, pk):
    lecturer = get_object_or_404(Utilisateur, pk=pk, type_utilisateur='INS')
    if request.method == 'POST':
        form = LecturerAddForm(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil instructeur mis à jour.')
            return redirect('lecturer_list')
    else:
        form = LecturerAddForm(instance=lecturer)
    return render(request, 'accounts/edit_lecturer.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Utilisateur, pk=pk, type_utilisateur='ETU')
    student.delete()
    messages.success(request, 'Étudiant supprimé.')
    return redirect('student_list')

@login_required
def lecturer_delete(request, pk):
    lecturer = get_object_or_404(Utilisateur, pk=pk, type_utilisateur='INS')
    lecturer.delete()
    messages.success(request, 'Instructeur supprimé.')
    return redirect('lecturer_list')

@login_required
def profile_single(request, id):
    user = get_object_or_404(Utilisateur, id=id)
    return render(request, 'accounts/profile_single.html', {'user': user})

# --- POST VIEWS ---

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Annonce ajoutée avec succès.')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/post_add.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Annonce modifiée.')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_add.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Annonce supprimée.')
    return redirect('home')

# --- OTHER VIEWS ---

@login_required
def mes_projets(request):
    projets = Projet.objects.filter(utilisateur=request.user)
    return render(request, 'course/mes_projets.html', {'projets': projets})

@login_required
def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'core/session_list.html', {'sessions': sessions})

@login_required
def semester_list(request):
    semesters = Semester.objects.all()
    return render(request, 'core/semester_list.html', {'semesters': semesters})

@login_required
def add_session(request):
    if request.method == 'POST':
        # Logic to add session would go here
        messages.success(request, 'Session ajoutée (Simulation).')
        return redirect('session_list')
    return render(request, 'core/session_add.html', {'title': 'Ajouter une session'})

@login_required
def edit_session(request, pk):
    # Logic to edit session
    messages.success(request, 'Session modifiée (Simulation).')
    return redirect('session_list')

@login_required
def delete_session(request, pk):
    # Logic to delete session
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    messages.success(request, 'Session supprimée.')
    return redirect('session_list')

@login_required
def student_program_edit(request, id):
    # Logic to edit student program
    messages.info(request, 'Fonctionnalité en cours de développement.')
    return redirect('profile_single', id=id)

# --- PLACEHOLDERS ---

def student_list_pdf(request):
    return redirect('student_list')

def lecturer_list_pdf(request):
    return redirect('lecturer_list')

def upload_file_view(request, slug):
    return render(request, 'course/course_single.html')

def upload_video(request, slug):
    return render(request, 'course/course_single.html')

def upload_file_edit(request, slug, file_id):
    return render(request, 'course/course_single.html')

def upload_file_delete(request, slug, file_id):
    return render(request, 'course/course_single.html')

def upload_video_edit(request, slug, video_slug):
    return render(request, 'course/course_single.html')

def upload_video_delete(request, slug, video_slug):
    return render(request, 'course/course_single.html')

def course_allocation_view(request):
    return render(request, 'course/course_allocation_view.html')

def add_score(request):
    return render(request, 'result/add_score.html')

def grade_results(request):
    return render(request, 'result/grade_results.html')

def ass_results(request):
    return render(request, 'result/assessment_results.html')

def course_registration(request):
    return render(request, 'course/course_registration.html')

def quiz_progress(request):
    return render(request, 'quiz/quiz_progress.html')

def quiz_marking(request):
    return render(request, 'quiz/quiz_marking.html')

def quiz_index(request, slug):
    return render(request, 'quiz/quiz_index.html')
