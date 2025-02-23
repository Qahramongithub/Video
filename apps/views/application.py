import os

from django.conf import settings
from django.db.models import Min
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, FormView

from apps.forms import VideoModelForm
from apps.models import ApplicationType, Application
from root import settings


class ApplicationListView(ListView):
    queryset = ApplicationType.objects.all()
    template_name = 'admin/video.html'
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        max_id = ApplicationType.objects.aggregate(min_pk=Min('pk'))['min_pk']  # Faqat sonni olamiz

        if max_id:  # Agar max_id mavjud bo'lsa
            context['videos'] = Application.objects.filter(ApplicationType_id=max_id)  # Faqat id qiymatini beramiz
        else:
            context['videos'] = Application.objects.none()  # Bo'sh queryset qaytarish

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


class VideoCreateView(FormView):
    queryset = Application.objects.all()
    form_class = VideoModelForm
    template_name = 'admin/video-create.html'

    def form_valid(self, form):
        print(self)

    def form_invalid(self, form):
        print(self)
