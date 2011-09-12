<?php
require_once( "lib/base_master.php" );

class Master extends Base_Master
{
    private $layout_file = null;
    public $page;

    function __construct( $page )
    {
        $this->page = $page;
    }
    
    public function render()
    {
        $this->page->render();
    }
}
