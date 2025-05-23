from django.shortcuts import render, redirect
from .models import Folder, File, FileVersion, FileAnnotation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Max, Q

@login_required
def folder_list(request):
    query = request.GET.get('q', '')
    folders = Folder.objects.filter(parent=None)
    if query:
        folders = folders.filter(Q(name__icontains=query) | Q(files__name__icontains=query) | Q(files__description__icontains=query) | Q(files__tags__icontains=query)).distinct()
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Folder.objects.create(name=name, owner=request.user)
            return redirect('folder_list')
    return render(request, 'files/folder_list.html', {'folders': folders, 'query': query})

@login_required
def folder_detail(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    query = request.GET.get('q', '')
    subfolders = folder.subfolders.all()
    files = folder.files.all()
    if query:
        subfolders = subfolders.filter(name__icontains=query)
        files = files.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query))
    # Folder creation inside current folder
    if request.method == 'POST' and 'create_folder' in request.POST:
        name = request.POST.get('name')
        if name:
            Folder.objects.create(name=name, parent=folder, owner=request.user)
            return redirect('folder_detail', folder_id=folder.id)
    # File upload
    if request.method == 'POST' and 'upload_file' in request.POST:
        uploaded_file = request.FILES.get('file')
        description = request.POST.get('description', '')
        tags = request.POST.get('tags', '')
        if uploaded_file:
            File.objects.create(
                folder=folder,
                name=uploaded_file.name,
                file=uploaded_file,
                description=description,
                tags=tags,
                owner=request.user
            )
            return redirect('folder_detail', folder_id=folder.id)
    return render(request, 'files/folder_detail.html', {'folder': folder, 'subfolders': subfolders, 'files': files, 'query': query})

@login_required
def folder_rename(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    if request.user != folder.owner:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            folder.name = name
            folder.save()
            return redirect('folder_detail', folder_id=folder.id)
    return render(request, 'files/folder_rename.html', {'folder': folder})

@login_required
def folder_delete(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    parent_id = folder.parent.id if folder.parent else None
    if request.user != folder.owner:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        folder.delete()
        if parent_id:
            return redirect('folder_detail', folder_id=parent_id)
        else:
            return redirect('folder_list')
    return render(request, 'files/folder_delete.html', {'folder': folder})

def file_detail(request, file_id):
    file = File.objects.get(id=file_id)
    versions = file.versions.all()
    annotation_error = None
    if request.method == 'POST' and request.user.is_authenticated:
        if 'new_version' in request.FILES:
            uploaded_file = request.FILES.get('new_version')
            comment = request.POST.get('comment', '')
            if uploaded_file:
                max_version = versions.aggregate(Max('version_number'))['version_number__max'] or 0
                FileVersion.objects.create(
                    file=file,
                    version_number=max_version + 1,
                    file_data=uploaded_file,
                    comment=comment
                )
                file.file = uploaded_file
                file.save()
                return redirect('file_detail', file_id=file.id)
        elif 'annotation_text' in request.POST:
            version_id = request.POST.get('version_id')
            text = request.POST.get('annotation_text', '').strip()
            if version_id and text:
                version = FileVersion.objects.get(id=version_id)
                FileAnnotation.objects.create(version=version, user=request.user, text=text)
                return redirect('file_detail', file_id=file.id)
            else:
                annotation_error = 'Note cannot be empty.'
    return render(request, 'files/file_detail.html', {'file': file, 'versions': versions, 'annotation_error': annotation_error})

def file_upload(request):
    # Placeholder for file upload
    return HttpResponse('File upload page (to be implemented)')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('folder_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

