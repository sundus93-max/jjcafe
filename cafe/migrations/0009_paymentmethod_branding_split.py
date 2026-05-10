from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0008_customerprofile_order_orderitem_promotion'),
    ]

    operations = [
        # Update SiteBranding - add website/admin split fields
        migrations.AddField('SiteBranding', 'website_logo',       models.ImageField(upload_to='branding/', null=True, blank=True, verbose_name='Website Logo')),
        migrations.AddField('SiteBranding', 'website_background', models.ImageField(upload_to='branding/', null=True, blank=True, verbose_name='Website Background')),
        migrations.AddField('SiteBranding', 'admin_logo',         models.ImageField(upload_to='branding/admin/', null=True, blank=True, verbose_name='Admin Portal Logo')),
        migrations.AddField('SiteBranding', 'admin_background',   models.ImageField(upload_to='branding/admin/', null=True, blank=True, verbose_name='Admin Portal Background')),

        # Add show_on to Promotion
        migrations.AddField('Promotion', 'show_on', models.CharField(max_length=10, choices=[('both','Website & App'),('website','Website Only'),('app','App Only')], default='both')),

        # Add notes and updated_at to Order
        migrations.AddField('Order', 'notes',      models.TextField(blank=True)),
        migrations.AddField('Order', 'updated_at', models.DateTimeField(auto_now=True, null=True)),
        migrations.AddField('Order', 'payment_method', models.CharField(max_length=30, blank=True)),

        # Create PaymentMethod
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('method_type', models.CharField(max_length=30, unique=True, choices=[
                    ('card','Credit / Debit Card'),('cash_on_pickup','Cash on Pickup'),
                    ('cash_on_delivery','Cash on Delivery'),('apple_pay','Apple Pay'),('google_pay','Google Pay'),
                ])),
                ('is_enabled', models.BooleanField(default=True)),
                ('icon', models.CharField(max_length=10, default='💳')),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'verbose_name':'Payment Method','verbose_name_plural':'Payment Methods','ordering':['order','name']},
        ),
    ]
