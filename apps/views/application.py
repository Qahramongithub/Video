import os

from django.conf import settings
from django.db.models import Min
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, FormView, View

from apps.forms import VideoModelForm, ApplicationTypeForm
from apps.models import ApplicationType, Application
from root import settings


class ApplicationListView(ListView):
    queryset = ApplicationType.objects.all()
    template_name = 'admin/video.html'
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        min_id = ApplicationType.objects.aggregate(min_pk=Min('pk'))['min_pk']

        context['videos'] = Application.objects.filter(
            ApplicationType__pk=min_id) if min_id else Application.objects.none()

        return context


class ApplicationFilterView(ListView):
    queryset = ApplicationType.objects.all()
    template_name = 'admin/video.html'
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.request.GET.get('pk')
        if pk:
            videos = Application.objects.filter(ApplicationType=pk)

            context['videos'] = videos
        else:
            context['videos'] = Application.objects.none()
        return context


def file_iterator(file_path, chunk_size=1048576):
    """ Faylni qism-qism qilib uzatish (chunking) """
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


def stream_video(request, video_id):
    """ Videoni streaming qilish uchun view """

    video = get_object_or_404(Application, id=video_id)
    video_path = os.path.join(settings.MEDIA_ROOT, str(video.video))

    if not os.path.exists(video_path):
        return HttpResponse("Fayl topilmadi", status=404)

    response = StreamingHttpResponse(file_iterator(video_path), content_type="video/mp4")
    response["Content-Disposition"] = f"inline; filename={video.video.name}"
    response["Accept-Ranges"] = "bytes"

    return response


class VideoCreateView(FormView, ListView):
    form_class = VideoModelForm
    queryset = ApplicationType.objects.all()
    template_name = 'admin/video-create.html'
    success_url = reverse_lazy('application-list')
    context_object_name = 'applications'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CategoryCreate(FormView):
    form_class = ApplicationTypeForm
    template_name = 'admin/category-create.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CategoryListView(ListView):
    queryset = ApplicationType.objects.all()
    template_name = 'admin/category-list.html'
    context_object_name = 'applications'


@csrf_exempt  # CSRF tokenni tekshirishga hojat yo'q (JS-da ishlatayotgan bo‘lsangiz)
def delete_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Application, id=video_id)
        video.delete()
        return JsonResponse({"message": "Video muvaffaqiyatli o‘chirildi!"})

    return JsonResponse({"error": "Faqat POST so‘rov qabul qilinadi!"}, status=400)
