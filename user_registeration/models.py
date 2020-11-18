from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from model_utils import Choices


ORDER_COLUMN_CHOICES = Choices(
    ('0', 'profile_picture'),
    ('1', 'user_name'),
    ('2', 'email'),
    ('3', 'resume'),
    ('4', 'pan_card'),
    ('5', 'adhar_card'),
    ('6', 'user_id')
)

# Create your models here.
class UserRegisterationModel(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=False)
    user_name = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    middle_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=False)
    email = models.EmailField(max_length=100, null=False)
    telephone = models.IntegerField(null=False)
    gender = models.CharField(max_length=10, null=False)
    address = models.TextField(max_length=1100, null=False)
    indian = models.BooleanField(null=False)
    option = models.IntegerField(null=False)
    role = models.IntegerField(null=False, default=3)
    profile_picture = models.FileField(upload_to='profile_picture/', null=True)
    resume = models.FileField(upload_to='resume/', null=True)
    pan_card = models.FileField(upload_to='pan_card/', null=True)
    adhar_card = models.FileField(upload_to='adhar_card/', null=True)
    class Meta:
        verbose_name_plural = "1. User Registration"
    def __str__(self):
        return '{}' .format(self.first_name)

class UserRole(models.Model):
    role_no = models.IntegerField(null=False)
    role_name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "2. Role Permissions"
    def __str__(self):
        return '{}' .format(self.role_name)

class LevelModel(models.Model):
    level = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=False)
    add_user = models.BooleanField(null=False)
    view_user = models.BooleanField(null=False)
    edit_user = models.BooleanField(null=False)
    delete_user = models.BooleanField(null=False)

    def __str__(self):
        return '{}' .format(self.level)

class UserQualification(models.Model):
    qualification_no = models.IntegerField(null=False)
    qualification_name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "3. Qualifications"
    def __str__(self):
        return '{}' .format(self.qualification_name)


def query_users_by_args(request,**kwargs):
    check_user_is_superuser = User.objects.filter(username = request.user.username).values('is_superuser')
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    if order == 'desc':
        order_column = '-' + order_column

    if check_user_is_superuser[0]['is_superuser'] == True:
        queryset = UserRegisterationModel.objects.all()
    else:
        getuserid = UserRegisterationModel.objects.filter(user_name = request.user.username).values('role')
        user_id = getuserid[0]['role']
        queryset = UserRegisterationModel.objects.filter(role__gte = user_id)

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                        Q(user_name__icontains=search_value) |
                                        Q(email__icontains=search_value)
                                        ) 


    count = queryset.count()

    queryset = queryset[start:start + length]

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }

class Language(models.Model):
    language_name = models.CharField(max_length=100, null=False)
    class Meta:
        verbose_name_plural = "4 Add Languages"
    def __str__(self):
        return '{}' .format(self.language_name) 

class PageName(models.Model):
    language_name = models.ForeignKey(Language, on_delete=models.CASCADE,null=False)
    page_name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return '{}' .format(self.page_name) 

class PageLabel(models.Model):
    page_name = models.ForeignKey(PageName, on_delete=models.CASCADE,null=False)
    page_label_class_name = models.CharField(max_length=100, null=False)
    page_label_text = models.CharField(max_length=100, null=False)
    def __str__(self):
        return '{}' .format(self.page_label_class_name)

class LanguageInformation(models.Model):    
    language_name = models.ForeignKey(Language, on_delete=models.CASCADE,null=False)
    class Meta:
        verbose_name_plural = "5 Add Information message"

    def __str__(self):
        return '{}-{}' .format(self.language_name, "information_msg")


class InfoMessages(models.Model):
    language_name = models.ForeignKey(LanguageInformation, on_delete=models.CASCADE,null=False)
    message_label = models.CharField(max_length=100)
    message = models.CharField(max_length=100)


    