<?
require_once( "lib/database.php" );

session_start();
/*data_default_timezone_set( @date_default_timezone_get() );*/
set_include_path( get_include_path() . PATH_SEPARATOR . "lib/" );

$GLOBALS['vars'] = array(
    "loggedin" => isset( $_SESSION['login'] ),
    "error" => NULL,
    );

$db = Database::get_instance();
