from cv2 import cv2
import numpy as np
import pygame


# Define the path to the image to compare against
img_path = 'oneway_up.png'

# Load the image to compare against
img_to_compare = cv2.imread(img_path, cv2.COLOR_BGR2GRAY)
print(type(img_to_compare))

# Set the threshold for comparison
threshold = 0.7

# Take a screenshot of the screen
screenshot_gray = cv2.imread("screen.png", cv2.COLOR_BGR2GRAY)

# Convert the screenshot to grayscale
# screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Use OpenCV's template matching to search for the given image in the screenshot
res = cv2.matchTemplate(screenshot_gray, img_to_compare, cv2.TM_CCOEFF_NORMED)

# Set a minimum threshold for matches
loc = np.where(res >= threshold)
loc_list = [*zip(*loc[::-1])]

final_locations = []

for location in loc_list:
    add = True

    for locked_location in final_locations:
        if abs(location[0]-locked_location[0]) < 20 or abs(location[1]-locked_location[1]) < 20:
            add = False

    if add:
        final_locations.append(location)

print("LOCATIONS", len(final_locations))
for pt in final_locations:
    print("Image found at", pt)


# Display

pygame.init()
screen = pygame.display.set_mode((screenshot_gray.shape[:2][::-1]))
alpha_surface = pygame.Surface((screenshot_gray.shape[:2][::-1]), pygame.SRCALPHA)
carImg = pygame.image.load('screen.png')

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the screenshot on the Pygame surface
    alpha_surface.blit(carImg, (0, 0))

    for found in final_locations:
        pygame.draw.rect(alpha_surface, (255, 0, 0, 100), (found[0], found[1], 40, 40))

    # Update the display
    screen.blit(alpha_surface, (0, 0))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
