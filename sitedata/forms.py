"""Forms for Sitedata

"""

from django import forms

from pagedown.widgets import PagedownWidget

from sitedata.models import Feedback


class FeedbackForm(forms.ModelForm):

    """Feedback Form displayed on site
    """

    text = forms.CharField(widget=PagedownWidget())

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
