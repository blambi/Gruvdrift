<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Gruvdrift.se</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <link href="<?php echo get_rootdir(); ?>css/base.css" rel="stylesheet" type="text/css" />
  </head>

  <body>
    <div id="Logo">
      <img src="<?php echo get_rootdir(); ?>images/gruvdrift2.png" alt="Gruvdrift.se LOGO" />
    </div>

<?
     require( 'lib/menu_gen.php' );
?>     
    <div id="Contents">

<?
     if( get_var( "error" ) )
              echo '<div class="error">Error: '. get_var( "error" ) ."</div>";
          $this->page->render();
?>
    </div>
    </div>
  </body>
</html>
