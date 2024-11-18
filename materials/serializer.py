from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "count_lesson", "lessons"]
