# Generated by Django 4.1.8 on 2023-05-18 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(choices=[('1', '1st grade'), ('2', '2nd grade'), ('3', '3rd grade'), ('4', '4th grade'), ('5', '5th grade'), ('6', '6th grade')], max_length=10)),
                ('designiation', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('phoneNumber', models.BigIntegerField()),
                ('adress', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=10)),
                ('type', models.CharField(max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('attemps', models.IntegerField(default=3)),
                ('payement_method', models.CharField(choices=[('1', 'Monthly'), ('2', 'Yearly'), ('3', 'Freemuim')], default=3, max_length=10)),
                ('payed', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('matricule', models.BigIntegerField()),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('UserApp.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('matricule', models.BigIntegerField()),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('UserApp.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('matricule', models.BigIntegerField()),
                ('father', models.ManyToManyField(to='UserApp.parent')),
                ('grade', models.ManyToManyField(to='UserApp.classes')),
            ],
            options={
                'abstract': False,
            },
            bases=('UserApp.user',),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('questions', models.JSONField()),
                ('types', models.JSONField()),
                ('answer', models.JSONField()),
                ('correctAnswers', models.JSONField()),
                ('note', models.IntegerField(default=0)),
                ('quizDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.student')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=300)),
                ('student', models.ManyToManyField(to='UserApp.student')),
            ],
        ),
        migrations.AddField(
            model_name='classes',
            name='teachers',
            field=models.ManyToManyField(to='UserApp.teacher'),
        ),
    ]