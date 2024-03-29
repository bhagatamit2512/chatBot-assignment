from rest_framework import serializers

class EmbeddingSerializers(serializers.Serializer):
    pipeline_id = serializers.CharField(required=True)
 