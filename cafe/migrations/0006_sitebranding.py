from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_category_item_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBranding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(default='JJCafe', max_length=100)),
                ('logo', models.ImageField(upload_to='branding/')),
                ('background', models.ImageField(blank=True, null=True, upload_to='branding/')),
                ('primary_color', models.CharField(default='#c8883a', help_text='Hex color e.g. #c8883a', max_length=7)),
                ('secondary_color', models.CharField(default='#2b1a0e', help_text='Hex color e.g. #2b1a0e', max_length=7)),
                ('tagline', models.CharField(blank=True, default='Brew • Bite • Bliss', max_length=200)),
            ],
            options={
                'verbose_name': 'Site Branding',
                'verbose_name_plural': 'Site Branding',
            },
        ),
    ]
