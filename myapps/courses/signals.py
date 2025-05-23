# signals.py
from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from.models import Node, NodeClosure

@receiver(post_save, sender=Node)
def handle_closure_update(sender, instance, created, **kwargs):
    if created:
        NodeClosure.rebuild_for_node(instance)
    elif getattr(instance, '_parent_changed', False):
      
        NodeClosure.rebuild_branch(instance)
    
@receiver(pre_save, sender=Node)
def track_parent_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
        instance._parent_changed = (old.parent_id != instance.parent_id)
        instance._old_parent = old.parent
    except sender.DoesNotExist:
        pass

@receiver(post_delete, sender=Node)
def delete_closure_relations(sender, instance, **kwargs):
    NodeClosure.objects.filter(descendant=instance).delete()
