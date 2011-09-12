<?
/* Creates fluffy menus of doom */
// New awesome menu
require_once( 'lib/fluffy_core.php' );
$selected = get_subpage();
$menu_items = parse_ini_file( "etc/menu.conf", True );

foreach( $menu_items as $uri => $settings )
{
    if( get_var( "loggedin" ) == ( $settings['admin'] == True ) or
        get_var( "loggedin" ) == True )
    {
        if( $uri == $selected )
            printf( '<div class="selected">%s</div>', $settings['caption'] );
        else
        {
            $uri = get_rootdir() . "index.php" .( $uri == "" ? "" : "/" . $uri );
            printf( '<div><a href="%s">%s</a></div>',
                    $uri, $settings['caption'] );
        }
    }
}
