from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(SanPham)
admin.site.register(LoaiSanPham)
admin.site.register(Item)
@admin.register(DonHang)
class DonHangAdmin(admin.ModelAdmin):
    list_display = ['id', 'ten', 'trangthai', 'tong_tien_display']

    def tong_tien_display(self, obj):
        return f"{obj.tongtien():,} ₫"
    tong_tien_display.short_description = 'Tổng tiền'