from django.db import models


class PartTopic(models.Model):
    PART_CHOICES = [
        ('part1', 'Part 1'),
        ('part2', 'Part 2'),
        ('part3', 'Part 3'),
        ('fulltest', 'Full Test'),
    ]

    topic = models.CharField(max_length=155, verbose_name="Topic")
    part_type = models.CharField(
        max_length=10,
        choices=PART_CHOICES,
        verbose_name="Part Type"
    )

    def __str__(self):
        return f"{self.get_part_type_display()}: {self.topic}"


class Part1Question(models.Model):
    part_topic = models.ForeignKey(PartTopic, on_delete=models.CASCADE, related_name="part1_questions")
    question = models.CharField(max_length=255, verbose_name="Question")

    def __str__(self):
        return self.question


class Part2Question(models.Model):
    part_topic = models.ForeignKey(PartTopic, on_delete=models.CASCADE, related_name="part2_questions")
    question = models.CharField(max_length=255, verbose_name="Cue Card Question")
    hint1 = models.CharField(max_length=255, verbose_name="Hint 1", blank=True, null=True)
    hint2 = models.CharField(max_length=255, verbose_name="Hint 2", blank=True, null=True)
    hint3 = models.CharField(max_length=255, verbose_name="Hint 3", blank=True, null=True)

    def __str__(self):
        return self.question


class Part3Question(models.Model):
    part_topic = models.ForeignKey(PartTopic, on_delete=models.CASCADE, related_name="part3_questions")
    question = models.CharField(max_length=255, verbose_name="Discussion Question")
    follow_up_question = models.CharField(max_length=255, verbose_name="Follow-Up Question", blank=True, null=True)

    def __str__(self):
        return self.question
