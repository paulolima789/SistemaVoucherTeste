# Generated by Django 4.2.4 on 2023-10-20 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_voucher', '0006_alter_voucher_especialidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='especialidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_voucher.especialidade'),
        ),
    ]
