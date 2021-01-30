from rest_framework.routers import SimpleRouter

from .views import PostViewSet, UserPostRelationView


router = SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'post_relation', UserPostRelationView)

urlpatterns = []
urlpatterns += router.urls
