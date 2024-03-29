"""Write file upload serializers here"""

from rest_framework import serializers
from pipeline.constants import File_parameters,Expected_errors
from pipeline.models import  UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["file"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "file": {"write_only": True},
        }
    
    def validate_file(self,value):
        ext=value.name.lower().split('.')[-1]
        if ext not in File_parameters.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(Expected_errors.FILE_EXTENSION_ERROR)
        
        max_size_bytes = File_parameters.MAX_FILE_SIZE_MB * 1024 * 1024
        if value.size > max_size_bytes:
            raise serializers.ValidationError(Expected_errors.FILE_SIZE_ERROR.value)
        
        return value
   



