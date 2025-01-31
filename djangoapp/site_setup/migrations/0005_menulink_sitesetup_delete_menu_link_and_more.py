# Generated by Django 5.1 on 2024-08-29 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0004_site_setup'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('url_or_path', models.CharField(max_length=2048)),
                ('new_tab', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Menu Link',
                'verbose_name_plural': 'Menu Links',
            },
        ),
        migrations.CreateModel(
            name='SiteSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65)),
                ('description', models.CharField(max_length=255)),
                ('show_header', models.BooleanField(default=True)),
                ('show_search', models.BooleanField(default=True)),
                ('show_menu', models.BooleanField(default=True)),
                ('show_description', models.BooleanField(default=True)),
                ('show_pagination', models.BooleanField(default=True)),
                ('show_footer', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Site Setup',
                'verbose_name_plural': 'Site Setup',
            },
        ),
        migrations.DeleteModel(
            name='Menu_link',
        ),
        migrations.DeleteModel(
            name='Site_setup',
        ),
    ]
