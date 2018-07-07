# Generated by Django 2.0.7 on 2018-07-07 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='survey.SurveyAnswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='survey.SurveyQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.SurveyQuestion'),
        ),
    ]