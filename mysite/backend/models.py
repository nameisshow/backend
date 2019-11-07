from django.db import models


class Button(models.Model):
    """
    按钮表
    """
    name = models.CharField(max_length=32, unique=True, help_text='按钮名')
    event = models.CharField(max_length=32, unique=True, help_text='按钮所对应的js方法名')
    type = models.CharField(max_length=32, default='', help_text='按钮出发的操作类型')
    sort = models.IntegerField(default=0, help_text='排序')


class Module(models.Model):
    """
    模块表
    """
    name = models.CharField(max_length=32, unique=True, help_text='按钮名')
    pid = models.IntegerField(default=0, help_text='模块父级id')
    sort = models.IntegerField(default=0, help_text='排序')
    buttons = models.ManyToManyField(Button)
    url = models.CharField(default='', max_length=128, help_text='模块链接')


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, unique=True, help_text='角色名')
    desc = models.CharField(max_length=300, default='', help_text='关于角色的描述')
    modules = models.ManyToManyField(Module)
    buttons = models.ManyToManyField(Button)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()


class Admin(models.Model):
    """
    管理员表
    """
    username = models.CharField(max_length=64, unique=True, help_text='用户名')
    password = models.CharField(max_length=32, help_text='混合盐值的32位md5密码（md5(密码+盐值)）')
    salt = models.CharField(max_length=6, help_text='盐值，6位随机字符串')
    real_name = models.CharField(max_length=32, default='', help_text='真实姓名')
    mobile = models.CharField(max_length=11, default='', help_text='手机号码')
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

