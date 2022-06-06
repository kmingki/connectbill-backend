# Generated by Django 4.0.5 on 2022-06-04 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_commission', '0002_initial'),
        ('users', '0001_initial'),
        ('userReview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreview',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client'),
        ),
        migrations.AddField(
            model_name='customerreview',
            name='commission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client_commission.commission'),
        ),
        migrations.AddField(
            model_name='customerreview',
            name='designer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.designer'),
        ),
    ]
