from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .models import JournalEntry, JournalSection, JournalTag


def auth(request):
    """Authenticate access to Journal"""
    # check if password is supplied via form
    if request.method == 'POST':
        password = request.POST.get('password', None)
        if password is None:
            return render(request, 'journal/auth.html')
        # authenticate the user is ME
        user = authenticate(username='harsh', password=password)
        # login the user
        if user is not None:
            login(request, user)
            return redirect('journal:entries:list')
    # for all other cases, show the journal auth page
    return render(request, 'journal/auth.html')


def tags(request):
    """Display all tags in journal"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    tags = []
    for tag in JournalTag.objects.order_by('name').all():
        tags.append((tag, tag.entries.count()))

    return render(request, 'journal/tags.html', {'tags': tags})


def tag(request, slug):
    """Display posts associated with a tag"""
    if not request.user.is_authenticated():
        return redirect('journal:auth')
    tag = get_object_or_404(JournalTag, slug=slug)
    entries = tag.entries.order_by('date_published').all()
    return render(
        request, 'journal/tag.html',
        {'tag': tag, 'entries': entries})


def entries(request):
    """Display index of all entries"""
    private = False
    if request.user.is_authenticated():
        private = True
    if private:
        entries = [
            (entry, True)
            for entry in
            JournalEntry.objects.order_by('-date_published')]
    else:
        entries = []
        for entry in JournalEntry.objects.order_by(
                '-date_published').select_related('section'):
            if entry.private or entry.section.private:
                entries.append((entry, False))
            else:
                entries.append((entry, True))

    sections = JournalSection.objects
    if not private:
        sections = sections.filter(private=False)
    sections = sections.order_by('name')

    return render(
        request, 'journal/entries.html',
        {'entries': entries, 'sections': sections})


def entry(request, entry_id):
    """Display journal entry"""
    entry = get_object_or_404(JournalEntry, id=entry_id)
    if entry.private or entry.section.private:
        if not request.user.is_authenticated():
            return redirect('journal:auth')

    return render(request, 'journal/entry.html', {'entry': entry})


def sections(request):
    """Sections in the journal"""
    sections = []
    for section in JournalSection.objects.order_by('name').all():
        sections.append((section, section.entries.count()))
    return render(request, 'journal/sections.html', {'sections': sections})


def section(request, slug):
    """Section in the journal"""
    section = get_object_or_404(JournalSection, slug=slug)
    if section.private:
        if not request.user.is_authenticated():
            return redirect('journal:auth')
    entries = section.entries\
        .filter(is_published=True).order_by('-date_published')
    return render(
        request, 'journal/section.html',
        {'entries': entries, 'section': section})


def logout_user(request):
    """Log out the user"""
    # log the user out IF they are logged in
    if request.user.is_authenticated():
        logout(request)
    return redirect('journal:auth')
