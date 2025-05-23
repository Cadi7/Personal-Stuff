from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Folder, File, FileVersion, FileAnnotation, SharedFile
from .forms import FolderForm, FileForm, FileVersionForm, AnnotationForm, ShareForm
from django.utils import timezone

@login_required
def folder_list(request):
    folders = Folder.objects.filter(owner=request.user, parent=None, is_deleted=False)
    return render(request, 'files/folder_list.html', {'folders': folders})

@login_required
def folder_detail(request, pk):
    folder = get_object_or_404(Folder, pk=pk, owner=request.user, is_deleted=False)
    subfolders = folder.subfolders.filter(is_deleted=False)
    files = folder.files.filter(is_deleted=False)
    return render(request, 'files/folder_detail.html', {
        'folder': folder, 'subfolders': subfolders, 'files': files
    })

@login_required
def folder_create(request, parent_pk=None):
    parent = None
    if parent_pk:
        parent = get_object_or_404(Folder, pk=parent_pk, owner=request.user)
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.parent = parent
            folder.save()
            return redirect('files:folder_detail', pk=folder.pk)
    else:
        form = FolderForm()
    return render(request, 'files/folder_form.html', {'form': form, 'parent': parent})

@login_required
def folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk, owner=request.user)
    folder.delete()
    return redirect('files:folder_list')

@login_required
def file_upload(request, folder_pk):
    folder = get_object_or_404(Folder, pk=folder_pk, owner=request.user)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.folder = folder
            file.save()
            return redirect('files:folder_detail', pk=folder.pk)
    else:
        form = FileForm()
    return render(request, 'files/file_form.html', {'form': form, 'folder': folder})

@login_required
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk, owner=request.user)
    file.delete()
    return redirect('files:folder_detail', pk=file.folder.pk)

@login_required
def file_detail(request, pk):
    file = get_object_or_404(File, pk=pk)
    versions = file.versions.all()
    shared = file.shared_with.all()
    annotations = FileAnnotation.objects.filter(version__file=file)
    return render(request, 'files/file_detail.html', {
        'file': file, 'versions': versions, 'shared': shared, 'annotations': annotations
    })

@login_required
def file_restore(request, pk):
    file = get_object_or_404(File, pk=pk, owner=request.user, is_deleted=True)
    file.is_deleted = False
    file.deleted_at = None
    file.save()
    return redirect('files:folder_detail', pk=file.folder.pk)

@login_required
def share_file(request, pk):
    file = get_object_or_404(File, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            shared_file = form.save(commit=False)
            shared_file.file = file
            shared_file.save()
            return redirect('files:file_detail', pk=file.pk)
    else:
        form = ShareForm()
    return render(request, 'files/share_form.html', {'form': form, 'file': file})

@login_required
def add_annotation(request, version_pk):
    version = get_object_or_404(FileVersion, pk=version_pk)
    if request.method == 'POST':
        form = AnnotationForm(request.POST)
        if form.is_valid():
            annotation = form.save(commit=False)
            annotation.version = version
            annotation.user = request.user
            annotation.save()
            return redirect('files:file_detail', pk=version.file.pk)
    else:
        form = AnnotationForm()
    return render(request, 'files/annotation_form.html', {'form': form, 'version': version})

# Add more views as needed for version upload, edit, trash list, etc.