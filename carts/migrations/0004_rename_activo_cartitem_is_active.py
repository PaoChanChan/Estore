# Generated by Django 5.0.4 on 2024-05-28 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_usuario_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='activo',
            new_name='is_active',
        ),
    ]
