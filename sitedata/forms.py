"""Forms for Sitedata

"""

from ckeditor.widgets import CKEditorWidget
from django import forms

from sitedata.models import Feedback


class FeedbackForm(forms.ModelForm):

    """Feedback Form displayed on site
    """
    # body = forms.CharField(widget=CKEditorWidget())

    class Meta:

        """Meta options for Feedback Form
        """
        model = Feedback
        fields = (
            'title',
            'text',
            'user_name',
            'user_email',
            'linked_post',
        )
