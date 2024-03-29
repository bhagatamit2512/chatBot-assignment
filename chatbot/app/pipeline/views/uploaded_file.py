
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from dotenv import load_dotenv
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ParseError
from pipeline.serializers.uploaded_file import UploadedFileSerializer
import uuid
import os

load_dotenv()
class UploadedFileView(APIView):
   
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadedFileSerializer
     
    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('file')
            file_info=[]
            if files :
                for file in files:
                    serializer = self.serializer_class(data={'file': file})
                    serializer.is_valid(raise_exception=True)
                    instance=serializer.save()
                    file_path = instance.file.url.lstrip('/')
                    file_info.append({
                        "pipeline_id":instance.id,
                        'name': os.path.basename(instance.file.name),
                        'path': file_path,
                        'size': instance.file.size 
                    })
                    
                return Response({'file_info': file_info}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except ParseError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
