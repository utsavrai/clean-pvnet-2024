from PIL import Image
import os

def resize_image(image_path, output_path, target_size):
    with Image.open(image_path) as img:
        resized_img = img.resize(target_size, Image.LANCZOS)
        resized_img.save(output_path)

def resize_images_in_directory(input_dir, output_dir, target_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.png')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resize_image(input_path, output_path, target_size)
            print(f"Image {filename} resized successfully!")

# Paths to your directories
rgb_dir = '/home/utsav/Downloads/Synapse_dataset/LND_TEST/TEST/image'
mask_dir = '/home/utsav/Downloads/Synapse_dataset/LND_TEST/TEST/mask'

# Output directories for resized images
resized_rgb_dir = '/home/utsav/Downloads/lnd_pvnet_custom_test_resized/rgb'
resized_mask_dir = '/home/utsav/Downloads/lnd_pvnet_custom_test_resized/mask'

# Desired size (width 960, height 544)
new_size = (640, 480)

# Resize the images in both directories
resize_images_in_directory(rgb_dir, resized_rgb_dir, new_size)
resize_images_in_directory(mask_dir, resized_mask_dir, new_size)

print("All images resized successfully!")
