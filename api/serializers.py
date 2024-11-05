from rest_framework import serializers

from music.models import Music
from music_star.models import MusicStar
from singer.models import Singer
from user.models import User


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'
        depth = 1


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'
        depth = 1


class MusicVOSerializer(serializers.ModelSerializer):
    singer = serializers.SerializerMethodField()  # 使用 SerializerMethodField 来获取 Singer 信息
    user = serializers.SerializerMethodField()
    class Meta:
        model = Music
        fields = '__all__'

    def get_singer(self, obj):
        try:
            singer = Singer.objects.get(id=obj.singerId)
            return SingerSerializer(singer).data
        except Singer.DoesNotExist:
            return None
    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.userId)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None

class SingerVOSerializer(serializers.ModelSerializer):
    music_list = serializers.SerializerMethodField()  # 用于获取音乐列表

    class Meta:
        model = Singer
        fields = '__all__'  # 包含 Singer 的所有字段

    def get_music_list(self, obj):
        # 查询与当前 Singer 相关的所有 Music 实例
        musics = Music.objects.filter(singerId=obj.id)  # 使用 singerId 过滤
        return MusicSerializer(musics, many=True).data  # 返回音乐的序列化数据

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    checkPassword = serializers.CharField(required=True, max_length=100)
    nickname = serializers.CharField(required=True, max_length=100)


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)  
    avatarUrl = serializers.CharField(required=False, allow_blank=True)  
    address = serializers.CharField(required=False, allow_blank=True)  
    phone = serializers.CharField(required=False, allow_blank=True)  

    class Meta:
        model = User
        fields = '__all__'

class MusicUploadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    imgUrl = serializers.EmailField(required=False, allow_blank=True)  
    type = serializers.CharField(required=False, allow_blank=True)  
    description = serializers.CharField(required=False, allow_blank=True)  
    url = serializers.CharField(required=False, allow_blank=True)  
    duration = serializers.CharField(required=False, allow_blank=True)
    singerName = serializers.CharField(required=False, allow_blank=True)
    singerImgUrl = serializers.CharField(required=False, allow_blank=True)
    songCount = serializers.CharField(required=False, allow_blank=True)
    singerDesc = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Music, Singer
        fields = '__all__'

class MusicStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicStar
        fields = '__all__'
        depth = 1

class MusicStarVOSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = MusicStar
        fields = '__all__'

    def get_music(self, obj):
        try:
            music = Music.objects.filter(id=obj.musicId)
            return MusicVOSerializer(music, many=True).data
        except Music.DoesNotExist:
            return None