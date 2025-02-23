from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView

from apps.forms import EmployeeCreateForm, EmployeeForm
from apps.models import ApplicationType, Application
from apps.models import Employee


class EmployeeCreateView(FormView, ListView):
    form_class = EmployeeCreateForm
    queryset = ApplicationType.objects.all()
    context_object_name = 'applications'
    template_name = 'admin/create-employee.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        fullname = form.cleaned_data['fullname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        pk = form.cleaned_data['pk']
        application = ApplicationType.objects.get(pk=pk)
        employee = Employee.objects.filter(username=username, password=password).first()
        if employee:
            return super().form_invalid(form)
        else:
            Employee.objects.create(username=username, password=password, ApplicationType=application,
                                    fullname=fullname)
            return super(EmployeeCreateView, self).form_valid(form)


class EmployeeListView(ListView):
    queryset = Employee.objects.all()
    context_object_name = 'employees'
    template_name = 'admin/employee-list.html'


@csrf_exempt
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.delete()
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


class EmployeeCreateFormView(FormView):
    form_class = EmployeeForm
    template_name = 'apps/employee-form.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        employee = Employee.objects.filter(username=username).first()

        if employee and password == employee.password:
            application = Application.objects.filter(ApplicationType_id=employee.ApplicationType.pk).all()
            context = {

                'videos': application,
            }

            return render(self.request, 'apps/video.html', context)

        else:
            form.add_error('password', 'Username yoki password noto\'g\'ri!')
            return self.form_invalid(form)


@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'DELETE':
        category = get_object_or_404(ApplicationType, pk=category_id)
        category.delete()
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


