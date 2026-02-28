import random
import time
import os
import asyncio
from PIL import Image

def random_sleep(min_sec, max_sec):
    delay = random.uniform(min_sec, max_sec)
    print(f"[DELAY] Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)

async def human_type(page, selector, text):
    """Types text character-by-character with random intervals."""
    try:
        await page.wait_for_selector(selector, timeout=5000)
        await page.click(selector)
        for char in text:
            # Randomizing delay between characters
            delay = random.randint(50, 250)
            await page.type(selector, char, delay=delay)
            
            # Small jitter for human effect (pauses)
            if random.random() > 0.95:
                await asyncio.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"[ERROR] Falha na digitação: {e}")

async def human_click(page, selector_or_element):
    """Simulates a human click with a small random movement before clicking."""
    try:
        if isinstance(selector_or_element, str):
            element = await page.wait_for_selector(selector_or_element, timeout=5000)
        else:
            element = selector_or_element
            
        box = await element.bounding_box()
        if box:
            # Move to a random point within the element
            x = box['x'] + box['width'] * random.random()
            y = box['y'] + box['height'] * random.random()
            await page.mouse.move(x, y, steps=10)
            await asyncio.sleep(random.uniform(0.1, 0.5))
            await page.mouse.click(x, y)
        else:
            await element.click(force=True, timeout=5000)
    except Exception as e:
        print(f"[ERROR] Falha no clique humano: {e}")

def simulate_error(error_rate):
    """Returns True if a 'human error' should be simulated based on the rate."""
    return random.random() < (error_rate / 100)

def scramble_image(image_path):
    """Renames and modifies EXIF/pixels slightly to evade hash detection."""
    if not os.path.exists(image_path):
        return None
    
    img = Image.open(image_path)
    
    # Slight transformation (resize by 1 pixel or tiny crop)
    width, height = img.size
    img = img.resize((width - 1, height - 1))
    
    # Save as new temporary name to change file signature
    new_name = f"temp_upload_{random.randint(1000, 9999)}.jpg"
    img.save(new_name, "JPEG", quality=95)
    
    return os.path.abspath(new_name)

def clean_temp_images():
    """Removes temporary scrambled images."""
    for file in os.listdir("."):
        if file.startswith("temp_upload_") and file.endswith(".jpg"):
            try:
                os.remove(file)
            except:
                pass
