from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from apps.forms import AdminLoginForm
from apps.models import Admin


class AdminFormView(FormView):
    form_class = AdminLoginForm
    template_name = 'admin/admin.html'
    success_url = reverse_lazy('application-list')

    def form_valid(self, form):
        # Kiritilgan foydalanuvchi nomi va parolni olish
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        admin = Admin.objects.filter(username=username).first()

        if admin:
            # Parolni tekshirish (Django'da parollarni qiyoslashda check_password dan foydalanish kerak)
            if password == admin.password:  # Adminning parolini tekshiradi
                return super().form_valid(form)
            else:
                # Xatolik xabari
                form.add_error('password', 'Foydalanuvchi topilmadi')
        else:
            # Agar admin topilmasa
            form.add_error('username', 'Foydalanuvchi topilmadi')

        return self.form_invalid(form)
