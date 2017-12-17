# gCode-Extraction
This package includes a python script and two solidworks macros. This tool allows to extract tool paths from a gcode file and output them to sequenced csv text files. The first macro will take these files and create a circular extrude along each path. The second macro will take each file and combine it into a combined part. 

## How To Use
1. Start with the **process_gcode.py** script. Either run it from command line or from an IDE. Check the code for optional settings.
  * The script will prompt you with a file browser, locate your .gcode file that you wish to process
  * A new folder will be made in the tool's root using either the project name you put in or based off the gcode file you entered
2. In this folder you will find input and output folders, a logs folder as well as two .swp macros.
3. First run the **batch_extrude.swp** macro. This will process all the files .txt files that have been generated at step 1. **BE ADVICED THAT THIS WILL TAKE A LONG TIME!** For the test part that is included, it took approcimately 45 minutes. 
  * In the logs folder you will find a .txt file that shows if the processing went well and how long each item took
  * Sometimes SW is not able to do a particular extrude, this will be denoted in the .txt file and require manual fixing (super easy). 
  * The SW files can be found in the output/SW folder
4. After all files have been fixed, run the **bath_combine.swp** macro. This will get all the SW files and combine them into one. 

## Limitations and TO-DO
As for now, the final macro only inserts all the different parts but does not combine them into one single piece of geometry. Simply using combine geometry did not work, at least not on all parts at once. It might be possible when doing it layer by layer. Another solution might be to create a solid block encompasses the volume of the final part. Then use each extrude to cut a part out of that block. After all the cuts, add another solid block of equal size and use the difference of the two blocks as the final part. This should be easily incorperated into a SW macro that loops over every part and cuts. 
As this will ammount to many cuts, in order to prevent exponential processing times, it might be sensible to do this per layer and then save that layer as a new part, to finally then combine all the layers.
