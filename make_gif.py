from PIL import Image
import glob

files = sorted(glob.glob('result/*.png'))
images = list(map(lambda file: Image.open(file), files))

images[0].save('result.gif', save_all=True, append_images=images[1:], duration=100, loop=0)



