from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from .models import *


# Register your models here.


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('dept_no', 'dept_name')
    list_filter = ()
    search_fields = []


class DeptEmpAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'dept_no', 'from_date', 'to_date')


class DeptManagerAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'dept_no', 'from_date', 'to_date')


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'first_name', 'last_name', 'gender', 'birth_date', 'hire_date')
    list_filter = ('gender', 'last_name',
                   ('hire_date', DateRangeFilter),
                   )
    search_fields = ['emp_no', 'first_name']


class SalariesAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'salary', 'from_date', 'to_date')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('emp_no', 'title', 'from_date', 'to_date')


# 클래스를 어드민 사이트에 등록한다.
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(DeptEmp, DeptEmpAdmin)
admin.site.register(DeptManager, DeptManagerAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Salaries, SalariesAdmin)
admin.site.register(Titles, TitlesAdmin)

# admin.site.register(Departments)
# admin.site.register(DeptEmp)
# admin.site.register(DeptManager)
# admin.site.register(Employees)
# admin.site.register(Salaries)
# admin.site.register(Titles)