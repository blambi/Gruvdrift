<?php
class Form_Helpers
{
    function __construct( $form )
    {
        $this->form = $form;
    }
    
    public function check_string( $key )
    {
        if( ! empty( $this->form[$key] ) )
            return $this->form[$key];

        return False;
    }

    public function check_email( $key )
    {
        if( ! empty( $this->form[$key] ) )
        {
            $ret = filter_var( $this->form[$key], FILTER_VALIDATE_EMAIL );
        
            if( ! $ret )
                return False;

            return $ret;
        }

        return "anonymous";
    }

    public function check_message( $key )
    {
        if( ! empty( $this->form[$key] ) and strlen( $this->form[$key] ) <= 1024 )
            return htmlspecialchars( $_POST['msg'] );

        return False;
    }        
}
