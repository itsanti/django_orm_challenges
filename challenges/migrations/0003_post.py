# Generated by Django 4.1 on 2023-12-07 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_laptop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('text', models.CharField(max_length=2000)),
                ('author', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('PUB', 'опубликован'), ('DRAFT', 'не опубликован'), ('BANNED', 'забанен')], max_length=10)),
                ('category', models.CharField(choices=[('BOOKS', 'Книги'), ('GAMES', 'Игры'), ('MUSIC', 'Музыка')], max_length=20)),
                ('published_at', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
