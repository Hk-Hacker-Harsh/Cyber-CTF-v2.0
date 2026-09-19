from PIL import Image


def scramble_image(input_path, output_path):
  img = Image.open(input_path).convert('RGB')
  width, height = img.size

  scrambled_img = Image.new('RGB', (width, height))

  original_pixels = img.load()
  scrambled_pixels = scrambled_img.load()

  for x in range(width):
    for y in range(height):
      pixel = original_pixels[x, y]

      if x % 2 == 0 and y % 2 == 0:
        new_x = (x + 3) % width
        new_y = (y + 5) % height
      elif x % 2 != 0 and y % 2 != 0:
        new_x = (x - 3) % width
        new_y = (y - 5) % height
      elif x % 2 == 0 and y % 2 != 0:
        new_x = (x + 1) % width
        new_y = (y - 1) % height
      else:
        new_x = (x - 1) % width
        new_y = (y + 1) % height

      scrambled_pixels[new_x, new_y] = pixel

  scrambled_img.save(output_path)
  print(
      f"[+] Image scrambled successfully! Saved to '{output_path}' ({width}x{height})"
  )


if __name__ == '__main__':
  scramble_image('flag_image.png', 'destroyed.png')