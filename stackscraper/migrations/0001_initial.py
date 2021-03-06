# Generated by Django 3.2.4 on 2021-06-30 18:40

from django.db import migrations, models
import djongo.models.fields
import stackscraper.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack', djongo.models.fields.EmbeddedField(model_container=stackscraper.models.TechStack)),
                ('company', djongo.models.fields.EmbeddedField(model_container=stackscraper.models.Company)),
                ('headline', models.CharField(max_length=255)),
            ],
        ),
    ]
