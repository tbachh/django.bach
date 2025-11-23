from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos,
        'total': todos.count(),
        'completed': todos.filter(completed=True).count(),
        'pending': todos.filter(completed=False).count(),
    }
    return render(request, 'myapp/todo_list.html', context)

def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title:
            Todo.objects.create(title=title, description=description)
            messages.success(request, 'Đã thêm công việc mới!')
        else:
            messages.error(request, 'Vui lòng nhập tiêu đề!')
    
    return redirect('myapp:todo_list')

def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    
    if todo.completed:
        messages.success(request, f'Đã hoàn thành: {todo.title}')
    else:
        messages.info(request, f'Đã đánh dấu chưa hoàn thành: {todo.title}')
    
    return redirect('myapp:todo_list')

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    title = todo.title
    todo.delete()
    messages.success(request, f'Đã xóa: {title}')
    return redirect('myapp:todo_list')