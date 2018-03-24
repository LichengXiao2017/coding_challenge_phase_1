# coding_challenge_phase_1

Answer to part 1:

1. How did you verify that you are parsing the contours correctly?
	
    Subjective verify is simple. I wrote part_1_verify.py, and use matplotlib.pyplot to draw graph of contour and mask pairs, and save them as .png files under process_data/icontour_coords_images and processed_data/mask_images.
    By comparing each pair of image with eyes, it's easy to confirm that the mask is parsed correctly from contour.
    If time allows, I can develop a statistical method to measure the accuracy quantitatively.
    
2. What changes did you make to the code, if any, in order to integrate it into our production code base? 
	
    I rewrote the parsing.py to parser.py in an OOP way, so that the methods are encapsulated, and will not conflict or influence other global methods and variables in the code base when referenced.
    I tried to change the poly_to_mask() mathod in parsing.py, by replacing 'outline = 0, fill = 1' to 'outline = 1, fill = 0', which seemed more close to the definition of "contour". However, this proved to be a bad idea later in the training of CNN, since the pure "contour" mask is too sparse to effectively train the model. Therefore, I changed back to the original configuration.

Answer to part 2:
