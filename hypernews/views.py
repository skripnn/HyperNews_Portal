from django.shortcuts import redirect
from django.views import View


class Main(View):
    def get(self, request):
        return redirect('news/')
