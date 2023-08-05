from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import User, Project, ProjectCategory, ProjectStatus, ProjectStage, ProjectActivity, Company

class ProjectCenterUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            "is_staff": "Can Login"
        }


class ProjectCenterUserAdmin(UserAdmin):

    form = ProjectCenterUserForm
    list_display = ['id', 'first_name', 'last_name', 'email', 'company', 'is_staff', 'email_notify']
    search_fields = ['last_name', 'email']
    readonly_fields = []
    list_filter = ['company', 'groups', 'is_staff', 'email_notify']
    fieldsets = (

        (_("Personal info"), {"fields": (("first_name", "last_name"), "email", "title", "company",
                                         "address_1",
                                         ("city", "state", "postal_code"), "primary_phone",
                                         ("email_notify",),
                                         )}),
        (_("Authentication"), {"fields": ("username", "password")}),
        # (_("Commdep info"), {"fields": (
        #     "company",
        #     "address_1",
        #     ("city", "state", "postal_code"),
        #     ("title", "primary_phone",),
        #    )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Other/Legacy"), {"fields": ("import_id",)}),
    )

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        return obj

    # inlines = [ApplicationInline, AttachmentsInline]


class CompanyProjectsInline(admin.TabularInline):
    model = Project
    readonly_fields = ('last_activity', 'last_activity_date')
    fields = ('title', 'last_activity', 'last_activity_date', 'status', 'stage', 'category',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CompanyUsersInline(admin.TabularInline):
    model = User
    # readonly_fields = ('jobId', 'jobTitle', 'created',)
    fields = ('first_name', 'last_name', 'email')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['name', ]
    ordering = ['name']

    inlines = [CompanyProjectsInline, CompanyUsersInline]


admin.site.register(Company, CompanyAdmin)


class ProjectActivityInline(admin.TabularInline):
    model = ProjectActivity
    readonly_fields = ('name', 'date', 'user', 'get_download_link')
    fields = ('name', 'date', 'user', 'get_download_link')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'last_activity', 'status', 'stage', 'category', 'internal')
    list_filter = ['company', 'category', 'status', 'stage', 'internal']
    search_fields = ['title', 'code', ]
    filter_horizontal = ['users']
    ordering = ['title']
    inlines = [ProjectActivityInline]
    fieldsets = (

        (_("Project info"), {"fields": ("title", ("company", "category"), ("status", "stage", "internal")
                                         )}),
        (_("Project Users"), {"fields": ("users",)}),
        # (_("Commdep info"), {"fields": (
        #     "company",
        #     "address_1",
        #     ("city", "state", "postal_code"),
        #     ("title", "primary_phone",),
        #    )}),
    )

    def last_activity(self, obj):
        return obj.projectactivity_set.order_by('-date').first()

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(ProjectAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Restrict the list of authors to Super Users and Staff only.
        """
        if db_field.name == 'users':
            if request.user.is_superuser or request.user.groups.filter(name='Commdep Admin').exists():
                """Do we filter for admins?"""
                kwargs['queryset'] = User.objects.filter(is_active=True, is_staff=True, company=self.instance.company)
            else:
                kwargs['queryset'] = User.objects.filter(is_active=True, is_staff=True, company=self.instance.company)

        return super(ProjectAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Project, ProjectAdmin)


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project', 'user', 'date', 'get_download_link')
    search_fields = ['name', 'file', ]
    ordering = ('-date',)

    def get_queryset(self, request):
        qs = super(ProjectActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Commdep Administrator').exists():
            return qs
        else:
            try:
                return qs.filter(project__company=request.user.company)
            except:
                return None


admin.site.register(ProjectActivity, ProjectActivityAdmin)


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(ProjectCategory, ProjectCategoryAdmin)


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(ProjectStatus, ProjectStatusAdmin)


class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(ProjectStage, ProjectStageAdmin)

admin.site.register(User, ProjectCenterUserAdmin)
