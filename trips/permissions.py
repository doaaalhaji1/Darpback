from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    صلاحية تسمح بالقراءة (GET) لجميع المستخدمين، 
    بينما تحصر عمليات الإضافة والتعديل والحذف (POST, PUT, DELETE) للأدمن فقط (is_staff).
    """
    def has_permission(self, request, view):
        # طلبات القراءة الآمنة مسموحة للجميع
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        
        # أي طلب آخر يتطلب أن يكون المستخدم مسجّل دخول و is_staff = True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)