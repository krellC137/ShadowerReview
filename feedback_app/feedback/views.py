from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # For dynamic URL generation
from .models import Question, Response, Answer
from .forms import ResponseForm, QuestionForm
from qrcode import make  # To generate QR code
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa  # For PDF generation

@login_required
def dashboard(request):
    responses = Response.objects.all()
    return render(request, 'feedback/dashboard.html', {'responses': responses})

@login_required
def generate_qr_code(request):
    form_url = request.build_absolute_uri(reverse('submit_form'))
    
    qr = make(form_url)
    stream = BytesIO()
    qr.save(stream)
    return HttpResponse(stream.getvalue(), content_type="image/png")

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
def download_pdf(request, response_id):
    response = Response.objects.get(id=response_id)
    answers = Answer.objects.filter(response=response)
    
    # Render template to HTML string
    html_string = render_to_string('feedback/pdf_template.html', {'response': response, 'answers': answers})

    # Generate PDF using xhtml2pdf
    response_pdf = HttpResponse(content_type='application/pdf')
    response_pdf['Content-Disposition'] = f'attachment; filename="{response.name}_{response.surname}_response.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response_pdf)

    # If error, show an error message
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response_pdf

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
#krell