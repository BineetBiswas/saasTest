# Generated by Django 4.0.5 on 2022-06-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyb', '0009_remove_businessdetail_annual_revenue_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessdetail',
            old_name='company_address',
            new_name='company_registered_address',
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='contact_address_City',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='contact_address_Line1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='contact_address_Line2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='contact_address_PinCode',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='contact_address_State',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='businessdetail',
            name='PAN',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
    ]
