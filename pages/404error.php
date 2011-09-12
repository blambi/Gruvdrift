<?php

require_once( "lib/base_page.php" );

class Page extends Base_Page
{    
    function __construct()
    {
        $this->title = "404 Error";
        $this->use_master = "masters/simple.php";
    }

    public function render()
    {
        echo '<p>Sorry but the requested page got sever existential crises.</p>';
        echo '<p>So we could not resolve '. getenv( 'REQUEST_URI' ) . '</p>';
    }
}
