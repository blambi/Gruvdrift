<?php
require_once( "lib/base_page.php" );

class Page extends Base_Page
{    
    function __construct()
    {
        $this->title = "News";
        $this->use_master = "masters/simple.php";
    }

    public function on_submit( $form )
    {
        if( isset( $_SESSION['login'] ) and $_SESSION['login'] == 1 )
        {
            // This iz the logout
            unset( $_SESSION['login'] );
        }
        else
        {
            if( $form['username'] == "admin" and $form['password'] == "fluffy" )
            {
                $_SESSION['login'] = 1;        
            }
        }

        $vars['loggedin'] = isset( $_SESSION['login'] );
        header( 'Location: '. get_rootdir() );
    }

    public function pre_render()
    {
    }

    public function render()
    {
        echo "hej";
    }
}
