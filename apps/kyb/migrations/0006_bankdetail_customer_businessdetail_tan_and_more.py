# Generated by Django 4.0.5 on 2022-06-06 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kyb', '0005_alter_company_is_buyer_alter_company_is_kyb_done_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='kyb.company')),
                ('bank_name', models.CharField(max_length=50, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=200, null=True)),
                ('ifsc_code', models.CharField(max_length=200, null=True)),
                ('account_no', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('company_name', models.CharField(max_length=200, null=True)),
                ('phone_no', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='TAN',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='annual_revenue',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='company_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='industry',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='businessdetail',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Subsription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_name', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kyb.company')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, null=True)),
                ('product_detail', models.CharField(blank=True, max_length=200, null=True)),
                ('pricing', models.CharField(max_length=200, null=True)),
                ('tiers', models.CharField(max_length=200, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kyb.company')),
            ],
        ),
        migrations.CreateModel(
            name='InviteToBuyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kyb.company')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kyb.customer')),
            ],
        ),
    ]
