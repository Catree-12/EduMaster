from django.urls import path
from . import views

urlpatterns = [
    # ===== 标签管理 =====
    # GET  /api/knowledge/tags/ - 获取标签列表
    # POST /api/knowledge/tags/ - 创建标签
    path('tags/', views.TagManageView.as_view(), name='tags'),
    
    # GET    /api/knowledge/tags/{id}/ - 获取标签详情
    # PUT    /api/knowledge/tags/{id}/ - 更新标签
    # DELETE /api/knowledge/tags/{id}/ - 删除标签
    path('tags/<int:tag_id>/', views.TagDetailView.as_view(), name='tag-detail'),
    
    # POST   /api/knowledge/tags/attach/ - 给对象添加标签
    # DELETE /api/knowledge/tags/detach/ - 移除对象的标签
    # GET    /api/knowledge/tags/object/ - 获取对象的所有标签
    path('tags/attach/', views.ObjectTagManageView.as_view(), name='tag-attach'),
    path('tags/detach/', views.ObjectTagManageView.as_view(), name='tag-detach'),
    path('tags/object/', views.ObjectTagManageView.as_view(), name='tag-object'),
    
    # ===== 知识点管理 =====
    # GET  /api/knowledge/points/ - 获取知识点树状结构
    # POST /api/knowledge/points/ - 创建知识点
    path('points/', views.KnowledgePointManageView.as_view(), name='knowledge-points'),
    
    # GET    /api/knowledge/points/{id}/ - 获取知识点详情
    # PUT    /api/knowledge/points/{id}/ - 更新知识点
    # DELETE /api/knowledge/points/{id}/ - 删除知识点
    path('points/<int:point_id>/', views.KnowledgePointDetailView.as_view(), name='knowledge-point-detail'),
    
    # POST   /api/knowledge/points/attach/ - 给对象关联知识点
    # DELETE /api/knowledge/points/detach/ - 移除对象的知识点关联
    # GET    /api/knowledge/points/object/ - 获取对象关联的所有知识点
    path('points/attach/', views.ObjectKnowledgePointManageView.as_view(), name='point-attach'),
    path('points/detach/', views.ObjectKnowledgePointManageView.as_view(), name='point-detach'),
    path('points/object/', views.ObjectKnowledgePointManageView.as_view(), name='point-object'),
]
