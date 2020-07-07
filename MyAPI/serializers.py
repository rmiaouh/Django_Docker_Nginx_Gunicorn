from rest_framework import serializers
from .models import Task, OrangeDB, RedDB, YellowDB, PinkDB, BlueDB, GreenDB


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializer_orange(serializers.ModelSerializer):
    class Meta:
        model = OrangeDB
        fields = '__all__'


class TaskSerializer_red(serializers.ModelSerializer):
    class Meta:
        model = RedDB
        fields = '__all__'


class TaskSerializer_yellow(serializers.ModelSerializer):
    class Meta:
        model = YellowDB
        fields = '__all__'


class TaskSerializer_pink(serializers.ModelSerializer):
    class Meta:
        model = PinkDB
        fields = '__all__'


class TaskSerializer_blue(serializers.ModelSerializer):
    class Meta:
        model = BlueDB
        fields = '__all__'


class TaskSerializer_green(serializers.ModelSerializer):
    class Meta:
        model = GreenDB
        fields = '__all__'