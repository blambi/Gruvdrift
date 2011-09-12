<?
function get_page( $filter )
{
    $page = str_replace( getenv( 'SCRIPT_NAME' ), '', getenv( 'REQUEST_URI' ) );

    // remove any get's
    $page = preg_replace( '/\?.*/', '', $page );

    // convert / to _ for subpage support
    $page = str_replace( '/', '_', $page );
    
    if( $page == "" )
        $page = "index";
    else
        $page = substr( $page, 1 );

    $page = sprintf( $filter, $page );
    
    $pages = scandir( "pages/" );  
    if( ! in_array( $page, $pages ) )
        if( strpos( $filter, "code" ) !== False )
            return NULL;
        else   
            $page = "404error.php";
    
    return "pages/" . $page;
}


function get_subpage()
{
    $page = str_replace( getenv( 'SCRIPT_NAME' ), '', getenv( 'REQUEST_URI' ) );

    if( $page == "" )
        return "index";

    else
        return substr( $page, 1 );
}

function get_rootdir()
{
    /* Returns our projects root working dir */
    return dirname( getenv( 'SCRIPT_NAME' ) ) ."/";
}

function is_post_form()
{
    return $_POST != Array();
}

function image( $name )
{
    echo '<img src="'. get_rootdir() . "public/images/" . $name ."\"/>\n";
}

function get_var( $key )
{
    return ( isset ( $GLOBALS['vars'][$key] )) ? $GLOBALS['vars'][$key] : false;
}

function set_var( $key, $value )
{
    $GLOBALS['vars'][$key] = $value;
}