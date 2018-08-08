from PIL import Image
from math import ceil
# equation for finding the number of pixels in a ring:
#  pixels = (distance_from_center - 1) * 8      (+4 if even dimension)

#  STEP 1
# covert each ring of the image into an array of each linear ring
# top left is the beginning of the string

def image_to_rings(image):
	image_size = image.size[0]
	image = image.load()
	num_of_rings = ceil(image_size / 2)
	rings = []
	
	for ring in range(num_of_rings):
		if image_size % 2 == 1 and ring == num_of_rings-1:
			middle_of_image = int(image_size / 2)
			rings.append([image[ middle_of_image, middle_of_image ]])
		else:
			rings.append([])

			distance = image_size - (ring * 2) - 1

			subtract = image_size - ring - 1
			start_coords = [[ring, ring], [subtract, ring], [subtract, subtract], [ring, subtract]]	# top left of each ring
			directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

			for move_direction in range(4):
				start_coord = start_coords[move_direction]	# top left of each ring
				direction = directions[move_direction]
				for pixel in range(distance):
					x_pixel = start_coord[0] + (pixel * direction[0])
					y_pixel = start_coord[1] + (pixel * direction[1])
					rings[-1].append(image[ x_pixel, y_pixel ])
			

	return rings

def rotate_rings(rings, rotate_amount): # is a float 0.0-1.0
	edited_rings = []
	for ring in rings:
		# print(len(ring))
		rotate_threshold = 1 / len(ring)
		movement = -round(rotate_amount / rotate_threshold)
		edited_ring = ring[movement:] + ring[:movement]
		edited_rings.append(edited_ring)
	return edited_rings

def rings_to_image(rings):
	for y in rings:
		for x in y:
			dic = {(255, 255, 255, 255):"-", (0, 0, 0, 255):"@", (74, 74, 74, 255):"#"}

	image_size = int(len(rings[0]) / 4) + 1
	image = Image.new('RGBA', (image_size, image_size), 255)
	data = image.load()
	# data = [[0 for x in range(image_size*4)] for y in range(image_size)] 
	
	for ring in range(len(rings)):
		if len(rings[ring]) == 1:
			middle_of_image = int(image_size / 2)
			data[middle_of_image, middle_of_image] = rings[ring][0]
		else:
			distance = image_size - (ring * 2) - 1

			subtract = image_size - ring - 1
			start_coords = [[ring, ring], [subtract, ring], [subtract, subtract], [ring, subtract]]	
			directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
			pixel_in_ring = 0
			
			for move_direction in range(4):

				start_coord = start_coords[move_direction]
				direction = directions[move_direction]

				for pixel in range(distance):
					x_pixel = start_coord[0] + (pixel * direction[0])
					y_pixel = start_coord[1] + (pixel * direction[1])
					data[x_pixel, y_pixel] = rings[ring][pixel_in_ring]
					pixel_in_ring += 1
	# flat_data = []
	# for y in data:
	# 	for x in data:
	# 		flat_data.append(x)

	
	# image.putdata(data)
	return image



# from PIL import Image

# import random
# data = [random.randint(0, 1) for i in range(64 * 64)]

# img = Image.new('1', (64, 64))
# img.putdata(data)
# img.save('my.png')
# img.show()
spin = 128
for i in range(spin):
	direction = (1 / spin) * i
	im = Image.open("image_rotater.png")
	im = rings_to_image(rotate_rings(image_to_rings(im), direction))
	im.save("image_rotater_files/image_rotated{0}.png".format(i+1))
	if i % 12 == 0:
		print("#", end="")