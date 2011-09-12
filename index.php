<?php
/* Dos front kontrolant */

/* Fult men men */
if( strpos( getenv( 'REQUEST_URI' ), "index.php" ) === False )
{
    header( "Location: ./index.php/index" );
    exit();
}

require_once( "lib/fluffy_init.php" );
require_once( "lib/fluffy_core.php" );
require_once( get_page( "%s.php" ) );

$page = new Page();
if( is_post_form() !== False )
    $page->on_submit( $_POST );

$page->pre_render();

if( $page->use_master )
{
    require_once( $page->use_master );
    $master = new Master( $page );
    $master->render();
}
else
    $page->render();
