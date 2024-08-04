


import pyautogui
import time

def center_coordinates(rect):
    x = rect[0] + rect[2] // 2
    y = rect[1] + rect[3] // 2
    return x, y
  
def search_and_click_image(image_path):
    image_location = pyautogui.locateOnScreen(image_path)
    if image_location:
        center_x, center_y = center_coordinates(image_location)
        pyautogui.click(center_x, center_y)
        print(f"Clicked on the center of {image_path}")
    else:
        print(f"Image {image_path} not found")
      
if __name__ == "__main__":
    image_path = 'img/1.png'
    search_and_click_image(image_path)
