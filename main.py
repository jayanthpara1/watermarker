import os
from PIL import Image

def add_logos_to_image(image_path, logo_path_left, logo_path_right, output_folder, padding_top=20, padding_right=20, padding_left=20, max_logo_width=200, max_logo_height=200, image_counter=1):
    # Open the original image
    image = Image.open(image_path)
    
    # Open the logos
    logo_left = Image.open(logo_path_left)
    logo_right = Image.open(logo_path_right)

    # Get the current width and height of the logos
    logo_left_width, logo_left_height = logo_left.size
    logo_right_width, logo_right_height = logo_right.size

    # Detect if the image is landscape or portrait
    image_width, image_height = image.size
    is_landscape = image_width > image_height

    # Calculate the aspect ratio of the logos
    logo_left_ratio = logo_left_width / logo_left_height
    logo_right_ratio = logo_right_width / logo_right_height

    # Resize the logos to fit within the max width and height while preserving aspect ratio
    if is_landscape:
        max_width = max_logo_width
        max_height = max_logo_height
    else:
        max_width = int(max_logo_width * 0.8)
        max_height = int(max_logo_height * 0.8)

    # Resize logos while maintaining aspect ratio
    new_left_width = min(max_width, logo_left_width)
    new_left_height = int(new_left_width / logo_left_ratio)
    logo_left = logo_left.resize((new_left_width, new_left_height), Image.Resampling.LANCZOS)

    new_right_width = min(max_width, logo_right_width)
    new_right_height = int(new_right_width / logo_right_ratio)
    logo_right = logo_right.resize((new_right_width, new_right_height), Image.Resampling.LANCZOS)

    # Calculate position for the logos
    position_left = (padding_left, padding_top)
    position_right = (image_width - new_right_width - padding_right, padding_top)

    # Paste the logos onto the image
    image.paste(logo_left, position_left, logo_left.convert("RGBA"))
    image.paste(logo_right, position_right, logo_right.convert("RGBA"))

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate new filename
    new_filename = f"stratum24_{image_counter:03d}{os.path.splitext(image_path)[1]}"
    output_path = os.path.join(output_folder, new_filename)
    
    # Save the resulting image
    image.save(output_path)

    print(f"Logos added and saved to: {output_path}")


def process_images(input_folder, logo_path_left, logo_path_right, output_folder, padding_top=20, padding_right=20, padding_left=20, max_logo_width=200, max_logo_height=200):
    image_counter = 1
    
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(input_folder, file_name)
            add_logos_to_image(image_path, logo_path_left, logo_path_right, output_folder, padding_top, padding_right, padding_left, max_logo_width, max_logo_height, image_counter)
            image_counter += 1


if __name__ == "__main__":
    # Paths (use relative paths here, or get them via arguments/config)
    input_folder = "Gallery"  # Replace with relative or argument-based path
    logo_path_left = "logo.png"  # Replace with relative or argument-based path
    logo_path_right = "ADSC 2 no bg.png"  # Replace with relative or argument-based path
    output_folder = "logoed"  # Output folder for processed images

    # Process the images in the input folder
    process_images(input_folder, logo_path_left, logo_path_right, output_folder)
