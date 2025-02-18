import matplotlib.pyplot as plt
import numpy as np
import json
import random
import os
import shutil
import time

# Color interpolation function remains the same
def interpolate_color(start_color, end_color, position):
    r = start_color[0] + (end_color[0] - start_color[0]) * position
    g = start_color[1] + (end_color[1] - start_color[1]) * position
    b = start_color[2] + (end_color[2] - start_color[2]) * position
    return (r, g, b)

# Temperature interpolation helper function
def calculate_temperature(time):
    # Define temperature ranges based on time
    if 0 <= time < 30:
        return 300 + (time / 30) * 30  # 300K to 330K
    elif 30 <= time < 70:
        return 330 + ((time - 30) / 40) * 20  # 330K to 350K
    elif 70 <= time < 100:
        return 350 + ((time - 70) / 30) * 30  # 350K to 380K
    return None

# Function to generate spore image with mustard yellow to light orange transition
def generate_spore_image(ax, num_spores=10):
    for _ in range(num_spores):
        x_center, y_center = np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)
        color = interpolate_color((1, 0.84, 0), (1, 0.8, 0.5), y_center)  # Mustard yellow to light orange
        spore_circle = plt.Circle((x_center, y_center), 0.02, color=color)
        ax.add_patch(spore_circle)

# Function to generate hyphae image with light orange to light red transition
def generate_hyphae_image(ax, num_hyphae=10, include_spores=False):
    for _ in range(num_hyphae):
        x_center, y_center = np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)
        color = interpolate_color((1, 0.7, 0), (1, 0.4, 0), y_center)  # Light orange to light red
        spore_circle = plt.Circle((x_center, y_center), 0.008, color=color)
        ax.add_patch(spore_circle)
        generate_randomized_branch(ax, x_center, y_center, branch_length=0.06, angle=np.random.uniform(0, 2 * np.pi), depth=3, branch_width=2, color=color, num_initial_branches=4)

    if include_spores:
        for _ in range(random.randint(1, 2)):
            x_center, y_center = np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)
            color = interpolate_color((1, 0.84, 0), (1, 0.8, 0.5), y_center)  # Mustard yellow to light orange
            spore_circle = plt.Circle((x_center, y_center), 0.02, color=color)
            ax.add_patch(spore_circle)

# Function to generate mycelium image (unchanged)
def generate_mycelium_image(ax, num_mycelium=10, include_hyphae=False):
    for _ in range(num_mycelium):
        x_center, y_center = np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)
        color = interpolate_color((1, 0.5, 0), (1, 0, 0), y_center)  # Orange to red
        spore_circle = plt.Circle((x_center, y_center), 0.008, color=color)
        ax.add_patch(spore_circle)
        generate_randomized_branch(ax, x_center, y_center, branch_length=0.2, angle=np.random.uniform(0, 2 * np.pi), depth=10, branch_width=2, color=color, num_initial_branches=14)

    if include_hyphae:
        for _ in range(random.randint(1, 2)):
            x_center, y_center = np.random.uniform(0.2, 0.8), np.random.uniform(0.2, 0.8)
            color = interpolate_color((1, 0.5, 0), (1, 0, 0), y_center)  # Orange to red
            spore_circle = plt.Circle((x_center, y_center), 0.008, color=color)
            ax.add_patch(spore_circle)
            generate_randomized_branch(ax, x_center, y_center, branch_length=0.06, angle=np.random.uniform(0, 2 * np.pi), depth=3, branch_width=2, color=color, num_initial_branches=4)
            
# Recursive branching function
def generate_randomized_branch(ax, x, y, branch_length, angle, depth, branch_width, color, num_initial_branches):
    if depth == 0 or branch_length < 0.005:
        return
    branch_length *= 0.7
    end_x = x + branch_length * np.cos(angle)
    end_y = y + branch_length * np.sin(angle)
    ax.plot([x, end_x], [y, end_y], color=color, alpha=0.8, linewidth=branch_width)

    num_sub_branches = np.random.randint(3, 6)
    new_branch_length = branch_length * (0.4 + np.random.uniform(0, 0.2))
    new_branch_width = branch_width * (0.6 + np.random.uniform(0, 0.4))

    for _ in range(num_sub_branches):
        new_angle = np.random.uniform(0, 2 * np.pi)
        generate_randomized_branch(ax, end_x, end_y, new_branch_length, new_angle, depth - 1, new_branch_width, color=color, num_initial_branches=0)

    if num_initial_branches > 0:
        for _ in range(num_initial_branches):
            new_angle = np.random.uniform(0, 2 * np.pi)
            generate_randomized_branch(ax, x, y, branch_length, new_angle, depth - 1, branch_width, color=color, num_initial_branches=0)

# Function to generate images from JSON file based on class_label
def generate_images_from_custom_json(json_file, output_dir):
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    generated_images = []
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    for time in range(100):  # Iterate from 0 to 99 seconds
        current_time = time
        temperature = calculate_temperature(current_time)  # Get temperature based on time
        if temperature is None:
            continue

        # Generate image based on time
        class_label = None
        if 0 <= current_time < 30:  # Spores
            class_label = "spore"
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            generate_spore_image(ax)
        elif 30 <= current_time < 70:  # Hyphae
            class_label = "hyphae"
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            include_spores = random.choice([True, False])
            generate_hyphae_image(ax, include_spores=include_spores)
        elif 70 <= current_time < 100:  # Mycelium
            class_label = "mycelium"
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)current_time}.png"
        image_path = os.path.join(temp_dir, image_filename)

        try:
            plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close(fig)
            generated_images.append({
                "image_path": image_path,
                "class_label": class_label,
                "description": f"{class_label} generated at {current_time}s",
                "temperature": temperature  # Add temperature
            })
        except Exception as e:
            print(f"Error: Failed to save image {image_path} due to {str(e)}")

    return generated_images

# Function to split and save images into train, val, and test sets
def split_and_save_images(generated_images, base_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    class_data = {"spore": [], "hyphae": [], "mycelium": []}
    for entry in generated_images:
        class_data[entry["class_label"]].append(entry)
    
    for label in class_data:
        random.shuffle(class_data[label])

    splits = {"train": [], "val": [], "test": []}
    for label, images in class_data.items():
        total_images = len(images)
        train_count = int(total_images * train_ratio)
        val_count = int(total_images * val_ratio)
        test_count = total_images - train_count - val_count

        splits["train"].extend(images[:train_count])
        splits["val"].extend(images[train_count:train_count + val_count])
        splits["test"].extend(images[train_count + val_count:])
    
    for split_name, split_data in splits.items():
        split_dir = os.path.join(base_dir, split_name)
        os.makedirs(split_dir, exist_ok=True)
        
        for entry in split_data:
            image_name = os.path.basename(entry["image_path"])
            split_image_path = os.path.join(split_dir, image_name)

            if not os.path.exists(entry["image_path"]):
                print(f"Error: Image {entry['image_path']} not found.")
                continue

            shutil.move(entry["image_path"], split_image_path)
            entry["image_path"] = split_image_path

        json_filepath = os.path.join(base_dir, f'{split_name}_data.json')
        with open(json_filepath, 'w') as json_file:
            json.dump(split_data, json_file, indent=4)

    print("Data split and saved successfully.")

# Run main to generate and split images
def main():
    json_file = '/home/generated_captions_13B.json'
    output_dir = '/home/dataset'
    os.makedirs(output_dir, exist_ok=True)

    generated_images = generate_images_from_custom_json(json_file, output_dir)
    split_and_save_images(generated_images, output_dir)

if __name__ == "__main__":
    main()
