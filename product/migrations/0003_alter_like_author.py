# Generated by Django 4.1.4 on 2022-12-22 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_remove_like_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
