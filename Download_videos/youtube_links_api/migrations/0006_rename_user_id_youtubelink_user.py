# Generated by Django 4.2.5 on 2025-04-06 09:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("youtube_links_api", "0005_youtubelink_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="youtubelink",
            old_name="user_id",
            new_name="user",
        ),
    ]
