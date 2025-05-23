from django.core.management.base import BaseCommand
from ...models import Node, NodeClosure

class Command(BaseCommand):
    help = 'Populate the closure table for existing nodes'

    def handle(self, *args, **kwargs):
        # 获取所有节点
        nodes = Node.objects.all()

        for node in nodes:
            # 添加自身关系
            NodeClosure.objects.get_or_create(
                ancestor=node,
                descendant=node,
                depth=0
            )

            # 如果有父节点，添加闭包关系
            if node.parent:
                ancestors = NodeClosure.objects.filter(descendant=node.parent)
                for ancestor in ancestors:
                    NodeClosure.objects.get_or_create(
                        ancestor=ancestor.ancestor,
                        descendant=node,
                        depth=ancestor.depth + 1
                    )

        self.stdout.write(self.style.SUCCESS('Closure table populated successfully'))