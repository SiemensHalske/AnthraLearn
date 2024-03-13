from PIL import Image
import numpy as np
import cv2


def add_padding(img_path, aspect_ratio):
    # Use Pillow to open the webp file
    pil_image = Image.open(img_path)

    # Convert the PIL image to a NumPy array
    img = np.array(pil_image)

    # Check if the image has an alpha channel and remove it if present
    if img.shape[2] == 4:
        # Convert to RGB
        img = img[:, :, :3]

    # Convert the RGB image to BGR format for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Calculate the new dimensions
    height, width, _ = img.shape
    new_width = int(height * aspect_ratio)

    # Calculate padding to be added to the left and right
    pad_width = (new_width - width) // 2
    # In case the division is not even
    pad_width_extra = (new_width - width) % 2

    # Create padding
    # Take the first column for padding color
    left_pad = np.full((height, pad_width, 3), img[:, :1, :], dtype=np.uint8)
    # Take the last column for padding color
    right_pad = np.full((height, pad_width + pad_width_extra,
                        3), img[:, -1:, :], dtype=np.uint8)

    # Concatenate the image with padding
    padded_img = np.hstack((left_pad, img, right_pad))

    # Convert the OpenCV BGR image back to RGB
    padded_img = cv2.cvtColor(padded_img, cv2.COLOR_BGR2RGB)

    # Convert the padded image to a PIL image
    pil_image = Image.fromarray(padded_img)

    # Save the padded image as PNG
    new_img_path = img_path.replace('.webp', '_padded.png')
    pil_image.save(new_img_path, 'PNG')

    return new_img_path


if __name__ == '__main__':
    # Image path
    # (needs to be updated with the correct path where the image is stored)
    img_path = 'banner.webp'
    # Desired aspect ratio (width divided by height)
    aspect_ratio = 16.85

    # Call the function to pad the image
    new_img_path = add_padding(img_path, aspect_ratio)

    if img_path != new_img_path:
        print(f'Padded image saved at {new_img_path}')
    else:
        print('No padding needed')

    print(f'{new_img_path}')
