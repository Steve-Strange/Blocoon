# Generated by Django 4.2.3 on 2023-07-14 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_userprofile_graph_roots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='graph_roots',
            field=models.BinaryField(editable=True, verbose_name='GraphsRoot'),
        ),
    ]