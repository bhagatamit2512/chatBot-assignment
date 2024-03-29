from django.urls import path
from pipeline_operation.views.views import EmbeddingView, InferenceView
urlpatterns = [
    path(
        "generateEmbedding/",
        EmbeddingView.as_view(),
        name="generate_embeddings",
    ),
    path(
        "chat/",
        InferenceView.as_view(),
        name="chat",
    ),
 ]