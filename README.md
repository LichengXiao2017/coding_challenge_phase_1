# coding_challenge_phase_1

Answer to part 1:

1. How did you verify that you are parsing the contours correctly?
	
    Subjective verify is simple. I wrote part_1_verify.py, and use matplotlib.pyplot to draw graph of contour and mask respectively, and save them as .png files, by comparing each pair of image with my eyes, it's easy to confirm that the mask is parsed correctly from contour.
    If time allows, I can develop a statistical method to measure the accuracy quantitatively.
    
2. What changes did you make to the code, if any, in order to integrate it into our production code base? 
	
    I rewrote the parsing.py to parser.py in an OOP way, so that the methods are encapsulated, and will not conflict or influence other global methods and variables in the code base when referenced.
    Since the poly_to_mask() method in parsing.py used 'outline = 0, fill = 1' when drawing the mask in this code:
    
      	ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
      
    It seems contradicted to our goal of get a mask of contour, according to the pictures in the study article:
    
      	article link: https://arxiv.org/pdf/1704.04296.pdf
      
      	picture: refer to those in above article
      
		
	Therefore, in parser.py, I changed it to:
	
		outline = 1, fill = 0
		
	This change may be further discussed with the prototyping engineer before integration to code base.
		
