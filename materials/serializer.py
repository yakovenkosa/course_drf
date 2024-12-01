from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import ValidatorLinkToTheVideo


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidatorLinkToTheVideo(field="link_to_video")]


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_count_lesson(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "count_lesson", "lessons"]
