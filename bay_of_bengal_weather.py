import os
import urllib.request
import json
import matplotlib.pyplot as plt
import numpy as np
import imageio
from PIL import Image
from datetime import datetime
import matplotlib.image as mpimg

# API URL for Bay of Bengal Weather Data
api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/bay%20of%20bengal?unitGroup=us&include=hours&key=PLVLHWM4STHA6SVPVK5S378MK&contentType=json"

try:
    # Fetch API data
    ResultBytes = urllib.request.urlopen(api_url)
    data = json.loads(ResultBytes.read().decode())
    all_images = []

    # Loop over days in forecast (10 days)
    for day in data['days'][:10]:
        wind_data = day['hours']
        date = day['datetime']
        date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")

        # Prepare a plot for the specified times of the day
        for time_frame in [f"{hour:02}:00:00" for hour in range(24)]:
            for hour in wind_data:
                if hour['datetime'] == time_frame:
                    wind_speed = hour.get('windspeed', 0)  # Wind speed in knots
                    wind_dir = hour.get('winddir', 0)  # Wind direction in degrees

                    # Convert direction to radians (for polar plot)
                    wind_dir_rad = np.deg2rad(wind_dir)

                    # Create the polar plot
                    fig = plt.figure(figsize=(10, 10))
                    ax = fig.add_subplot(111, polar=True)
                    ax.set_theta_direction(-1)  # Counter-clockwise direction
                    ax.set_theta_offset(np.pi / 2)  # North at the top

                    # Plot the wind direction and speed as a bar
                    ax.bar(wind_dir_rad, wind_speed, width=0.2, color='b', alpha=0.5)

                    # Set tick labels for directions
                    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))
                    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

                    # Add title and watermark centered on the plot
                    plt.title(f"Wind Speed(Knots): {date_str} {datetime.strptime(time_frame, '%H:%M:%S').strftime('%I %p')}")
                    
                    # Add "BWOT" watermark at the center
                    plt.text(0.5, 0.5, 'BWOT', fontsize=50, color='gray', alpha=0.3,
                             ha='center', va='center', transform=ax.transAxes)

                    # Add logo in the right corner
                    logo = mpimg.imread('bwot.png')  # Ensure the logo is in the same directory
                    ax_logo = fig.add_axes([0.8, 0.8, 0.1, 0.1], zorder=10)  # Adjust position and size
                    ax_logo.axis('off')  # Hide the axis
                    ax_logo.imshow(logo)

                    # Save each frame as an image
                    image_path = f"frame_{date}_{time_frame.replace(':', '')}.png"
                    plt.savefig(image_path)
                    plt.close(fig)
                    all_images.append(image_path)

 # Create GIF animation using Pillow
    frames = [Image.open(filename) for filename in all_images]
    frames[0].save('BWOT_wind_pattern_animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)

    # Cleanup temporary images
    for filename in all_images:
        os.remove(filename)

    print("Animation created: wind_pattern_animation.gif")

except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode()}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
