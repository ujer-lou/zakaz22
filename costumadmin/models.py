from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import (
    PositiveSmallIntegerField, CharField, EmailField, Model,
    SmallIntegerField, ImageField, ForeignKey, CASCADE,
    TextField, DateTimeField, ManyToManyField, TextChoices
)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Maxsus foydalanuvchi menejeri"""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email manzili kiritilishi shart")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields["is_staff"]:
            raise ValueError("Superuser uchun 'is_staff=True' bo'lishi kerak.")
        if not extra_fields["is_superuser"]:
            raise ValueError("Superuser uchun 'is_superuser=True' bo'lishi kerak.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserRole(TextChoices):
        ADMIN = 'admin', "Admin"
        USER = 'user', "User"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = EmailField("Email manzili", blank=True, unique=True)
    objects = CustomUserManager()
    rank = PositiveSmallIntegerField(default=0)
    role = CharField(max_length=50, choices=UserRole.choices, default=UserRole.USER)
    groups = ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Permissions for this user.',
        verbose_name='user permissions',
    )


class Book(Model):
    name = CharField(max_length=255)
    level = CharField(max_length=255)
    image = ImageField(upload_to='books/')


class WritingTask1(models.Model):
    TYPE_CHOICES = [
        ('bar_chart', 'Bar Chart'),
        ('line_graph', 'Line Graph'),
        ('table', 'Table'),
        ('pie_chart', 'Pie Chart'),
        ('diagram', 'Diagram'),
        ('map', 'Map'),
    ]
    tepy = [
        ('1', '1'),
        ('2', '2')
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Type")
    type1 = models.CharField(max_length=50, choices=tepy, verbose_name="typeee", default='bar_chart')
    question = models.TextField(verbose_name="Question")
    photo = models.ImageField(upload_to='writing_task_photos1/', null=True, blank=True, verbose_name="Photo")


class Unit(models.Model):
    """Unit modeli"""
    unit_num = models.SmallIntegerField(default=1)
    unit_name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='units')

    def __str__(self):
        return f"{self.book.name} - Unit {self.unit_num}: {self.unit_name}"


class Vocab(models.Model):
    """Vocabulary model"""
    en = models.CharField(max_length=255)
    uz = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='vocab/audio/', blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='vocabs')

    def __str__(self):
        return f"{self.en} - {self.uz}"


class TestSection(Model):
    """Test bo‘limi modeli"""
    title = CharField(max_length=255)
    description = TextField()


class TestType(models.TextChoices):
    MATN = 'matn', _('Matn')
    AUDIO = 'audio', _('Audio')
    ARALASH = 'aralash', _('Aralash')


class OptionTest(models.TextChoices):
    A = 'a', 'A'
    B = 'b', 'B'
    C = 'c', 'C'
    D = 'd', 'D'


class Test(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    vocab = models.ForeignKey('Vocab', on_delete=models.SET_NULL, null=True, blank=True)

    type = models.CharField(
        max_length=10,
        choices=TestType.choices,
        default=TestType.MATN
    )

    question = models.CharField(max_length=255)

    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)

    right = models.CharField(
        max_length=1,
        choices=OptionTest.choices
    )

    audio = models.FileField(
        upload_to='audios/',
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question} [{self.get_type_display()}]"


class Result(Model):
    """Natijalar modeli"""

    class ResultType(TextChoices):
        VOCAB = 'vocab', 'Lug‘at'
        TEST = 'test', 'Test'

    user = ForeignKey(User, CASCADE, related_name='results')
    correct = PositiveSmallIntegerField()
    quantity = SmallIntegerField()
    created_at = DateTimeField(auto_now=True)
    type = CharField(max_length=50, choices=ResultType.choices)
    test_section = ManyToManyField(TestSection, related_name='results')
    unit = ManyToManyField(Unit, related_name='results')


class CambridgeTest(models.Model):
    """Cambridge test modeli, har bir test uchun alohida ma'lumotlarni saqlaydi."""
    book_name = models.CharField(max_length=100, help_text="Kitob nomi")
    test_number = models.IntegerField(help_text="Test raqami")
    reading_test_number = models.IntegerField(help_text="Reading test raqami")
    listening_test_number = models.IntegerField(help_text="Listening test raqami")
    listening_available = models.BooleanField(default=True, help_text="Listening test mavjudligi")
    reading_available = models.BooleanField(default=True, help_text="Reading test mavjudligi")

    def __str__(self):
        reading_status = "Available" if self.reading_available else "Not Available"
        listening_status = "Available" if self.listening_available else "Not Available"
        return f"{self.book_name} - Test {self.test_number}: Reading Test {self.reading_test_number} - {reading_status}, Listening Test {self.listening_test_number} - {listening_status}"


class ReadingSection(models.Model):
    """Reading testning har bir bo'limini (passage) saqlaydigan model.
    Har bir passage o'zining nomi, matni va turini o'z ichiga oladi."""
    cambridge_test = models.ForeignKey('CambridgeTest', on_delete=models.CASCADE,
                                       related_name='reading_sections',
                                       help_text="Bu passage tegishli bo'lgan Cambridge testi")
    reading_passage = models.CharField(max_length=255,
                                       help_text="Bu yerda READING PASSAGE NUMBER boladu")
    section_name = models.CharField(max_length=255,
                                    help_text="Passage nomi, masalan 'How tennis rackets have changed'")
    section_text = models.TextField(blank=True, null=True, help_text="Bu yerda passage matni yoziladi (majburiy emas)")

    SECTION_TYPES = [
                        ('A', 'Type A'), ('B', 'Type B'), ('C', 'Type C'), ('D', 'Type D'),
                        ('E', 'Type E'), ('F', 'Type F'), ('G', 'Type G')
                    ] + [(str(i), f'Type {i}') for i in range(1, 16)]

    section_type = models.CharField(max_length=10, choices=SECTION_TYPES,
                                    help_text="Passage turini belgilovchi harf, har bir tur ma'lum bir test formatini ifodalaydi")

    def __str__(self):
        return f"{self.reading_passage} - {self.section_name} - {self.get_section_type_display()}"


class SectionText(models.Model):
    """Har bir ReadingSection uchun turiga qarab matnlarni saqlaydigan model."""
    reading_section = models.ForeignKey(ReadingSection, on_delete=models.CASCADE, related_name='texts')
    text_type = models.CharField(max_length=10, choices=ReadingSection.SECTION_TYPES)
    text = models.TextField()

    def __str__(self):
        return f"{self.text_type} - {self.text[:50]}"  # Textning birinchi 50 belgisini ko'rsatadi


class TFNGQuestion(models.Model):
    """True, False, yoki Not Given turdagi savollar uchun model."""
    section = models.ForeignKey(ReadingSection, on_delete=models.CASCADE, related_name='tfng_questions')
    question_number = models.IntegerField(help_text="Savol raqami")
    question_text = models.TextField(help_text="Savol matni")
    correct_answer = models.CharField(max_length=10, choices=[
        ('True', 'True'),
        ('False', 'False'),
        ('Not Given', 'Not Given')],
                                      help_text="To'g'ri javob")

    def __str__(self):
        return f"Question {self.question_number}: {self.question_text[:50]}... - Correct: {self.correct_answer}"


class FillInTheBlanksQuestion(models.Model):
    """Bo'sh joylarni to'ldirish uchun savollar modeli."""
    section = models.ForeignKey(ReadingSection, on_delete=models.CASCADE, related_name='fill_in_the_blanks_questions')
    question_name = models.CharField(max_length=255, help_text="A descriptive name for the question")
    question_text = models.TextField(
        help_text="Savol matni, masalan: 'Excavations of rock shelters inside {{qnumber}} {{blank}} near the village of Kelo revealed:'")


class BlankAnswer(models.Model):
    question = models.ForeignKey(FillInTheBlanksQuestion, on_delete=models.CASCADE, related_name='answers')
    blank_identifier = models.CharField(max_length=10, help_text="Blank identifikatori, masalan: 'blank1'")
    correct_answer = models.CharField(max_length=255, help_text="To'g'ri javob")

    def __str__(self):
        return f"{self.blank_identifier} - {self.correct_answer}"
