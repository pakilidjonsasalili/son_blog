# Generated by Django 2.2 on 2021-10-25 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comentario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={'verbose_name': 'Comentario', 'verbose_name_plural': 'Comentarios'},
        ),
    ]