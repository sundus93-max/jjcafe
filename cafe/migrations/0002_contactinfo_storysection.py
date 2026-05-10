from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(help_text='Full street address')),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('opening_hours', models.TextField(blank=True, help_text='e.g. Mon–Fri 8am–6pm')),
                ('google_maps_url', models.URLField(blank=True, help_text="Paste the Google Maps embed src URL here (Maps → Share → Embed → copy the src='...' value)")),
            ],
            options={
                'verbose_name': 'Contact Info',
                'verbose_name_plural': 'Contact Info',
            },
        ),
        migrations.CreateModel(
            name='StorySection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=1, help_text='Display order (1 = first)')),
                ('heading', models.CharField(blank=True, help_text='Optional section heading', max_length=200)),
                ('body', models.TextField(help_text='Main paragraph text')),
                ('image_url', models.URLField(blank=True, help_text='Optional section image URL')),
            ],
            options={
                'verbose_name': 'Our Story Section',
                'verbose_name_plural': 'Our Story Sections',
                'ordering': ['order'],
            },
        ),
    ]
