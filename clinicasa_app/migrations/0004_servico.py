# Generated by Django 5.1.4 on 2024-12-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicasa_app', '0003_prestador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cnpj', models.CharField(max_length=14)),
                ('nome_servico', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'servico',
                'managed': False,
            },
        ),
    ]
