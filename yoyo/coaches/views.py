from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Coach
from .utils import generate_qr_code


class SearchView(ListView):
    model = Coach
    paginate_by = 10
    context_object_name = 'coaches'
    template_name = 'yoyo/search.html'
    allow_empty = False

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if len(self.object_list) == 1:
            coach = self.object_list.first()
            return redirect('yoyo:detail', pk=coach.pk)

        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                return redirect('yoyo:index')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self) -> list:
        try:
            value = self.request.GET['q']
            if not value:
                return []
            else:
                self.allow_empty = True
        except KeyError:
            return []

        values = value.split(' ', 2)

        # first_name = None
        # last_name = None
        # second_name = None
        #
        # for value in values:
        #     if str(value).endswith(('ан', 'ын', 'ин', 'ских', 'ов', 'ев', 'ской', 'цкой', 'их', 'ых')):
        #         last_name = value
        #     elif str(value).endswith(('ович', 'евич', 'ич', 'овна', 'евна', 'ична', 'инична')):
        #         second_name = value
        #     else:
        #         first_name = value

        # result = self.model.objects.filter_by_fio(
        #     first_name=first_name,
        #     last_name=last_name,
        #     second_name=second_name,
        # )
        result = self.model.objects.filter_by_fio(values)
        return result


class CoachDetail(DetailView):
    model = Coach
    context_object_name = 'coach'
    template_name = 'yoyo/detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            context.update({
                'qr_code': generate_qr_code(self.object, self.request)
            })
        context.update(kwargs)
        return super().get_context_data(**context)
