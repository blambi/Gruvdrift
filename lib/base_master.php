<?php

abstract class Base_Master
{
    private $layout_file;
    public $page;

    function __construct( $page )
    {
        $this->page = $page;
    }
    
    abstract public function render();
}
