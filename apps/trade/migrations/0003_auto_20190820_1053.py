# Generated by Django 2.2.4 on 2019-08-20 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190812_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'verbose_name': '订单信息', 'verbose_name_plural': '订单信息'},
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='nonce_str',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='随机加密串'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='pay_type',
            field=models.CharField(choices=[('alipay', '支付宝'), ('wechat', '微信')], default='alipay', max_length=10, verbose_name='支付类型'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_sn',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='订单编号'),
        ),
    ]
