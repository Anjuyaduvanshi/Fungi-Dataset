import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from skimage.util import random_noise
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import warnings




class Fungi:
    def adjust_color(self, base_color, hue_shift=0, saturation_scale=1, value_scale=1):
        base_color_hsv = rgb_to_hsv(base_color)
        base_color_hsv[0] = (base_color_hsv[0] + hue_shift) % 1.0
        base_color_hsv[1] = np.clip(base_color_hsv[1] * saturation_scale, 0, 1)
        base_color_hsv[2] = np.clip(base_color_hsv[2] * value_scale, 0, 1)
        return hsv_to_rgb(base_color_hsv)

    def check_overlap(self, new_bubble, existing_bubbles):
        new_x, new_y, new_width, new_height = new_bubble
        new_radius = max(new_width, new_height) / 2
        for bubble in existing_bubbles:
            x, y, width, height = bubble
            radius = max(width, height) / 2
            distance = np.sqrt((new_x - x)**2 + (new_y - y)**2)
            if distance < (new_radius + radius):
                return True
        return False

    def generate_fungi_bubbles(self, amount=None, irregularity=None, color_dist=None, base_color=None, 
                            noise_level=None, save_path=None, hue_shift=None, saturation_scale=None, value_scale=None,
                            mean_size=None, size_variance=None, background_color=None,
                            background_hue_shift=None, background_saturation_scale=None, background_value_scale=None,
                            background_intensity=None):
        fig, ax = plt.subplots(figsize=(6, 6))

        # Adjust the background color
        adjusted_background_color = self.adjust_color(background_color, background_hue_shift, background_saturation_scale, background_value_scale * background_intensity)
        fig.set_facecolor(adjusted_background_color)
        ax.set_aspect('equal')
        #plt.margins(x=0, y=0, tight=True)
        
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.axis('off')

        
        num_bubbles = int(20 + amount * 80)
        existing_bubbles = []

        for _ in range(num_bubbles):
            size = np.random.normal(mean_size, size_variance)
            width = size * (1 - irregularity + np.random.rand() * irregularity)
            height = size * (1 - irregularity + np.random.rand() * irregularity)

            while True:
                x, y = np.random.uniform(-1, 1, 2)
                new_bubble = (x, y, width, height)
                if not self.check_overlap(new_bubble, existing_bubbles):
                    existing_bubbles.append(new_bubble)
                    break

            num_vertices = 100
            angles = np.linspace(0, 2 * np.pi, num_vertices)
            radii = np.random.normal(1, irregularity, num_vertices)
            vertices = np.column_stack([radii * np.cos(angles), radii * np.sin(angles)])
            vertices[:, 0] *= width
            vertices[:, 1] *= height
            
            angle = np.random.rand() * 360
            theta = np.radians(angle)
            c, s = np.cos(theta), np.sin(theta)
            rotation_matrix = np.array([[c, -s], [s, c]])
            vertices = vertices.dot(rotation_matrix)
            
            vertices += np.array([x, y])
            
            bubble_color = self.adjust_color(np.clip(np.array(base_color) + (np.random.rand(3) - 0.5) * color_dist, 0, 1), 
                                        hue_shift, saturation_scale, value_scale)
            
            path = Path(vertices)
            bubble = PathPatch(path, facecolor=bubble_color, alpha=1.0)  # Set alpha to 1.0 for opaque bubbles
            ax.add_patch(bubble)

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        
        noisy_image = random_noise(image, mode='gaussian', var=noise_level**2)
        noisy_image = np.clip(noisy_image[..., :3], 0, 1)
        

        if save_path:
            plt.imsave(save_path, noisy_image, dpi=1200)
            #print(f"Image saved to {save_path}")
            plt.close()
        else:
            try:
                plt.imshow(noisy_image)
                plt.axis('off')
                #plt.show()
            except UserWarning as e:
                warnings.warn(str(e))
                temp_save_path = 'temp_fungi_bubbles.png'
                plt.imsave(temp_save_path, noisy_image, dpi=1200)
                #fig.savefig('whatever.png', facecolor=fig.get_facecolor(), edgecolor='none')
                print(f"Image saved to {temp_save_path} because interactive display is not available.")
    
