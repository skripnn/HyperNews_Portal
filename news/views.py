from django.shortcuts import render
from django.views import View


class ComingSoon(View):
    def get(self, request):
        return render(request, 'news/coming_soon.html')
