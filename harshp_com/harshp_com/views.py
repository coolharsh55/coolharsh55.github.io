from django.shortcuts import render

from utils.meta_generator import create_meta


def home(request):
    meta = create_meta(
        title='harshp.com',
        description='personal website & project',
        keywords=['harshp.com', 'coolharsh55'],
        url=request.build_absolute_uri(),
    )
    return render(request, 'sitebase/homepage.html', {'meta': meta})


def stub(request):
    return render(request, 'sitebase/stub.html')
