from django import forms


class FileValidationMixin:
    """Mixin to provide common file validation for forms with file uploads."""
    
    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images