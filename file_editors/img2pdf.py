from PIL import Image
import os

def images_to_pdf(image_paths, output_pdf_path):
    images = []

    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"Saved PDF to {output_pdf_path}")
    else:
        print("No images found to convert.")


img_path=["/var/home/noor/CN_Assignment_#5_U2210158.png"]
output="/var/home/noor/D/University_projects/computerNetwork/CN_Assignment_#5_U2210158.pdf"
# Example usage
images_to_pdf(img_path, output)
