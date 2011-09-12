<?php
abstract class Base_Page
{
    public $title;
    public $use_master;
    
    public function on_submit( $form )
    {
    }

    public function pre_render()
    {
    }

    abstract public function render();
}
