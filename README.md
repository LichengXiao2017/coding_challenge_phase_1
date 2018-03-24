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

  1.Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
  
  Yes, I discovered that the mask file produced in part 1 by pure "contour" is too sparse for training the model, so I changed the configuration of parser.py in part 1 back to original values as in parsing.py.
  
  In the future, there are several possible improvement to part 1 to facilitate part 2.
  
  First, the size of dcm and mask can be rescaled to enlarge the potion of masking area, so that the mask information will be more dense, and can help training model in Part 2.
  
  Second, the original dcm and mask can also be rotate at different angles, to generate more correct training sample pairs, which will further facilitate Part 2.
  
  Third, the dcm can be further processed using image processing techniques, so as to make the contour features more apparent.
  
  2.How do you/did you verify that the pipeline was working correctly?
  
  I actually trained the pipeline, and the loss and accuracy showed on jupyter notebook, so I knew it did work, although the training speed is really slow.
  
  I even made some prediction using the model, and drawed the graph, compared them with actual mask. However, because the model is far from well-trained, the prediction is almost meaningless.
  
  3.Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?
  
  Yes, there are some deficienies and possible future improvement approaches.
  
  First, the optimizer now in use is 'adam', but usually 'sgd' is a better choice, which may be implemented in the future.
  
  Second, the batch_size, filter number, filter size, number and sturcture of layers, all of them are far from optimal. If there were more time, I can do experiments on these parameters, and try to optimize them.
  
  Third, the training pipeline can't be deployed to cloud, which makes it really slow. If there were more time, I can use google API to enable the pipeline to be trained on google cloud, which is expotentially accelerated.
  
  Fourth, ENet is faster and smaller than classical CNN. If there were more time, I can try to implement the pipeline with ENet.
