import av

# Generate Video from PIL Image Arrays
def generate_video_from_pil_images(pil_images, output, width, height):
	container = av.open(output, mode="w")

	stream = container.add_stream('mpeg4', rate=30)
	stream.width = width
	stream.height = height

	def encode(pil_image):
		frame = av.VideoFrame.from_image(pil_image)
		for packet in stream.encode(frame):
			container.mux(packet)
		
	for pil_image in pil_images:
		encode(pil_image)
	
	container.close()


# Generate Seek Video
def generate_seek_video(pil_images, target_index, output, width, height):
	container = av.open(output, mode="w")
	
	stream = container.add_stream("mpeg4", rate=30)
	stream.width = width
	stream.height = height
	
	def encode(pil_image):
		frame = av.VideoFrame.from_image(pil_image)
		for packet in stream.encode(frame):
			container.mux(packet)
			
	reversed_images = pil_images[::-1]
	second_part = pil_images[target_index:-1] 
	reversed_second_part = second_part[::-1]
	
	seek_images = pil_images + reversed_images + pil_images + reversed_second_part
	focus_images = [pil_images[target_index]] * 180
	
	for image in seek_images :
		slow_motion_frames = [image] * 6
		for frame in slow_motion_frames:
			encode(frame)
	
	for focus_image in focus_images:
		encode(focus_image)
		
	container.close()


# Generate Instagram Video
def generate_instagram_vid(vid_name, vid_width, vid_height, pil_images, stop_index, fps, repeat_rate,slow_motion_rate):
	container = av.open(vid_name, mode="w")

	### Add mp4 stream to container with fps, width and height
	stream = container.add_stream("mpeg4", rate=int(fps))
	stream.width = vid_width
	stream.height = vid_height
	
	### Write Encode function to Encode frame into Mpeg4 format
	def encode(image):
		frame = av.VideoFrame.from_image(image)
		for packet in stream.encode(frame):
			container.mux(packet)
			
	def slow_motion_reverse(pil_images):
		frames_count = len(pil_images)
		total_frames = frames_count * 2 * repeat_rate
		print("Total Frames is ", total_frames)
		
		for idx in range(total_frames):
			local_index = idx%len(pil_images)
			play_times = int(idx/len(pil_images))
		
			if play_times % 2 == 0 and play_times < (repeat_rate * 2 - 1):
				frame_index = local_index
				print(frame_index, play_times)
				frame = pil_images[local_index]
				frames = [frame] * slow_motion_rate
				for frame in frames:
					encode(frame)
					
			elif play_times == (repeat_rate * 2 - 1):
				frame_index = frames_count - local_index - 1
				if frame_index > stop_index:
					print(frame_index, play_times)
					frame = pil_images[frame_index]
					frames = [frame] * slow_motion_rate * 3
					for frame in frames:
						encode(frame)

				elif frame_index == stop_index:
					print(frame_index, play_times)
					frame = pil_images[frame_index]
					frames = [frame] * slow_motion_rate * 90
					for frame in frames:
						encode(frame)
								
			else:
				print(frame_index, play_times)
				frame = pil_images[frames_count - local_index - 1]
				frames = [frame] * slow_motion_rate
				for frame in frames:
					encode(frame)
			
	slow_motion_reverse(pil_images)
	
	### Close Container
	container.close()