from django.contrib import admin

from user.models import PartTopic, Part1Question
from .models import (
    User, Book, WritingTask1, Unit, Vocab, Test, Result, CambridgeTest,
    ReadingSection, TFNGQuestion, FillInTheBlanksQuestion, SectionText, BlankAnswer
)


# User Admin Panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'rank', 'role', 'is_staff')
    search_fields = ('email', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser')


# Book Admin Panel
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name', 'level')


# WritingTask1 Admin Panel
@admin.register(WritingTask1)
class WritingTask1Admin(admin.ModelAdmin):
    list_display = ('id', 'type', 'question')
    search_fields = ('type', 'question')
    list_filter = ('type',)


# Unit Admin Panel
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_num', 'unit_name', 'book')
    search_fields = ('unit_name',)
    list_filter = ('book',)


# Vocabulary Admin Panel
@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    list_display = ('en', 'uz', 'unit')
    search_fields = ('en', 'uz')
    list_filter = ('unit',)


# Test Admin Panel
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question', 'book', 'unit', 'vocab', 'type')
    search_fields = ('question',)
    list_filter = ('book', 'unit', 'type')


# Result Admin Panel
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'correct', 'quantity', 'type')
    search_fields = ('user__email', 'type')
    list_filter = ('type',)


# CambridgeTest Admin Panel
@admin.register(CambridgeTest)
class CambridgeTestAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'test_number', 'reading_test_number', 'listening_test_number')
    search_fields = ('book_name',)
    list_filter = ('book_name',)


# SectionText Inline for ReadingSection
class SectionTextInline(admin.TabularInline):
    model = SectionText
    extra = 1  # Number of initial inline fields


# ReadingSection Admin Panel
@admin.register(ReadingSection)
class ReadingSectionAdmin(admin.ModelAdmin):
    list_display = ('cambridge_test', 'reading_passage', 'section_name', 'section_type')
    inlines = [SectionTextInline]
    search_fields = ('section_name',)
    list_filter = ('section_type',)


# TFNGQuestion Admin Panel
@admin.register(TFNGQuestion)
class TFNGQuestionAdmin(admin.ModelAdmin):
    list_display = ('section', 'question_number', 'question_text', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('correct_answer',)


class BlankAnswerInline(admin.TabularInline):
    model = BlankAnswer
    extra = 1  # Boshlang'ich blanklar soni


@admin.register(FillInTheBlanksQuestion)
class FillInTheBlanksQuestionAdmin(admin.ModelAdmin):
    list_display = ('section', 'question_name', 'question_text')
    search_fields = ('question_name', 'question_text')
    inlines = [BlankAnswerInline]


# PartTopic Admin Panel
@admin.register(PartTopic)
class PartTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'part_type')
    search_fields = ('topic',)
    list_filter = ('part_type',)


# Part1Question Admin Panel
@admin.register(Part1Question)
class Part1QuestionAdmin(admin.ModelAdmin):
    list_display = ('part_topic', 'question')
    search_fields = ('question',)
    list_filter = ('part_topic',)
