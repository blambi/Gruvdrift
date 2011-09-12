<?php
class Image_Helper
{
    private $surface = Null;

    function __construct()
    {
        $this->surface = new Imagick();
    }
    
    function read( $input_filename )
    {
        // Return True if ok, False on fail
        return $this->surface->readImage( $input_filename ); 
    }

    function scale( $width, $height )
    {
        // resscales the image to specified width, height, crops excess.
        $this->surface->scaleImage( $width, 0 );

        if( $this->surface->getImageHeight() > $height )
        {
            // Crop
        }
        elseif( $this->surface->getImageHeight() < $height )
        {
            // gap filling time
        }
    }

    function write( $output_filename )
    {
        return $this->surface->writeImage( $output_filename );
    }
}