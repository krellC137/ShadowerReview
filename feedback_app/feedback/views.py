from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # For dynamic URL generation
from django.contrib.auth import logout  # To handle logout
from .models import Question, Response, Answer
from .forms import ResponseForm, QuestionForm
from qrcode import make  # To generate QR code
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa  # For PDF generation
import base64
from django.http import JsonResponse

@login_required
def dashboard(request):
    responses = Response.objects.all()
    return render(request, 'feedback/dashboard.html', {'responses': responses})

@login_required
def generate_qr_code(request):
    form_url = request.build_absolute_uri(reverse('submit_form'))
    
    # Generate the QR code
    qr = make(form_url)
    stream = BytesIO()
    qr.save(stream)
    qr_data = stream.getvalue()

    # Encode the QR code as base64 so it can be rendered in an img tag
    qr_base64 = base64.b64encode(qr_data).decode('utf-8')

    return JsonResponse({'qr_code': qr_base64})


# Remove @login_required to allow access without logging in
def submit_form(request):
    questions = Question.objects.all()
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save()
            for question in questions:
                answer_text = form.cleaned_data.get(f'question_{question.id}', '')
                Answer.objects.create(response=response, question=question, answer_text=answer_text)
            return redirect('thank_you')
    else:
        form = ResponseForm()

    return render(request, 'feedback/form.html', {'form': form, 'questions': questions})

@login_required
def update_questions(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'feedback/update_questions.html', {'form': form})

@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'feedback/question_list.html', {'questions': questions})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'feedback/edit_question.html', {'form': form})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('question_list')

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'feedback/add_question.html', {'form': form})


@login_required
def view_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    answers = Answer.objects.filter(response=response)
    return render(request, 'feedback/view_response.html', {'response': response, 'answers': answers})

@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.delete()
    return redirect('dashboard')  # Redirect to dashboard after deletion

# New thank_you view
def thank_you(request):
    return render(request, 'feedback/thank_you.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
#krell