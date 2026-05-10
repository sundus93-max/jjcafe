from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_alter_contactinfo_google_maps_url'),
    ]

    operations = [
        # 1. Create Category table
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/')),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['order', 'name'],
            },
        ),
        # 2. Add category FK to Item
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='items',
                to='cafe.category',
            ),
        ),
        # 3. Add ordering to Item
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['name'], 'verbose_name': 'Menu Item', 'verbose_name_plural': 'Menu Items'},
        ),
    ]
