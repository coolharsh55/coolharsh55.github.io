from django.db import models
from subdomains.utils import reverse
from django.utils import timezone
import markdown

from sitebase.editors import EDITOR_TYPES
from utils.models import get_unique_slug
from sitebase.models import Post


class Poem(Post):
    """A poem on harshp_com"""

    body_type = models.CharField(
        max_length=8, choices=EDITOR_TYPES, default='markdown')
    body_text = models.TextField(blank=True)
    body = models.TextField()
    headerimage = models.URLField(max_length=256, blank=True, null=True)
    highlight = models.BooleanField(default=False, db_index=True)

    class Meta(object):

        verbose_name = 'Poem'
        verbose_name_plural = 'Poems'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                Poem, self, 'title', title=self.title)
        self.date_updated = timezone.now()
        if self.body_type == 'markdown':
            self.body_text = markdown.markdown(self.body, extensions=[
                'markdown.extensions.abbr',
                # 'markdown.extensions.codehilite',
                'markdown.extensions.smarty',
            ], output_format='html5')
        else:
            self.body_text = self.body
        super(Poem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poems:poem', args=[self.slug], subdomain='poems')

    def get_seo_meta(self):
        """get meta properties for this object"""
        meta = super(Poem, self).get_seo_meta()
        if self.headerimage:
            meta['image'] = self.headerimage
        return meta
