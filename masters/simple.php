<?php
require_once( "lib/base_master.php" );

class Master extends Base_Master
{
    private $layout_file = "masters/simple.layout.php";
    public $page;

    function __construct( $page )
    {
        $this->page = $page;
    }
    
    public function render()
    {
        require_once( $this->layout_file );
    }
}
