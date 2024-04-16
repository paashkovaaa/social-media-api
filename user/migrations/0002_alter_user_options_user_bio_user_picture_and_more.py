# Generated by Django 5.0.4 on 2024-04-09 08:39

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ("email",)},
        ),
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(max_length=150, null=True, verbose_name="bio"),
        ),
        migrations.AddField(
            model_name="user",
            name="picture",
            field=models.ImageField(
                null=True,
                upload_to=user.models.profile_image_file_path,
                verbose_name="picture",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True, max_length=50, unique=True, verbose_name="username"
            ),
        ),
    ]
