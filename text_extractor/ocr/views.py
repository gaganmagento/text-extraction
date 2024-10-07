# ocr/views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from django.core.files.storage import FileSystemStorage
import pytesseract
from PIL import Image
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            fs = FileSystemStorage()
            filename = fs.save(request.FILES['image'].name, request.FILES['image'])
            uploaded_file_url = fs.url(filename)

            # Extract text from image
            # Use the correct path to the uploaded image
            image_path = os.path.join(fs.location, filename)
            text = pytesseract.image_to_string(Image.open(image_path))

            # Clean up the uploaded image
            os.remove(image_path)

            return render(request, 'ocr/result.html', {
                'uploaded_file_url': uploaded_file_url,
                'extracted_text': text
            })
    else:
        form = ImageUploadForm()
    return render(request, 'ocr/upload.html', {'form': form})
