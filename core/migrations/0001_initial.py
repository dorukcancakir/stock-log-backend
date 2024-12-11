# Generated by Django 5.1.4 on 2024-12-11 13:35

import core.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='core_compan_name_f8e523_idx')],
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_categories', to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_tags', to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('min_quantity', models.PositiveSmallIntegerField(default=0)),
                ('image', models.FileField(upload_to=core.models.upload_to)),
                ('unit_of_measurement', models.CharField(choices=[('PIECE', 'Piece'), ('LITRE', 'Litre'), ('KILOGRAM', 'Kilogram'), ('METER', 'Meter')], default='PIECE', max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.company')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.itemcategory')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.itemtag')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='USER', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.company')),
            ],
            options={
                'indexes': [models.Index(fields=['company'], name='core_user_company_1ff1de_idx'), models.Index(fields=['email'], name='core_user_email_38052c_idx'), models.Index(fields=['first_name', 'last_name'], name='core_user_first_n_7ed624_idx'), models.Index(fields=['role'], name='core_user_role_73872d_idx'), models.Index(fields=['is_active'], name='core_user_is_acti_8c954f_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='itemcategory',
            index=models.Index(fields=['company'], name='core_itemca_company_cd5b7f_idx'),
        ),
        migrations.AddIndex(
            model_name='itemcategory',
            index=models.Index(fields=['name'], name='core_itemca_name_eb29ae_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='itemcategory',
            unique_together={('company', 'name')},
        ),
        migrations.AddIndex(
            model_name='itemtag',
            index=models.Index(fields=['company'], name='core_itemta_company_d344fa_idx'),
        ),
        migrations.AddIndex(
            model_name='itemtag',
            index=models.Index(fields=['name'], name='core_itemta_name_db230d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='itemtag',
            unique_together={('company', 'name')},
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['company'], name='core_item_company_3197c8_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['category'], name='core_item_categor_72af40_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['tag'], name='core_item_tag_id_eb9d1a_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name'], name='core_item_name_de2dec_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['quantity'], name='core_item_quantit_6eeceb_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['min_quantity'], name='core_item_min_qua_3bcf0f_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('company', 'category', 'tag', 'name')},
        ),
    ]
