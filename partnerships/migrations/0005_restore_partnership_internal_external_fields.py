# Generated migration to restore fields for partnership, internal and external forms

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partnerships', '0004_remove_exterfep_benef_remove_exterfep_categid_and_more'),
    ]

    operations = [
        # Add back fields to PartnerAgencies model
        migrations.AddField(
            model_name='partneragencies',
            name='headagen',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='partneragencies',
            name='contdet',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        
        # Add back fields to InterFep model
        migrations.AddField(
            model_name='interfep',
            name='categid',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='interfep',
            name='dateapprec',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interfep',
            name='dateincep',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interfep',
            name='benef',
            field=models.TextField(blank=True, null=True),
        ),
        
        # Add back fields to ExterFep model
        migrations.AddField(
            model_name='exterfep',
            name='categid',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='exterfep',
            name='benef',
            field=models.TextField(blank=True, null=True),
        ),
    ]