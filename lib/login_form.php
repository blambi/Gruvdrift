<?php
if( ! get_var( 'loggedin' ) )
{
?>

<form action="<? echo get_rootdir() . 'index.php' ?>" method="post">
  Username:
  <input type="textbox" class="textfield" style="width:110px;" name="username" />
  <input type="password" class="textfield" style="width:110px;" name="password" />
  <input type="submit" value="login" />
</form>

<?php
}
else
{
    echo 'Hi there admin wanna <a href="'. get_rootdir() . 'index.php/logout">logout?</a>';
}