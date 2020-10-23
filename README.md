# Synthetic aperture sonar using consumer electronics

This project started as a [class project](http://fab.cba.mit.edu/classes/862.13/students/brandon/index.html) for [MAS.862](http://fab.cba.mit.edu/classes/862.19/index.html) at MIT in 2013.

### First, generate a train of pings

    $ python ping.py pingfile.sonar 0.24 200

### Then, take a look at them

    $ python view.py pingfile.sonar

### Finally, focus to a particular plane

    $ python analyze.py
