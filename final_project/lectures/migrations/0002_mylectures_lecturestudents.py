# Generated by Django 4.0.4 on 2024-03-07 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('lectures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyLectures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('lec_id', models.ForeignKey(db_column='lec_id', on_delete=django.db.models.deletion.RESTRICT, to='lectures.lecture')),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'db_table': 'MyLectures',
            },
        ),
        migrations.CreateModel(
            name='LectureStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canceled', models.BooleanField(default=False)),
                ('lec_id', models.ForeignKey(db_column='lec_id', on_delete=django.db.models.deletion.RESTRICT, to='lectures.lecture')),
                ('student_id', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'db_table': 'LectureStudents',
            },
        ),
    ]
