from enum import Enum

class FileExtension(Enum):
    PDF_FILE = ".pdf"
    DOCX_FILE = ".docx"

class ChatMessage(Enum):
    CHAT_SAVED = "Message saved successfully!"
    CHAT_FAILED = "Error saving message"
    FAILED_TO_RETRIEVE = "Error retrieving message history"