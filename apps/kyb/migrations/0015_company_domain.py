# Generated by Django 4.0.5 on 2022-07-06 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyb', '0014_remove_invitetobuyer_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='domain',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
