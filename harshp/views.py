# VIEWS
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response

from blog.models import BlogPost
from stories.models import StoryPost
from poems.models import Poem
from articles.models import Article
from lifeX.models import LifeXWeek
from brainbank.models import BrainBankIdea

from itertools import chain
from operator import attrgetter
from sitedata.social_meta import create_meta

def home(request, page=''):
	try:
		blogs = BlogPost.objects.order_by('-published')[:3]
		stories = StoryPost.objects.order_by('-published')[:3]
		poems = Poem.objects.order_by('-published')[:3]
		articles = Article.objects.order_by('-published')[:3]
		brainbank_idea = BrainBankIdea.objects.latest('published')
		lifeXweek = LifeXWeek.objects.latest('number')
		description = 'The personal website of Harshvardhan Pandit (coolharsh55)'
		keywords = ['harshp.com','blog','stories','poems',]
		meta = create_meta('harshp.com', description, keywords, url=request.build_absolute_uri(),)
	except (BlogPost.DoesNotExist,
			StoryPost.DoesNotExist,
			Poem.DoesNotExist,
			Article.DoesNotExist,
			LifeXWeek.DoesNotExist,
			BrainBankIdea.DoesNotExist):
		raise Http404('Error retrieving website data...')
	return render_to_response('harshp/index.html', {
		'blogs':blogs, 'stories':stories, 'poems':poems, 'articles':articles,
		'brainbank_idea':brainbank_idea, 'lifeXweek':lifeXweek, 'meta':meta,})

def changelog(request):
	return render_to_response('harshp/changelog.html')

def privacypolicy(request):
	return render_to_response('harshp/privacypolicy.html')