from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from .models import ExchangeProposal, Ad, Category, Post
from .serializers import ProposalCreateSerializer, ProposalStatusUpdateSerializer, AdSerializer, CategorySerializer, PostSerializer

from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics, mixins

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated




class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('user', 'category').prefetch_related('tags').order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'condition', 'user__username']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']


    # РАЗЛИЧНЫЕ СЕРИАЛЗАТОРЫ ДЛЯ РАЗНЫХ МЕТОДОВ
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return AdListSerializer
    #     elif self.action == 'retrieve':
    #         return AdDetailSerializer
    #     return AdSerializer

    # переопределяем queryset
    # def get_queryset(self):
    #     user = self.request.user
    #     qs = Ad.objects.select_related('user', 'category').prefetch_related('tags').order_by('-created_at')
    #     if not user.is_staff:
    #         qs = qs.filter(user=user)  # например, обычный пользователь видит только свои объявления
    #     return qs
    

    # разные permissions
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve', 'recent']:
    #         permission_classes = [AllowAny]  # доступно всем
    #     else:
    #         permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    #     return [permission() for permission in permission_classes]


    # для кастомной обработки ошибок
    # def handle_exception(self, exc):
    # # например, логируем исключения или возвращаем кастомный формат ошибки
    #     return super().handle_exception(exc)


    def list(self, request, *args, **kwargs):
        # Логика перед получением списка (например, логирование)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Логика перед получением одного объекта
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Можно добавить предварительную обработку данных перед созданием
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Полное обновление объекта (PUT)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Частичное обновление объекта (PATCH)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Логика перед удалением объекта
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Автоматическая установка пользователя при создании
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['post'])
    def mark_as_sold(self, request, pk=None):
        """
        Кастомный эндпоинт, чтобы отметить объявление как проданное.
        Вызывается POST /ads/{pk}/mark_as_sold/
        """
        ad = self.get_object()
        # Например, добавим поле `sold` и установим его True
        ad.sold = True
        ad.save()
        return Response({'status': 'объявление отмечено как проданное'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Кастомный эндпоинт для списка последних 5 объявлений.
        Вызывается GET /ads/recent/
        """
        recent_ads = self.queryset[:5]
        serializer = self.get_serializer(recent_ads, many=True)
        return Response(serializer.data)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]






class ProposalCreateView(generics.CreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ProposalsToMeListView(generics.ListAPIView):
    serializer_class = ProposalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["ad_sender", "status"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class ProposalsFromMeListView(generics.ListAPIView):
    serializer_class = ProposalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user)

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["ad_receiver", "status"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class ProposalStatusUpdateView(generics.UpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        obj = super().get_object()
        if obj.ad_receiver.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Вы не можете изменить статус этого предложения.")
        return obj
    






class AdListCreateView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получить список объявлений
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Создать новое объявление
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Автоматически связать объявление с текущим пользователем
        serializer.save(user=self.request.user)


class AdDetailView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получить объявление по ID
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Полное обновление объявления
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Частичное обновление объявления
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Удаление объявления
        return self.destroy(request, *args, **kwargs)
    










class AdListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ads = Ad.objects.all()
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # связываем с юзером
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    def put(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)








class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)