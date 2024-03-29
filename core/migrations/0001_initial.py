# Generated by Django 4.1 on 2023-02-10 08:29

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('addres', models.CharField(blank=True, max_length=255, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('email_code', models.PositiveIntegerField(null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category name')),
                ('name_en', models.CharField(max_length=255, null=True, unique=True, verbose_name='Category name')),
                ('name_ru', models.CharField(max_length=255, null=True, unique=True, verbose_name='Category name')),
                ('name_uz', models.CharField(max_length=255, null=True, unique=True, verbose_name='Category name')),
                ('description', models.TextField(verbose_name='Category description')),
                ('description_en', models.TextField(null=True, verbose_name='Category description')),
                ('description_ru', models.TextField(null=True, verbose_name='Category description')),
                ('description_uz', models.TextField(null=True, verbose_name='Category description')),
                ('status', models.CharField(choices=[('0', 'Stack-out'), ('1', 'Stack-in')], default='0', max_length=10, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('transaction', models.CharField(max_length=255)),
                ('customer', models.CharField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total price')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'db_table': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Product name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Product name')),
                ('name_ru', models.CharField(max_length=255, null=True, verbose_name='Product name')),
                ('name_uz', models.CharField(max_length=255, null=True, verbose_name='Product name')),
                ('code', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(verbose_name='Product description')),
                ('description_en', models.TextField(null=True, verbose_name='Product description')),
                ('description_ru', models.TextField(null=True, verbose_name='Product description')),
                ('description_uz', models.TextField(null=True, verbose_name='Product description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[core.models.min_value_validator], verbose_name='Product price')),
                ('status', models.CharField(choices=[('0', 'InActive'), ('1', 'Active')], default='0', max_length=10, verbose_name='Product status')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Category', to='core.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'Products',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='profiles')),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveBigIntegerField(default=0, validators=[core.models.min_value_validator], verbose_name='Product quantity')),
                ('type', models.CharField(choices=[('0', 'Stock-out'), ('1', 'Stock-in')], default='0', max_length=10)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stock',
                'db_table': 'Stock',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.CharField(max_length=255, verbose_name='User')),
                ('quantity', models.PositiveBigIntegerField(verbose_name='Quantity')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='core.stock')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
                'db_table': 'Sales',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[core.models.min_value_validator])),
                ('quantity', models.PositiveBigIntegerField(default=0, validators=[core.models.min_value_validator])),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invoice', to='core.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='core.product')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stock', to='core.stock')),
            ],
            options={
                'verbose_name': 'InvoiceItem',
                'verbose_name_plural': 'InvoiceItmes',
                'db_table': 'InvoiceItems',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveBigIntegerField(verbose_name='quantity')),
                ('type', models.CharField(choices=[('1', 'stock-in'), ('0', 'stock-out')], max_length=12, verbose_name='type')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.stock')),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'Histories',
                'db_table': 'History',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Customuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('addres', models.CharField(blank=True, max_length=255, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('email_code', models.PositiveIntegerField(null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
