from django.contrib import admin
from .models import (UserRegisterationModel,
                    LevelModel, UserRole,
                    UserQualification, Language,
                    PageName, PageLabel,
                    #  ViewAppName, ViewClass,
                    LanguageInformation,
                    InfoMessages,
                    )
import nested_admin

# Register your models here.

admin.site.register(UserRegisterationModel)
admin.site.register(UserQualification)
# admin.site.register(InfoMessages)

class PageLabelInline(nested_admin.NestedTabularInline):
    extra = 0
    model = PageLabel

class PageNameInline(nested_admin.NestedTabularInline):
    extra = 0
    fk_name = 'language_name'
    model = PageName 
    inlines = [PageLabelInline]

class LanguageAdmin(nested_admin.NestedModelAdmin):  
    inlines = [PageNameInline]

admin.site.register(Language, LanguageAdmin)

class LevelModelInline(nested_admin.NestedTabularInline):
    extra = 0
    max_num = 1
    model = LevelModel

class UserRoleAdmin(nested_admin.NestedModelAdmin):  
    inlines = [LevelModelInline]

admin.site.register(UserRole, UserRoleAdmin)

class InfoMessagesInline(nested_admin.NestedTabularInline):
    extra = 0
    model = InfoMessages


class LanguageInformationMessageAdmin(nested_admin.NestedModelAdmin):  
    extra = 0
    model = LanguageInformation
    inlines = [InfoMessagesInline]

admin.site.register(LanguageInformation, LanguageInformationMessageAdmin)
