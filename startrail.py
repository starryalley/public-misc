#!/usr/bin/env python
from gimpfu import *
import glob, os

# inspired by: http://www.startrails.de/html/software.html
#

# ref: libgimp     http://developer.gimp.org/api/2.0/libgimp/libgimp-gimpenums.html
#      Gimp Python http://www.gimp.org/docs/python/index.html
#      PDB         http://oldhome.schmorp.de/marc/pdb/index.html


def startrail(file_pattern, dark_file_pattern, output_filename):
    print "current work dir:", os.getcwd()
    print "file_pattern:", file_pattern
    print "dark_file_pattern:", dark_file_pattern
    print "output_filename:", output_filename
    print "================================"

    print "Processing Dark Frames..."
    darkframe = dark(dark_file_pattern)

    # get list of all input images
    output_image = None
    patterns = file_pattern.split(" ")
    file_list = []
    for p in patterns:
        file_list += glob.glob(p)

    
    # now every files is in file_list, loop and process all
    for fname in file_list:
        print "Processing:", fname
        image = pdb.gimp_file_load(fname, fname)
        if output_image is None:
            # create new image
            drawable = image.active_layer
            output_image = pdb.gimp_image_new (drawable.width, drawable.height, 0)
            
        # empty layer
        #layer = gimp.Layer(output_image, "new", drawable.width, drawable.height, RGBA_IMAGE, 100, NORMAL_MODE)

        # tmp image for dark frame subtraction
        tmp_image = pdb.gimp_image_new (image.active_layer.width, image.active_layer.height, 0)
        layer = pdb.gimp_layer_new_from_drawable (image.active_layer, tmp_image)
        tmp_image.add_layer(layer, -1)
        dark_layer = pdb.gimp_layer_new_from_drawable (darkframe.active_layer, tmp_image)
        pdb.gimp_layer_set_mode(dark_layer, 8) # enum GimpLayerModeEffects, GIMP_SUBTRACT_MODE == 8
        tmp_image.add_layer(dark_layer, -1)
        pdb.gimp_image_merge_visible_layers(tmp_image, 1) 

        # this is the layer after dark frame subtraction
        layer = pdb.gimp_layer_new_from_drawable (tmp_image.active_layer, output_image)
        pdb.gimp_layer_set_mode(layer, 10) # enum GimpLayerModeEffects, GIMP_LIGHTEN_ONLY_MODE == 10
        output_image.add_layer(layer, -1)
            
        # clean up
        pdb.gimp_image_delete(image)
        pdb.gimp_image_delete(tmp_image)

    # save output image
    if output_image is not None:
        # EXPAND_AS_NECESSARY (0), CLIP_TO_IMAGE (1), CLIP_TO_BOTTOM_LAYER (2)
        pdb.gimp_image_merge_visible_layers(output_image, 0) 

        print "Done! Save to", output_filename
        pdb.gimp_file_save(output_image, output_image.active_layer, output_filename, output_filename)

    pass


def dark(file_pattern):
    #http://www.astromart.com/articles/article.asp?article_id=185

    # get list of all dark images
    output_image = None
    patterns = file_pattern.split(" ")
    file_list = []
    for p in patterns:
        file_list += glob.glob(p)

    count = 1

    # now every files is in file_list, loop and process all
    for fname in file_list:
        print "Processing Dark:", fname
        image = pdb.gimp_file_load(fname, fname)
        if output_image is None:
            # create new image
            drawable = image.active_layer
            output_image = pdb.gimp_image_new (drawable.width, drawable.height, 0)
            
        layer = pdb.gimp_layer_new_from_drawable (image.active_layer, output_image)
        pdb.gimp_layer_set_opacity(layer, (1.0 / count * 100))
        #print "[%d]Transparency: %.1f" %(count, (1.0 / count * 100))
        count += 1
        #pdb.gimp_layer_set_mode(layer, 10) # enum GimpLayerModeEffects, GIMP_LIGHTEN_ONLY_MODE == 10
        output_image.add_layer(layer, -1)  # -1 means to insert it above the active layer
            
        #drawable = pdb.gimp_image_get_active_layer(image)
        pdb.gimp_image_delete(image)

    # save output image
    if output_image is not None:
        # EXPAND_AS_NECESSARY (0), CLIP_TO_IMAGE (1), CLIP_TO_BOTTOM_LAYER (2)
        pdb.gimp_image_merge_visible_layers(output_image, 1) 
        pdb.gimp_file_save(output_image, output_image.active_layer, "dark.jpg", "dark.jpg")

    print "Dark Frames done! Save to dark.jpg"
    return output_image

# 
register(
    "startrail",
    "Star Trail Maker v1.0",
    "Merge multiple exposures (pictures) into one using ligten layer mode\n Exposures are supposed to be taken on a tripot with successive same exposures so that it makes the star trails.",
    "Mark Kuo (starryalley@gmail.com)",
    "Licensed under GPLv3",
    "2010.10",
    "<Toolbox>/Xtns/Languages/Python-Fu/Star Trail Maker",
    "*",
    [
        (PF_STRING, "file_pattern", "Input File Pattern", "*.jpg"),
        (PF_STRING, "dark_file_pattern", "Dark Frames Input File Pattern", "*.jpg"),
        (PF_STRING, "output_filename", "Output Filename", "output.jpg"),
    ],
    [],
    startrail
    )
main()
