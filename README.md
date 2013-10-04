cafd
====

computer-aided fish design

This is a simplistic "3D" object viewer written in Python, which relies on pygame.

Despite the name, it does not (yet) provide a user interface for designing objects, only for viewing them.

here is an excerpt of the code:

    if len(sys.argv) < 2 :
        print( "usage: cafd.py object" )
        print( "where object names a set of files in the objects subfolder," )
        print( "to wit:" )
        print( "objects/object.faces" )
        print( "objects/object.edges" )
        print( "objects/object.vertices" )
        exit()

here is another excerpt:

         elif event.key == pygame.K_h :
            print( '         b : colorize (replace all edge & face colors with random "blue" colors)' )
            print( '         c : colorize (replace all edge & face colors with random colors)' )
            print( '         C : colorize (replace all edge & face colors with random "dark" colors)' )
            print( '         d : debug' )
            print( '         e : toggle erase-between-frames' )
            print( '      h(H) : print this help info' )
            print( '         i : move object toward viewer (in)' )
            print( '         l : (re)load object (restore original orientation & colors)' )
            print( '         o : move object away from viewer (out)' )
            print( '         q : quit' )
            print( '         r : record object to file (appends "-new" to original name)' )
            print( '         s : change z-sort mode (min, max, avg)' )
            print( '         u : un-colorize (show monochrome pseudo-shaded)' )
            print( '         w : toggle between wireframe & "solid" representation' )
            print( '      x(X) : rotate cw(CCW) about the x axis' )
            print( '      y(Y) : rotate cw(CCW) about the y axis' )
            print( '      z(Z) : rotate cw(CCW) about the z axis' )
            print( 'arrow keys : move object left, right, up, down' )

note: the file linex.py is independent, not part of, nor used by, cafd.py
