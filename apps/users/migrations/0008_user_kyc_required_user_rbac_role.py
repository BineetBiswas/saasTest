# Generated by Django 4.0.5 on 2022-07-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_activation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kyc_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='rbac_role',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]