from django.contrib.auth import logout
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import SingerSerializer
from api.serializers import SingerVOSerializer, MusicVOSerializer, MusicSerializer, LoginSerializer, \
    RegisterSerializer, UserSerializer, UserUpdateSerializer, MusicStarVOSerializer
from goods.models import Goods
from music.models import Music
from music_star.models import MusicStar
from singer.models import Singer
from user.models import User


@api_view(['GET', 'POST'])
def singer_list(request):
    if request.method == 'GET':
        singers = Singer.objects.all()
        serializer = SingerSerializer(singers, many=True)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def singer_add(request):
    name = request.data.get('name')
    try:
        # 尝试获取歌手，如果存在则抛出异常
        singer = Singer.objects.get(name=name)
        return Response({"code": 40000, "data": "", "message": "歌手已存在"})
    except Singer.DoesNotExist:
        # 如果歌手不存在，则继续添加逻辑
        description = request.data.get('description')
        imgUrl = request.data.get('imgUrl')
        newSinger = Singer(name=name, description=description, imgUrl=imgUrl, songCount=0)
        newSinger.save()
        return Response({"code": 0, "data": True, "message": "添加成功"})


@api_view(['GET'])
def singer_detail(request, id):
    try:
        singer = Singer.objects.get(id=id)
    except Goods.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    if request.method == 'GET':
        serializer = SingerVOSerializer(singer)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def singer_delete(request, id):
    try:
        singer = Singer.objects.get(id=id)
    except Singer.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    singer.delete()
    singers = Singer.objects.all()
    serializer = SingerVOSerializer(singers, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def singer_update(request, id):
    try:
        singer = Singer.objects.get(id=id)
    except Singer.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    serializer = SingerSerializer(singer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['GET'])
def singer_id_list(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 40000, "data": "", "message": "无权限"})
    singers = Singer.objects.all()
    ids = [singer.id for singer in singers]
    return Response({"code": 0, "data": ids, "message": ""})


@api_view(['GET', 'POST'])
def music_list(request):
    if request.method == 'GET':
        if request.GET.get('searchText') is None:
            musics = Music.objects.all()
            serializer = MusicVOSerializer(musics, many=True)
            return Response({"code": 0, "data": serializer.data, "message": ""})
        else:
            searchText = request.GET.get('searchText')
            musics = Music.objects.filter(
                Q(name__icontains=searchText) | Q(type__icontains=searchText)
            )
            serializer = MusicVOSerializer(musics, many=True)
            return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def music_add(request):
    name = request.data.get('name')
    try:
        # 尝试获取歌手，如果存在则抛出异常
        music = Music.objects.get(name=name)
        return Response({"code": 40000, "data": "", "message": "歌手已存在"})
    except Music.DoesNotExist:
        name = request.data.get('name')
        imgUrl = request.data.get('imgUrl')
        type = request.data.get('type')
        description = request.data.get('description')
        url = request.data.get('url')
        duration = request.data.get('duration')
        singerId = request.data.get('singerId')
        userId = request.session.get('userId')
        if userId is None:
            return Response({"code": 40100, "data": "", "message": "未登录"})
        user = User.objects.get(id=userId)
        if user is None:
            return Response({"code": 40100, "data": "", "message": "未登录"})
        if user.role == 'user':
            return Response({"code": 40000, "data": "", "message": "无权限"})
        music = Music(name=name, imgUrl=imgUrl, type=type, description=description, url=url, duration=duration, heat=0,
                      singerId=singerId, userId=userId)
        music.save()
        return Response({"code": 0, "data": True, "message": ""})


@api_view(['GET'])
def hot_music_list(request):
    musics = Music.objects.filter(heat__gt=0).order_by('-heat')
    musics = musics[:5] if musics.count() > 5 else musics
    serializer = MusicVOSerializer(musics, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['GET', 'PUT', 'DELETE'])
def music_detail(request, id):
    try:
        music = Music.objects.get(id=id)
    except Music.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    if request.method == 'GET':
        serializer = MusicVOSerializer(music)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def music_delete(request, id):
    try:
        music = Music.objects.get(id=id)
    except Music.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    music.delete()
    musics = Music.objects.all()
    serializer = MusicVOSerializer(musics, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def music_update(request, id):
    try:
        music = Music.objects.get(id=id)
    except Music.DoesNotExist:
        return Response({"code": 40000, "data": "", "message": ""})
    serializer = MusicSerializer(music, data=request.data)
    if serializer.is_valid():
        serializer.save()
        musics = Music.objects.all()
        serializer = MusicVOSerializer(musics, many=True)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def music_upload(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    name = request.data.get('name')
    imgUrl = request.data.get('imgUrl')
    type = request.data.get('type')
    description = request.data.get('description')
    url = request.data.get('url')
    duration = request.data.get('duration')
    singerName = request.data.get('singerName')
    singerImgUrl = request.data.get('singerImgUrl')
    singerDesc = request.data.get('singerDesc')
    singer = Singer.objects.filter(name=singerName).first()
    if not singer:
        singer = Singer(name=singerName, imgUrl=singerImgUrl, songCount=0, description=singerDesc)
        singer.save()
    singerId = singer.id
    singer.songCount += 1
    singer.save()
    music = Music(name=name, imgUrl=imgUrl, type=type, description=description, url=url, duration=duration,
                  singerId=singerId, userId=userId)
    music.save()
    return Response({"code": 0, "data": True, "message": ""})


def custom_login(request, user):
    request.session['userId'] = user.id
    request.session['username'] = user.username
    request.session['nickname'] = user.nickname
    request.session['role'] = user.role
    request.session.set_expiry(3600)


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.get(username=username, password=password)
        if user is not None:
            custom_login(request, user)  # 登录用户并创建 session
            serializer = UserSerializer(user)
            return Response({"code": 0, "data": serializer.data, "message": ""})
        else:
            return Response({"code": 40000, "data": "", "message": "用户不存在"})
    return Response({"code": 40000, "data": "", "message": ""})


@api_view(['POST'])
def user_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        checkPassword = serializer.validated_data['checkPassword']
        nickname = serializer.validated_data['nickname']
        if password != checkPassword:
            return Response({'code': 40000, "data": [], "message": ""})
        if User.objects.filter(username=username).exists():
            return Response({'code': 40000, "data": [], "message": "账号已存在"})
        user = User(
            username=username,
            password=password,
            nickname=nickname,
            avatarUrl='https://hejiajun-img-bucket.oss-cn-wuhan-lr.aliyuncs.com/hm/56e55a4c-90d4-49c7-99e0-54a600f7afdd.jpg',
            role='user',
        )
        user.save()
        serializer = UserSerializer(user)
        return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def user_logout(request):
    logout(request)
    request.session.flush()
    return Response({"code": 0, "message": "登出成功"})


@api_view(['GET'])
def user_current(request):
    if request.method == 'GET':
        userId = request.session.get('userId')
        if userId is None:
            return Response({"code": 40100, "data": "", "message": "用户未登录"})
        user = User.objects.get(id=userId)
        return Response({"code": 0, "data": UserSerializer(user).data, "message": ""})


@api_view(['POST'])
def user_update(request):
    if request.method == 'POST':
        user_id = request.data.get('id')
        if user_id is None:
            return Response({"code": 40001, "data": "", "message": "缺少用户 ID"})
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"code": 40400, "data": "", "message": "用户未找到"})
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 0, "data": serializer.data, "message": "更新成功"})
        return Response({"code": 40000, "data": serializer.errors, "message": "更新失败"})


@api_view(['GET'])
def user_list(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def user_delete(request, id):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    if userId == id:
        return Response({"code": 40000, "data": "", "message": "自己不能删除自己"})
    user = User.objects.get(id=id)
    if user is None:
        return Response({"code": 40000, "data": "", "message": "用户不存在"})
    user.delete()
    return Response({"code": 0, "data": True, "message": ""})


@api_view(['POST'])
def user_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    user = User.objects.get(id=userId)
    if user.role == 'user':
        return Response({"code": 0, "data": "", "message": "无权限"})
    username = request.data.get('username')
    users = User.objects.filter(username=username)
    if not users.exists():
        password = request.data.get('password')
        nickname = request.data.get('nickname')
        avatarUrl = request.data.get('avatarUrl')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        user = User(username=username, password=password, nickname=nickname, avatarUrl=avatarUrl, email=email,
                    role='user',
                    phone=phone, address=address)
        user.save()
        return Response({"code": 0, "data": True, "message": ""})

@api_view(['POST'])
def music_star_add(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    musicId = request.data.get('musicId')
    musicStar = MusicStar(musicId=musicId, userId=userId)
    musicStar.save()
    musics = Music.objects.filter(id=musicId)
    music = musics.first()
    music.heat += 1
    music.save()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['GET'])
def music_star_list(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    musicStars = MusicStar.objects.filter(userId=userId)
    serializer = MusicStarVOSerializer(musicStars, many=True)
    return Response({"code": 0, "data": serializer.data, "message": ""})


@api_view(['POST'])
def music_star_delete(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    musicId = request.data.get('musicId')
    musicStar = MusicStar.objects.filter(musicId=musicId)
    musicStar.delete()
    return Response({"code": 0, "data": True, "message": ""})

@api_view(['GET'])
def music_starred(request):
    userId = request.session.get('userId')
    if userId is None:
        return Response({"code": 40100, "data": "", "message": "未登录"})
    musicId = request.GET.get('musicId')
    musicStars = MusicStar.objects.filter(musicId=musicId, userId=userId)
    if musicStars.exists():
        return Response({"code": 0, "data": True, "message": ""})
    return Response({"code": 0, "data": False, "message": ""})

