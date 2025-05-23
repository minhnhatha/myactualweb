from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
class LoaiSanPham(models.Model):
    ten = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    def __str__(self):
        return self.ten
# Create your models here.
def up(instance, filename):
    loai_slug = instance.loai.slug  
    return f'{loai_slug}/{filename}'
class SanPham(models.Model):
    ten = models.CharField(max_length=255)
    loai = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE)
    gia = models.IntegerField(default=0)
    anh = models.ImageField(upload_to=up)
    chitiet = models.TextField()
    soluong = models.IntegerField(default=0)
    def __str__(self):
        return self.ten
class Item(models.Model):
    ten = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    soluong = models.IntegerField(default=0)
    trangthai = models.BooleanField(default=False)
    def sotien(self):
        return self.product.gia * self.soluong
class DonHang(models.Model):
    ten = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)
    trangthai = models.BooleanField(default=False)
    tenkhach = models.CharField(max_length=255)
    sdt = models.CharField(max_length=20)
    email = models.EmailField()
    diachi = models.CharField(max_length=255)
    ngaydathang = models.DateTimeField(default=now)
    ghichu = models.TextField()
    def tongtien(self):
        tien = 0
        item_list = self.item.all()
        for i in item_list:
            tien += i.sotien()
        return tien