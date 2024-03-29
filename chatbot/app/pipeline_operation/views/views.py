from rest_framework.views import APIView
from rest_framework.response import Response
from pipeline_operation.serializers.embedding_serializers import  EmbeddingSerializers
from pipeline.models import UploadedFile
from pipeline_operation.embedding_config import generate_embeddings, process_file
from pipeline_operation.serializers.inference_serializers import InferenceSerializers
from pipeline_operation.inference_config import chat_service
class EmbeddingView(APIView):
    serializer_class = EmbeddingSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pipeline_id = serializer.validated_data.get('pipeline_id')
            try:
                uploaded_file = UploadedFile.objects.get(id=pipeline_id)
                file_path = uploaded_file.file.path
                document=process_file(pipeline_id,file_path)
                generate_embeddings(document)
                return Response({'message': "embeddings generated successfully"})
            except UploadedFile.DoesNotExist:
                return Response({'error': 'UploadedFile not found'}, status=404)
        else:
            return Response(serializer.errors, status=400)
        
        
class InferenceView(APIView):
    serializer_class = InferenceSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data["question"]
            pipeline_id = serializer.validated_data["pipeline_id"]
            session_id = serializer.validated_data["session_id"]
            data = {
                "question": question,
                "pipeline_id": pipeline_id,
                "session_id": session_id
            }
            try:
                result=chat_service(data)
                print("(((((((((((((((((((((((((((())))))))))))))))))))))))))))",result)
                return Response({'message': result})
            except ValueError:
                return Response({'error': "answer not found"}, status=404)
        else:
            return Response(serializer.errors, status=400)