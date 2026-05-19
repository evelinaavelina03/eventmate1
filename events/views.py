from django.shortcuts import render

def event_list(request):
    # Пока просто показываем шаблон-заглушку (без данных из БД)
    return render(request, 'events/event_list.html', {'events': []})

def event_detail(request, event_id):
    # Заглушка
    return render(request, 'events/event_detail.html', {'event': None})