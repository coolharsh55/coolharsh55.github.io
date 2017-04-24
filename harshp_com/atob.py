from blog.models import BlogSeries, BlogPost
from articles.models import ArticleSeries, Article

aseries = list(ArticleSeries.objects.all())
for s in aseries:
	# print(s.title, len(s.article_set.all()))
	try:
		bs = BlogSeries.objects.get(slug=s.slug)
	except BlogSeries.DoesNotExist:
		bs = BlogSeries()
		bs.title = s.title
		bs.short_description = s.short_description
		bs.slug = s.slug
		bs.save()
		print('{} series added'.format(bs.title))
		continue
	print('{} series exists'.format(s.title))

articles = list(Article.objects.order_by('date_published'))
for a in articles:
	try:
		bp = BlogPost.objects.get(slug=a.slug)
	except BlogPost.DoesNotExist:
		print('{} to be added'.format(a.title))
		bp = BlogPost()
		bp.title = a.title
		bp.date_created = a.date_created
		bp.date_published = a.date_published
		bp.date_updated = a.date_updated
		bp.is_published = True
		bp.short_description = a.short_description
		bp.slug = a.slug
		if a.series is not None:
			bs = BlogSeries.objects.get(slug=a.series.slug)
			bp.series = bs
		bp.body = a.body
		bp.headerimage = a.headerimage
		bp.highlight = a.highlight
		bp.save()
		for tag in a.tags.all():
			bp.tags.add(tag)
		for author in a.authors.all():
			bp.authors.add(author)
		bp.save()
		continue
	print('{} post exists'.format(a.title))
