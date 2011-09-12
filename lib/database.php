<?php
/*         ..     .      .                   .. ..               .
       .... .    .      ..       (           .   ..     ..       .
       .    .   .    ....        )           .......     .      ..
.      .   .   .   .            (            ..   ...... .. ..  .
 .     .. .    . ..       /\  .-"""-.  /\          .. ...... ......
 ..     .      ..        //\\/  ,,,  \//\\          .  ..  .    .. ..
   . . . .               |/\| ,;;;;;, |/\|          .       ... .. ..
    . ..... .  .         //\\\;-"""-;///\\           .         ..   .
   .....      .         //  \/   .   \/  \\          .         .... ..
   ..   .   .          (| ,-_| \ | / |_-, |)         .    ..   . .  . .
  ..   ...  ..           //`__\.-.-./__`\\            .   .    .  . ..
 .  . ..  .    ..       // /.-(() ())-.\ \\           .   .    .  ...  .
..   ...   .    .      (\ |)   '---'   (| /)              .   .. .. .   ..
 .    . .. ..   .       ` (|           |) `               .  .....  .     .
.    ..   ..  . .         \)           (/                .   ....   .     ..
 .    .        ..                                       ..   .. .          .
       ....                                                     .
           ... ....       Hi there, seen any bugs?            ..
              ..                 - Glenn the Spider
*/



class Database
{
    private $db;
    private static $instance;
    
    private function __construct()
    {
        $this->db = new SQLiteDatabase( "data/masql.db", SQLITE3_OPEN_CREATE );

        /* if our table don't exists create it */
        if( ! @$this->db->query( "SELECT RowID FROM img_collections LIMIT 1" ) )
        {
            /* Note RowID is allways existing and autocreated in
             * sqlite databases so we use that one */
            $this->db->query( "CREATE TABLE img_collections (
name VARCHAR NOT NULL,
position INT DEFAULT 0 )" );
        }

        if( ! @$this->db->query( "SELECT RowID FROM img_images LIMIT 1" ) )
        {
            $this->db->query( "CREATE TABLE img_images (
name VARCHAR NOT NULL,
coll_id INT NOT NULL,
filename VARCHAR NOT NULL,
position INT DEFAULT 0 )" );
        }
    }

    function get_collections()
    {
        $resp = $this->db->query( 'SELECT RowID, * FROM img_collections ORDER BY position ASC' );

        $posts = Array();
        
        while( $row = $resp->fetch( SQLITE3_ASSOC ) )
        {
            // Hackish but still have to get a better hang on joins..
            $resp2 = $this->db->query( "SELECT filename FROM img_images WHERE coll_id = ". $row['RowID'] ." ORDER BY position LIMIT 1" );
            $row2 = $resp2->fetch( SQLITE3_ASSOC );

            if( $row2 != False )
                $row['thumbnail'] = str_replace( '.png', '-thumb.png', $row2['filename'] );
            else
                $row['thumbnail'] = "noimages.png";
            
            $row['images'] = 0; // TODO: Add image count
            $posts[] = $row;
        }

        return $posts;
    }

    function create_collection( $name )
    {
        $name = sqlite_escape_string( $name );

        if( $name == "" )
            throw new Exception( "Bad name..." );
        
        $this->db->query( 'INSERT INTO img_collections (name) VALUES ( "'. $name .'")' );
    }

    function get_collection_name( $collection_id )
    {
        if( ! is_numeric( $collection_id ) )
            throw new Exception( "Not an int..." );

        $resp = $this->db->query( 'SELECT name FROM img_collections WHERE RowID = '. $collection_id );

        $x = $resp->fetch( SQLITE3_ASSOC );

        if( $x != Null )
            return $x['name'];
        
        return "hmmm bad...";
    }

    function update_collection_positions( $order )
    {
        foreach( $order as $pos => $id )
        {
            if( ! is_numeric( $id ) )
                return false;
        } // check first...

        foreach( $order as $pos => $id ) // Not that nice but...
        {
            $resp = $this->db->query( 'UPDATE img_collections SET position = '. $pos .' WHERE RowID = '. $id );
        }
        
        return true;
    }

    function update_collection_name( $id, $new_name )
    {
        if( ! is_numeric( $id ) )
            return false;
        $new_name = sqlite_escape_string( $new_name );
        $resp = $this->db->query( 'UPDATE img_collections SET name = "'. $new_name .'" WHERE RowID = '. $id );
        return true;
    }

    function delete_collection( $id )
    {
        if( ! is_numeric( $id ) )
            return false;

        // Remove all image records
        $resp = $this->db->query( 'DELETE FROM img_images WHERE coll_id = '. $id );
        
        // Remove collection
        $resp = $this->db->query( 'DELETE FROM img_collections WHERE RowID = '. $id );

        return true;
    }
    

    function get_images( $collection_id )
    {
        if( ! is_numeric( $collection_id ) )
            throw new Exception( "Not an int..." );

        $resp = $this->db->query( 'SELECT RowID, * FROM img_images WHERE coll_id = '. $collection_id .' ORDER BY position' );
        
        $posts = Array();
        
        while( $row = $resp->fetch( SQLITE3_ASSOC ) )
        {
            $posts[] = $row;
        }

        if( empty( $posts ) )
            $posts[] = Array( 'RowID' => -1,
                              'coll_id' => $collection_id,
                              'filename' => "noimages.png",
                              'name' => "Sorry no pictures here",
                              'position' => 0 );

        return $posts;
    }

    function get_image_filename( $id )
    {
        if( ! is_numeric( $id ) )
            throw new Exception( "Not an int..." );

        $resp = $this->db->query( 'SELECT RowID, filename FROM img_images WHERE RowID = '. $id );
        return $resp->fetch( SQLITE3_ASSOC );
    }
    
    function add_image( $collection_id, $title, $filename )
    { 
        $title = sqlite_escape_string( $title );

        if( $title == "" )
            throw new Exception( "Bad title..." );

        if( ! is_numeric( $collection_id ) )
            throw new Exception( "Not an int..." );

        $this->db->query( 'INSERT INTO img_images ( name, coll_id, filename ) VALUES ( "'. $title .'", '. $collection_id .', "'. $filename .'" )' );
    }

    function delete_image( $id )
    {
        if( ! is_numeric( $id ) )
            return false;

        $resp = $this->db->query( 'DELETE FROM img_images WHERE RowID = '. $id );
        return true;
    }
    
    function update_images_positions( $order )
    {
        foreach( $order as $pos => $id )
        {
            if( ! is_numeric( $id ) )
                return false;
        } // check first...

        foreach( $order as $pos => $id ) // same as for the collection images...
        {
            $resp = $this->db->query( 'UPDATE img_images SET position = '. $pos .' WHERE RowID = '. $id );
        }
        
        return true;
    }

    function update_image_name( $id, $new_name )
    {
        if( ! is_numeric( $id ) )
            return false;
        $new_name = sqlite_escape_string( $new_name );
        $resp = $this->db->query( 'UPDATE img_images SET name = "'. $new_name .'" WHERE RowID = '. $id );
        return true;
    }

    
    public static function get_instance()
    {
        if( self::$instance == NULL )
            self::$instance = new Database();

        return self::$instance;
    }
}
?>
