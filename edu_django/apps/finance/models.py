# finance 应用的数据模型
from django.db import models
from django.conf import settings
from courses.models import CourseTerm

# Create your models here.

class Order(models.Model):
    """订单"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('system_free', '系统免费'),
    ]
    
    order_no = models.CharField(max_length=50, unique=True, verbose_name='订单号', help_text='如 ORD20231027001')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='下单用户'
    )
    term = models.ForeignKey(
        CourseTerm,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='关联班期',
        help_text='购买的是具体班期'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实付金额')
    snapshot_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='价格快照',
        help_text='下单时的单价，防止后续改价'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        null=True, 
        blank=True, 
        verbose_name='支付方式'
    )
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='第三方支付流水号')
    
    refund_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name='退款金额'
    )
    refund_reason = models.CharField(max_length=200, null=True, blank=True, verbose_name='退款原因')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    refunded_at = models.DateTimeField(null=True, blank=True, verbose_name='退款时间')
    
    class Meta:
        db_table = 'finance_orders'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_no'], name='idx_order_no'),
            models.Index(fields=['user', 'status'], name='idx_order_user'),
            models.Index(fields=['-created_at'], name='idx_order_created'),
        ]
    
    def __str__(self):
        return f"{self.order_no} - {self.user.nickname or self.user.username}"
