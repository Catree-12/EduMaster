from django.contrib import admin
from .models import Node, section_content, video_content, Lerning_progress, NodeClosure

class SectionContentInline(admin.StackedInline):
    model = section_content
    extra = 1
    fields = ('text_content', 'file_url', 'image_url', 'order')
    verbose_name = '内容'
    verbose_name_plural = '内容'


class ChapterInline(admin.StackedInline):
    model = Node
    extra = 1
    fields = ('title', 'order','description')
    fk_name = 'parent'
    verbose_name = '章'
    verbose_name_plural = '章'
   


class SectionInline(admin.StackedInline):
    model = Node
    extra = 1
    fields = ('title', 'order', 'description')
    fk_name = 'parent'
    verbose_name = '节'
    verbose_name_plural = '节'



class SubsectionInline(admin.StackedInline):
    model = Node
    extra = 1
    fields = ('title', 'order')
    fk_name = 'parent'
    verbose_name = '小节'
    verbose_name_plural = '小节'



@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'node_type', 'parent', 'author__name', 'order')
    list_filter = ('node_type', 'author', 'parent')
    search_fields = ('title', 'description', 'tags')
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段
    fieldsets = (
        (None, {
            'fields': ('node_type', 'parent', 'author', 'title', 'order', 'description', 'tags')
        }),
    )
    ordering = ['order']

    def author__name(self, obj):
        return obj.author.username
    author__name.short_description = '作者'    

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        if obj.node_type == 'course':
            return [ChapterInline(self.model, self.admin_site)]
        elif obj.node_type == 'chapter':
            return [SectionInline(self.model, self.admin_site)]
        elif obj.node_type == 'section':
            return [SubsectionInline(self.model, self.admin_site), SectionContentInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        obj = form.instance
        for instance in instances:
            if not instance.pk:
                parent = form.instance
                instance.author = parent.author
                if obj.node_type == 'course':
                    instance.node_type = 'chapter'
                elif obj.node_type == 'chapter':
                    instance.node_type ='section'
                elif obj.node_type =='section':
                    instance.node_type ='subsection'
            instance.save()     
    

  
# 自定义 section_content 的 Admin 显示
@admin.register(section_content)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = ( 'node', 'text_content', 'file_url', 'image_url')
    list_filter = ('node',)
    search_fields = ('text_content',)
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段
    fieldsets = (
        (None, {
            'fields': ('node', 'text_content', 'file_url', 'image_url', 'order')
        }),
    )
    ordering = ['order']

# 自定义 video_content 的 Admin 显示
@admin.register(video_content)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'video_url', 'total_duration', 'resolution', 'file_size')
    list_filter = ('chapter', 'resolution', 'created_at')
    search_fields = ('chapter__title',)
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段 
    fieldsets = (
        (None, {
            'fields': ('chapter', 'video_url', 'total_duration', 'resolution', 'file_size')
        }),
    )

# 自定义 Lerning_progress 的 Admin 显示
@admin.register(Lerning_progress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'node', 'is_completed', 'last_visited', 'created_at')
    list_filter = ('user', 'is_completed', 'created_at')
    search_fields = ('user__username', 'node__title')
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段
    fieldsets = (
        (None, {
            'fields': ('user', 'node', 'is_completed', 'last_visited')
        }),
    )

# 自定义 NodeClosure 的 Admin 显示
@admin.register(NodeClosure)
class NodeClosureAdmin(admin.ModelAdmin):
    list_display = ('ancestor', 'descendant', 'depth')
    list_filter = ('ancestor', 'descendant', 'depth')
    search_fields = ('ancestor__title', 'descendant__title')
    filter_horizontal = ()  # 如果有需要，可以在这里添加多对多字段
    fieldsets = (
        (None, {
            'fields': ('ancestor', 'descendant', 'depth')
        }),
    )
    