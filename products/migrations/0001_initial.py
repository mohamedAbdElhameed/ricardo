# Generated by Django 2.1.3 on 2018-12-18 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(help_text='Quantity', verbose_name='Quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('buyer', models.ForeignKey(help_text='Buyer', on_delete=django.db.models.deletion.CASCADE, to='userprofile.Buyer', verbose_name='Buyer')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=35, verbose_name='Name')),
                ('description', models.TextField(help_text='Description', verbose_name='Description')),
                ('image', models.ImageField(help_text='Image', upload_to='', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default='False', help_text='Paid', verbose_name='Paid')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('rated', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(help_text='Buyer', on_delete=django.db.models.deletion.CASCADE, to='userprofile.Buyer', verbose_name='Buyer')),
                ('seller', models.ForeignKey(default=2, help_text='Seller', on_delete=django.db.models.deletion.CASCADE, to='userprofile.Seller', verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(help_text='quantity', verbose_name='quantity')),
                ('order', models.ForeignKey(help_text='Order', on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.Order', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=50, verbose_name='Name')),
                ('description', models.TextField(help_text='Description', verbose_name='Description')),
                ('price', models.FloatField(help_text='Price', verbose_name='Price')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('active', models.BooleanField(default=False, help_text='active', verbose_name='active')),
                ('seller', models.ForeignKey(help_text='Seller', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_products', to='userprofile.Seller', verbose_name='Seller')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductAdditionalAttributeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=50, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
            ],
            options={
                'verbose_name': 'Product Additional Attribute Name',
                'verbose_name_plural': 'Product Additional Attribute Names',
            },
        ),
        migrations.CreateModel(
            name='ProductAdditionalAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_attribute_value', models.CharField(help_text='Additional Attributes Values', max_length=120, verbose_name='Additional Attributes Values')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('product', models.ForeignKey(help_text='Product', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='additional_attributes', to='products.Product', verbose_name='Product')),
                ('product_additional_attribute', models.ForeignKey(help_text='Product Additional Attributes', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_additional_attributes', to='products.ProductAdditionalAttributeName', verbose_name='Product Additional Attributes')),
            ],
            options={
                'verbose_name': 'Product Additional Attribute Value',
                'verbose_name_plural': 'Product Additional Attribute Values',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Image', upload_to='', verbose_name='Image')),
                ('order', models.IntegerField(help_text='Order', verbose_name='Order')),
                ('alt_text', models.CharField(help_text='Alt Text', max_length=100, verbose_name='Alt Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('product', models.ForeignKey(help_text='Product', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(help_text='Status name', max_length=50, verbose_name='Status name')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=50, verbose_name='Name')),
                ('image', models.ImageField(help_text='Image', upload_to='', verbose_name='Image')),
                ('description', models.TextField(help_text='Description', verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created At', verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Modified At', verbose_name='Modified At')),
                ('category', models.ForeignKey(help_text='Category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='products.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Sub Category',
                'verbose_name_plural': 'Sub Categories',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(help_text='Sub Category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategory_products', to='products.SubCategory', verbose_name='Sub Category'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(help_text='Product', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=None, help_text='you can change the status form the states list', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(help_text='Product', on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Product'),
        ),
        migrations.CreateModel(
            name='OrderProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Order Status',
                'proxy': True,
                'verbose_name_plural': 'Orders Status',
                'indexes': [],
            },
            bases=('products.order',),
        ),
    ]
