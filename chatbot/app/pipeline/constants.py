
class File_parameters():
    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS=['pdf', 'docx']
    
class Expected_errors():
    FILE_EXTENSION_ERROR="Unsupported file format. Only .pdf, .docx, are allowed."
    FILE_SIZE_ERROR="File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB."
