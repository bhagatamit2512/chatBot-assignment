from rest_framework import serializers

class InferenceSerializers(serializers.Serializer):
    pipeline_id = serializers.CharField(required=True)
    session_id=serializers.CharField(required=True)
    question = serializers.CharField(required=True)