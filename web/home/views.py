from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from home.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from django.utils.timezone import now
# Create your views here.
def mainhome(request):
    sanpham = SanPham.objects.all()
    loai = LoaiSanPham.objects.all()
    use = request.user
    nofi = 0
    if use.is_authenticated: nofi = len(DonHang.objects.filter(ten = use, trangthai = False))
    data = {
        'sanpham': sanpham,
        'loai':loai,
        'use': use,
        'nofi': nofi,
    }
    return render(request, "home.html", data)
def listhome(request):
    jk = SanPham.objects.all()
    if request.method == "POST":
        search_query = request.POST.get('search', '').strip()
        sanpham = SanPham.objects.filter(ten__icontains=search_query)
    else:
        sanpham = jk
    use = request.user
    nofi = 0
    if use.is_authenticated: nofi = len(DonHang.objects.filter(ten = use, trangthai = False))
    loai = LoaiSanPham.objects.all()
    data = {
        'jk': jk,
        'sanpham': sanpham,
        'loai':loai,
        'use':use,
        'nofi': nofi,
    }
    return render(request, "list.html", data)
def sortlisthome(request, loai):
    jk = SanPham.objects.filter(loai__slug = loai)
    if request.method == "POST":
        search_query = request.POST.get('search', '').strip()
        sanpham = SanPham.objects.filter(ten__icontains=search_query, loai__slug = loai)
    else:
        sanpham = jk 
    use = request.user
    nofi = 0
    if use.is_authenticated: nofi = len(DonHang.objects.filter(ten = use, trangthai = False))
    kind = LoaiSanPham.objects.all()
    type = LoaiSanPham.objects.get(slug = loai)
    data = {
        'jk': jk,
        'sanpham': sanpham,
        'loai':kind,
        'type': type.ten,
        'use':use,
        'nofi': nofi,
    }
    return render(request, "sortlist.html", data)
def detailhome(request, pk):
    try:
        sanpham = SanPham.objects.get(id = pk)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        raise Http404("Bún không bún")
    loai = LoaiSanPham.objects.all()
    kind = SanPham.objects.filter(loai = sanpham.loai).exclude(id=pk)[:5]
    use = request.user
    nofi = 0
    if use.is_authenticated: nofi = len(DonHang.objects.filter(ten = use, trangthai = False))
    data = {
        'sanpham': sanpham,
        'loai':loai,
        'use':use,
        'nofi': nofi,
        'kind': kind,
    }
    return render(request, "detail.html", data)
def add_to_cart(request, id):
    use = request.user.is_authenticated
    if use:
        try:
            sanpham = SanPham.objects.get(id=id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Sản phẩm không tồn tại hoặc có lỗi dữ liệu.")
        khachhang = request.user
        order, created = DonHang.objects.get_or_create(ten = khachhang, trangthai = False)
        orderitem, created = Item.objects.get_or_create(ten = khachhang, trangthai = False, product = sanpham)
        if orderitem.soluong == 0:
            orderitem.soluong = 1
            orderitem.save()
            order.item.add(orderitem)
        else:
            orderitem.soluong = min(min(orderitem.soluong + 1, orderitem.product.soluong), 20)
            orderitem.save()
        return redirect("list")
    return redirect('signin')
def profile(request):
    if request.user.is_authenticated:
        khachhang = request.user
        orders = DonHang.objects.filter(ten = khachhang).order_by('-ngaydathang')
        info = User.objects.get(id = khachhang.id)
        # if request.method=="UP":
        #     orderitem.soluong += 1
        #     orderitem.save()
        # if request.method=="DOWN":
        #     orderitem.soluong = max(orderitem.soluong - 1, 0)
        #     orderitem.save()
        data={'orders': orders,'info':info,'app':len(orders),}
        return render(request, "profile.html", data)
    return redirect("signin")
def upsoluong(request, id):
    if request.user.is_authenticated:
        try:
            item = Item.objects.get(id = id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Bún không bún")
        item.soluong = min(min(item.soluong + 1, item.product.soluong), 20)
        item.save()
        return redirect('profile')
    raise Http404("Bún không bún")
def downsoluong(request, id):
    if request.user.is_authenticated:
        try:
            item = Item.objects.get(id = id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Bún không bún")
        item.soluong = max(item.soluong - 1, 1)
        item.save()
        return redirect('profile')
    raise Http404("Bún không bún")
def xoadonhang(request, id):
    if request.user.is_authenticated:
        try:
            k = DonHang.objects.get(id = id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Bún không bún")
        k.item.all().delete()
        k.delete()
        return redirect('profile')
    raise Http404("Bún không bún")
def xoa_item(request, id, don):
    if request.user.is_authenticated:
        try:
            item = Item.objects.get(id = id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Bún không bún")
        item.delete()
        k = DonHang.objects.get(id = don)
        if (not len(k.item.all())):
            k.delete()
        return redirect('profile')
    return redirect("signin")
def buyhome(request, id):
    if request.user.is_authenticated:
        try:
            order = DonHang.objects.get(id = id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise Http404("Bún không bún")
        khachhang = request.user
        info = User.objects.get(id = khachhang.id)
        if request.method == 'POST':
            order.ten = khachhang
            order.tenkhach = request.POST['name'][:300]
            order.sdt = request.POST['phone'][:300]
            order.email = request.POST['email'][:300]
            order.diachi = request.POST['address'][:300]
            order.ghichu = request.POST['note'][:1000]
            order.ngaydathang = now()
            order.trangthai = True
            order.save()
            for k in order.item.all():
                k.trangthai = True
                k.product.soluong -= k.soluong
                for i in DonHang.objects.filter(trangthai = False):
                    j = i.item.get(product__id = k.product.id)
                    j.soluong -= k.soluong
                    if (j.soluong <= 0): j.delete()
                    if (not len(i.item.all())): i.delete()
                    j.save()
                k.product.save()
                k.save()
            return redirect("profile")
        data={'order': order,'info':info,}
        return render(request, "buy.html", data)
    raise Http404("Bún không bún")
#https://www.youtube.com/watch?v=A5nUJ3SVfhs
#https://www.youtube.com/watch?v=PKWCFPTMWVw&t=198s