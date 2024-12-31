import random

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from costumadmin.models import WritingTask1, Book, Unit, Vocab, CambridgeTest
from user.models import Part1Question, PartTopic, Part2Question, Part3Question


class RegistrationView(View):
    def get(self, request):
        step = request.GET.get('step', '1')  # Default to step 1
        if step == '2' and 'registration_email' not in request.session:
            messages.error(request, "Sessiya muddati tugagan. Iltimos, qayta ro‘yxatdan o‘ting.")
            return redirect(f'{request.path}?step=1')
        return render(request, 'sign-up.html', {'step': step})

    def post(self, request):
        step = request.GET.get('step', '1')

        if step == '1':
            email = request.POST.get('email')
            if not email:
                messages.error(request, "Emailni kiritish shart.")
                return render(request, 'sign-up.html', {"step": "1"})

            try:
                code = random.randint(100000, 999999)

                # Debugging
                print(f"Generated code for {email}: {code}")

                # Send email directly
                send_mail(
                    'Verification Code',
                    f'Your verification code is {code}',
                    'your-email@example.com',  # Replace with your sender email
                    [email],
                    fail_silently=False,
                )

                # Save code in session
                request.session['verification_code'] = str(code)
                request.session['registration_email'] = email

                return redirect(f'{request.path}?step=2')
            except Exception as e:
                print("Email sending failed:", e)
                messages.error(request, "Emailni jo'natishda xatolik yuz berdi.")
                return render(request, 'sign-up.html', {"step": "1"})

        elif step == '2':  # Verification code
            code = request.POST.get('code')
            email = request.session.get('registration_email')
            stored_code = request.session.get('verification_code')

            print(f"Entered code: {code}, Stored code: {stored_code}, Email: {email}")

            if not email:
                messages.error(request, "Sessiya muddati tugagan. Iltimos, qayta ro‘yxatdan o‘ting.")
                return redirect(f'{request.path}?step=1')

            if stored_code and stored_code == code:
                print("Verification successful!")
                return redirect(f'{request.path}?step=3')

            messages.error(request, 'Tasdiqlash kodi noto‘g‘ri. Yangi kod yuborildi.')
            new_code = random.randint(100000, 999999)
            send_mail(
                'New Verification Code',
                f'Your new verification code is {new_code}',
                'your-email@example.com',
                [email],
                fail_silently=False,
            )
            request.session['verification_code'] = str(new_code)
            return render(request, 'sign-up.html', {"step": "2"})
        elif step == '3':  # Password setup
            password = request.POST.get('password')
            email = request.session.get('registration_email')
            user = User.objects.create_user(
                username=f"user{random.randint(100000, 999999)}",
                email=email,
                password=password
            )
            user.save()
            del request.session['verification_code']
            del request.session['registration_email']
            messages.success(request, 'Ro‘yxatdan muvaffaqiyatli o‘tdingiz!')
            return redirect('login')
        return render(request, 'sign-up.html', {"step": step})


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import login


class LoginFormView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Foydalanuvchini topish uchun filter ishlatamiz
            user = User.objects.filter(email=email).first()
            if not user:
                raise User.DoesNotExist
            print(user)
        except User.DoesNotExist:
            messages.error(request, "Email yoki parol noto'g'ri!")
            return render(request, self.template_name)

        if user.check_password(password):
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('homee')
        else:
            messages.error(request, "Email yoki parol noto'g'ri!")
            return render(request, self.template_name)


def home_main(request):
    return render(request, 'user/index.html')


def WritingView(request):
    return render(request, 'user/writing_user.html')

def writing_task_view(request, task_type):
    tasks = WritingTask1.objects.filter(type1=task_type)
    task = random.choice(tasks) if tasks.exists() else None

    # task_type ga qarab vaqt va matn o'zgarishi
    if task_type == 1:
        task_type_label = "Task 1"
        time_limit = 20  # 20 minutes
        word_limit = "Write at least 150 words."
    elif task_type == 2:
        task_type_label = "Task 2"
        time_limit = 40  # 40 minutes
        word_limit = "Write at least 250 words."
    else:
        task_type_label = "Full Test"
        time_limit = 20  # 20 minutes
        word_limit = "Write at least 150 words."

    return render(
        request,
        'user/writing_user.html',
        {
            'task': task,
            'task_type_label': task_type_label,
            'time_limit': time_limit,
            'word_limit': word_limit,
            'task_type': task_type,
        }
    )


@require_POST
@csrf_exempt
def submit_response(request):
    task_id = request.POST.get('task_id')
    response = request.POST.get('response')

    try:
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user",
                 "content": f"Review this IELTS response and find mistakes and give an IELTS-like answer: {response}"}
            ]
        )
        evaluation = chat_response.choices[0].message['content']
        return JsonResponse({
            'status': 'success',
            'message': 'Response saved and evaluated successfully',
            'task_id': task_id,
            'response': response,
            'evaluation': evaluation
        })

    except Exception as e:
        print(str(e))
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to evaluate response'
        }, status=500)


def SpeakingView(request):
    return render(request, 'user/speaking.html')


def ieltsView(request):
    return render(request, 'user/ielts.html')


def take_test(request, topic_id):
    questions = Part1Question.objects.filter(part_topic_id=topic_id).order_by('id')
    return render(request, 'user/taketestprt1.html', {'questions': questions})

def take_test2(request, topic_id):
    questions = Part2Question.objects.filter(part_topic_id=topic_id).order_by('id')
    return render(request, 'user/taketestprt1.html', {'questions': questions})

def take_test3(request, topic_id):
    questions = Part3Question.objects.filter(part_topic_id=topic_id).order_by('id')
    return render(request, 'user/taketestprt1.html', {'questions': questions})


import os
import uuid
import json
import openai

from django.conf import settings
from django.http import JsonResponse
from pydub import AudioSegment
from django.views.decorators.csrf import csrf_exempt

openai.api_key = settings.OPENAI_API_KEY  # Ensure this is set in settings.py


def grammar_check(text):
    """
    Sends the transcribed text to ChatGPT to:
      - Find grammar/usage mistakes
      - Provide improvement advice
      - NOT provide a corrected version of the text.
    We assume the text is in English.
    Returns a dict with 'mistakes' and 'improvement_advice'.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. "
                        "The user is speaking in English. "
                        "You MUST respond in valid JSON format ONLY. "
                        "Do NOT include backticks, code blocks, or disclaimers. "
                        "Only respond with keys 'mistakes' and 'improvement_advice'. "
                        "If you cannot comply, return an empty JSON object."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Here is the text (in English):\n\n"
                        f"{text}\n\n"
                        "Identify grammar/usage mistakes, list them in 'mistakes' (array). "
                        "Then provide advice on how to improve in 'improvement_advice' (string). "
                        "Do NOT provide a corrected version of the text."
                    )
                }
            ],
            temperature=0.0,  # more deterministic
        )
        assistant_reply = response["choices"][0]["message"]["content"].strip()

        print("Assistant reply:", assistant_reply)  # Debug

        data = json.loads(assistant_reply)  # Attempt to parse JSON
        return {
            "mistakes": data.get("mistakes", []),
            "improvement_advice": data.get("improvement_advice", "")
        }

    except json.JSONDecodeError:
        print("ChatGPT did not return valid JSON.")
        return {
            "mistakes": [],
            "improvement_advice": "No structured advice provided; invalid JSON returned by ChatGPT."
        }
    except Exception as e:
        print("Error calling ChatGPT:", e)
        return {
            "mistakes": [],
            "improvement_advice": f"Error calling ChatGPT: {str(e)}"
        }


@csrf_exempt
def upload_audio(request):
    """
    1. Uploads an audio file (via 'POST' request).
    2. Converts the uploaded file to MP3 using pydub.
    3. Transcribes the MP3 file using OpenAI Whisper.
    4. Sends the transcription to ChatGPT for mistake detection and improvement advice.
    5. Returns a JSON response with the original transcription and the mistakes/advice.
    """
    if request.method == 'POST' and 'audio' in request.FILES:
        try:
            # 1. Get the audio file
            audio_file = request.FILES['audio']

            # 2. Extract base name and extension
            base_name, ext = os.path.splitext(audio_file.name)

            # 3. Generate unique filename
            unique_id = uuid.uuid4().hex
            new_filename = f"{base_name}_{unique_id}{ext}"

            # 4. Create path and save file
            wav_path = os.path.join(settings.MEDIA_ROOT, 'audio', new_filename)
            os.makedirs(os.path.dirname(wav_path), exist_ok=True)
            with open(wav_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # 5. Convert to MP3 using pydub
            sound = AudioSegment.from_file(wav_path)
            mp3_path = os.path.splitext(wav_path)[0] + '.mp3'
            sound.export(mp3_path, format='mp3')
            os.remove(wav_path)  # remove original file

            # 6. Transcribe with OpenAI Whisper
            with open(mp3_path, 'rb') as f:
                transcription_response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=f,
                    # language="en" or your chosen language
                )
            transcript_text = transcription_response["text"]

            # 7. Analyze mistakes and get advice (NO correction)
            analysis_data = grammar_check(transcript_text)

            # 8. Return JSON response
            return JsonResponse({
                'message': 'Audio converted, saved, and transcribed successfully!',
                'mp3_file': os.path.basename(mp3_path),
                'transcription': transcript_text,
                'analysis': {
                    'mistakes': analysis_data.get('mistakes', []),
                    'improvement_advice': analysis_data.get('improvement_advice', '')
                }
            }, status=200)

        except Exception as e:
            print(f"Error during upload_audio: {e}")
            return JsonResponse(
                {'message': 'Internal server error', 'error': str(e)},
                status=500
            )

    # If it's not POST or no file
    return JsonResponse({'message': 'Invalid request!'}, status=400)


def part1View(request):
    topics = PartTopic.objects.filter(part_type='part1')
    print("Filtered Topics Count:", topics.count())
    selected_topic = request.GET.get('topic')
    print(selected_topic)
    if selected_topic:
        try:
            selected_topic = int(selected_topic)  # Convert to integer
            questions = Part1Question.objects.filter(part_topic_id=selected_topic)
            if not questions.exists():
                print(f"No questions found for topic id: {selected_topic}")
        except ValueError:
            questions = Part1Question.objects.none()
            selected_topic = None
            print(f"Invalid topic ID: {selected_topic}")
    else:
        questions = Part1Question.objects.none()
        print("No topic selected, returning no questions.")
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/part1.html', {
        'topics': topics,
        'questions': page_obj,
        'selected_topic': selected_topic,
    })


def part2View(request):
    topics = PartTopic.objects.filter(part_type='part2')
    print("Filtered Topics Count:", topics.count())
    selected_topic = request.GET.get('topic')
    if selected_topic:
        try:
            selected_topic = int(selected_topic)  # Convert to integer
            questions = Part2Question.objects.filter(part_topic_id=selected_topic)
            if not questions.exists():
                print(f"No questions found for topic id: {selected_topic}")
        except ValueError:
            questions = Part2Question.objects.none()
            selected_topic = None
            print(f"Invalid topic ID: {selected_topic}")
    else:
        questions = Part2Question.objects.none()
        print("No topic selected, returning no questions.")
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/part2.html', {
        'topics': topics,
        'questions': page_obj,
        'selected_topic': selected_topic,
    })


def part3View(request):
    topics = PartTopic.objects.filter(part_type='part3')
    print("Filtered Topics Count:", topics.count())
    selected_topic = request.GET.get('topic')
    if selected_topic:
        try:
            selected_topic = int(selected_topic)  # Convert to integer
            questions = Part3Question.objects.filter(part_topic_id=selected_topic)
            if not questions.exists():
                print(f"No questions found for topic id: {selected_topic}")
        except ValueError:
            questions = Part3Question.objects.none()
            selected_topic = None
            print(f"Invalid topic ID: {selected_topic}")
    else:
        questions = Part3Question.objects.none()
        print("No topic selected, returning no questions.")
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/part3.html', {
        'topics': topics,
        'questions': page_obj,
        'selected_topic': selected_topic,
    })

def essentView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            unit_id = data.get('unit_id')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

        if not book_id or not unit_id:
            messages.error(request, "Please select both Book and Unit.")
            return JsonResponse({'success': False, 'message': "Please select both Book and Unit."}, status=400)

        try:
            book = Book.objects.get(id=book_id)
            unit = Unit.objects.get(id=unit_id, book=book)
            messages.success(request, f"Selected {book.name} - {unit.unit_name}.")
            return JsonResponse({'success': True, 'message': f"Selected {book.name} - {unit.unit_name}."})
        except Book.DoesNotExist:
            messages.error(request, "Selected Book does not exist.")
            return JsonResponse({'success': False, 'message': "Selected Book does not exist."}, status=404)
        except Unit.DoesNotExist:
            messages.error(request, "Selected Unit does not exist.")
            return JsonResponse({'success': False, 'message': "Selected Unit does not exist."}, status=404)

    # For GET request, display the form
    books = Book.objects.all().prefetch_related('units')
    book_units = {}
    for book in books:
        book_units[book.id] = [{'id': unit.id, 'unit_num': unit.unit_num, 'unit_name': unit.unit_name} for unit in
                               book.units.all()]
    book_units_json = json.dumps(book_units)
    context = {
        'books': books,
        'book_units_json': book_units_json,
    }
    return render(request, 'essential.html', context)


def testview(request):
    units = Unit.objects.all()
    books = Book.objects.all()
    vocabs = Vocab.objects.all()
    context = {
        'units': units,
        'books': books,
        'vocabs': vocabs
    }
    print(units)
    return render(request, 'tests.html', context)


def get_vocabs(request):
    unit_id = request.GET.get('unit_id')
    if unit_id:
        try:
            unit = Unit.objects.get(id=unit_id)
            vocabs = unit.vocabs.all()
            vocab_list = []
            for vocab in vocabs:
                vocab_list.append({
                    'id': vocab.id,
                    'en': vocab.en,
                    'uz': vocab.uz,
                    'audio_url': vocab.audio_file.url if vocab.audio_file else '',
                })
            return JsonResponse({'vocabs': vocab_list})
        except Unit.DoesNotExist:
            return JsonResponse({'error': 'Unit not found'}, status=404)
    return JsonResponse({'error': 'No unit_id provided'}, status=400)


def start_test(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

        if not unit_id:
            return JsonResponse({'success': False, 'message': 'Unit ID not provided.'}, status=400)

        try:
            unit = Unit.objects.get(id=unit_id)
            vocabs = unit.vocabs.all()

            if not vocabs.exists():
                return JsonResponse({'success': False, 'message': 'No vocabularies found for this Unit.'}, status=404)

            # Previously, we selected only 5 vocabs. Now we use all vocabs:
            test_vocabs = list(vocabs)

            # Convert them all into questions:
            questions = [{'id': v.id, 'en': v.en, 'uz': v.uz} for v in test_vocabs]

            return JsonResponse({'success': True, 'questions': questions})
        except Unit.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Unit does not exist.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


def submit_test(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unit_id = data.get('unit_id')
            answers = data.get('answers')  # Expected to be a list of {'id': vocab_id, 'answer': user_answer}
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

        if not unit_id or not answers:
            return JsonResponse({'success': False, 'message': 'Unit ID or answers not provided.'}, status=400)

        try:
            unit = Unit.objects.get(id=unit_id)
            vocabs = unit.vocabs.filter(id__in=[a['id'] for a in answers])
            vocab_dict = {v.id: v for v in vocabs}
            results = []
            correct_count = 0
            for a in answers:
                vocab_id = a['id']
                user_answer = a['answer'].strip().lower()
                vocab = vocab_dict.get(vocab_id)
                if vocab:
                    correct = (user_answer == vocab.uz.lower())
                    if correct:
                        correct_count += 1
                    results.append({
                        'en': vocab.en,
                        'correct_uz': vocab.uz,
                        'user_answer': a['answer'],
                        'correct': correct,
                    })
            total = len(answers)
            return JsonResponse({'success': True, 'results': results, 'correct_count': correct_count, 'total': total})
        except Unit.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Unit does not exist.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


def readingView(request):
    cambridge_book = CambridgeTest.objects.get(book_name="IELTS 19 Academic 2024")
    reading_sections = cambridge_book.reading_sections.all()
    return render(request, 'reading/reading.html', {'book': cambridge_book, 'sections': reading_sections})
