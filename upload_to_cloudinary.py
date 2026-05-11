import cloudinary
import cloudinary.uploader
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'jjcafe.settings.production'
django.setup()

cloudinary.config(
    cloud_name='dbphb4rs1',
    api_key='825771744642443',
    api_secret='Aj6h4pFdZ8sBc7679PFRQcN5EAo'
)

from cafe.models import Item, Category, SiteBranding, Promotion


def find_file(path):
    """Try original path, then with spaces instead of underscores."""
    if os.path.exists(path):
        return path
    # Try replacing underscores with spaces
    alt = path.replace('_', ' ')
    if os.path.exists(alt):
        return alt
    # Search in the folder for a similar filename
    folder = os.path.dirname(path)
    filename = os.path.basename(path)
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if f.lower().replace('_', '').replace(' ', '') == filename.lower().replace('_', '').replace(' ', ''):
                return os.path.join(folder, f)
    return None


print("Uploading Item images...")
for item in Item.objects.all():
    if item.image:
        path = 'media/' + str(item.image)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            item.image = result['public_id']
            item.save()
            print(f"OK: {item.name} -> {result['secure_url']}")
        else:
            print(f"Missing: {path}")

print("\nUploading Category images...")
for cat in Category.objects.all():
    if cat.image:
        path = 'media/' + str(cat.image)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            cat.image = result['public_id']
            cat.save()
            print(f"OK: {cat.name} -> {result['secure_url']}")
        else:
            print(f"Missing: {path}")

print("\nUploading Branding images...")
for b in SiteBranding.objects.all():
    if b.website_logo:
        path = 'media/' + str(b.website_logo)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            b.website_logo = result['public_id']
            b.save()
            print(f"Logo -> {result['secure_url']}")
        else:
            print(f"Missing logo: {path}")

    if b.website_background:
        path = 'media/' + str(b.website_background)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            b.website_background = result['public_id']
            b.save()
            print(f"Background -> {result['secure_url']}")
        else:
            print(f"Missing background: {path}")

    if b.admin_logo:
        path = 'media/' + str(b.admin_logo)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            b.admin_logo = result['public_id']
            b.save()
            print(f"Admin logo -> {result['secure_url']}")

    if b.admin_background:
        path = 'media/' + str(b.admin_background)
        real_path = find_file(path)
        if real_path:
            result = cloudinary.uploader.upload(real_path, overwrite=True)
            b.admin_background = result['public_id']
            b.save()
            print(f"Admin background -> {result['secure_url']}")

print("\nAll done!")
