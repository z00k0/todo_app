from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from users.models import AppUser
from projects.models import Project, Task
from django import forms
from django.core.exceptions import ValidationError


class Slugifier(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('number', 'name')}


class AppUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AppUser
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AppUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = AppUser
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    form = AppUserChangeForm
    add_form = AppUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'patronymic', 'sex', 'position', 'department', 'birthday',
                    'mobile', 'avatar', 'is_staff', 'is_active', 'start_date')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'patronymic', 'sex', 'position', 'department',
                                      'birthday', 'mobile', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name', 'email')
    filter_horizontal = ()


admin.site.register(AppUser, UserAdmin)
admin.site.register(Project, Slugifier)
admin.site.register(Task)
admin.site.unregister(Group)
