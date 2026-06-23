import cv2
import numpy as np

def apply_color_filter(image, filter_type, power):
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,0] = 0
        filtered_image[:,:,2] = cv2.add(filtered_image[:,:,2], power)
    elif filter_type == "blue_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,2] = 0
        filtered_image[:,:,0] = cv2.add(filtered_image[:,:,0], power)
    elif filter_type == "green_tint":
        filtered_image[:,:,0] = 0
        filtered_image[:,:,2] = 0
        filtered_image[:,:,1] = cv2.add(filtered_image[:,:,1], power)
    elif filter_type == "increase_red":
        filtered_image[:,:,2] = cv2.add(filtered_image[:,:,2], power)
    elif filter_type == "decrease_blue":
        filtered_image[:,:,0] = cv2.subtract(filtered_image[:,:,0], power)
    return filtered_image

image_path = "planet.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
else:
    filter_type = "original"
    power = 0

    print("Press keys:\n r- Red tint\n b- Blue tint\n g- Green tint\n i- Increase Red\n d- Decrease Blue\n q- Quit")

    while True:
        filtered_image = apply_color_filter(image, filter_type, power)
        cv2.imshow("Filtered Image", filtered_image)
        key = cv2.waitKey(0) & 0xFF

        if key in [ord('r'), ord('b'), ord('g'), ord('i'), ord('d')]:
            filter_type = {"r":"red_tint","b":"blue_tint","g":"green_tint","i":"increase_red","d":"decrease_blue"}[chr(key)]
            power = int(input("Enter power value: "))
        elif key == ord('q'):
            break
        else:
            print("Invalid key.")

cv2.destroyAllWindows()
