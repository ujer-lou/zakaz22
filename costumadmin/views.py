from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from costumadmin.forms import UnitForm
from costumadmin.models import Unit, Book, WritingTask1


def units_view(request):
    units = Unit.objects.all()
    books = Book.objects.all()  # Assuming `Book` is a related model
    return render(request, 'admin/admin_unit.html', {'units': units, 'books': books})


def add_writing_task(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        question = request.POST.get('question')
        photo = request.FILES.get('photo') if 'photo' in request.FILES else None
        WritingTask1.objects.create(type=type, question=question, photo=photo)
        return redirect(reverse('task1'))
    return redirect(reverse('task1'))


def writing1_view(request):
    task1_list = WritingTask1.objects.all()  # Retrieve all tasks
    paginator = Paginator(task1_list, 10)  # Paginate with 10 items per page
    page = request.GET.get('page')  # Get the page number from the query parameters
    task1 = paginator.get_page(page)  # Get the tasks for the required page
    return render(request, 'admin/admin_writing1.html', {
        'writings': task1,
        'type_choices': WritingTask1.TYPE_CHOICES
    })


def writing2_view(request):
    task1 = WritingTask1.objects.all()
    return render(request, 'admin/admin_writing1.html', context={'writings': task1})


def admin_main_view(request):
    return render(request, 'admin/admin.html')


def add_unit(request):
    if request.method == "POST":
        unit_name = request.POST.get("unit_name")
        unit_num = request.POST.get("unit_num")
        book_id = request.POST.get("book")

        if not all([unit_name, unit_num, book_id]):
            return JsonResponse({"success": False, "error": "Barcha maydonlarni to'ldiring."})

        book = get_object_or_404(Book, id=book_id)
        Unit.objects.create(unit_name=unit_name, unit_num=unit_num, book=book)

        # POST-Redirect-GET naqshini qo'llash
        return redirect("units")  # Bu URL "admin_unit" nomli marshrutga yo'naltiradi

    # GET so'rovda faqat forma ko'rsatiladi
    return render(request, "admin/admin_unit.html")


def delete_unit(request, unit_id):
    if request.method == 'DELETE':
        try:
            unit = Unit.objects.get(id=unit_id)
            unit.delete()
            return JsonResponse({'success': True, 'message': 'Unit deleted successfully.'}, status=200)
        except Unit.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Unit not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Unit muvaffaqiyatli yangilandi.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # GET so'rov uchun ma'lumot qaytarish
    data = {
        'unit_num': unit.unit_num,
        'unit_name': unit.unit_name,
        'book_id': unit.book.id,
    }
    return JsonResponse(data)
