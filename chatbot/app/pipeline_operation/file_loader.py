from pathlib import Path
from pipeline_operation.constants import FileExtension
from langchain_community.document_loaders import PyMuPDFLoader,Docx2txtLoader


class FileLoader:
    def __init__(self,filename,extension):
       self.filename = Path(filename)
       self.extension = extension
       self.methods = {
           FileExtension.PDF_FILE.value: self.load_pdf,
           FileExtension.DOCX_FILE.value:self.load_docs
       }
    
    def load_pdf(self):
        PDFReader=PyMuPDFLoader(file_path=str(self.filename))
        document=PDFReader.load()
        return document
    
    def load_docs(self):
        DOCXReader=Docx2txtLoader(file_path=str(self.filename))
        documnet=DOCXReader.load()
        return documnet
    
    def load_data(self):
       method = self.methods.get(self.extension)
       return method()