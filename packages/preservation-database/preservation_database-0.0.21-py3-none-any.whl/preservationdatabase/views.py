from django.http import Http404
from django.shortcuts import render

import preservationdatabase.utils


def index(request):
    context = {}

    if request.POST:
        doi = request.POST.get('doi', None)
        doi = preservationData.utils.normalize_doi(doi)

        # lookup request
        if doi:
            context['preservations'], context['doi'] = \
                preservationData.utils.show_preservation_for_doi(doi)

    template = 'index.html'

    return render(
        request,
        template,
        context,
    )
