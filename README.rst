|

NAME
====

    DaemonLite is a library for writing system daemons in Python. It is distributed under MIT license.

    Based on https://github.com/serverdensity/python-daemon


|

SYNOPSIS
========

.. code-block::


    from DaemonLite import DaemonLite

    class Staff(DaemonLite) :
        def run(self) :
            # Do something
        
    staff = Staff('/var/staff/staff.pid')
    staff.start()


|

Actions
===========
    start()   - starts the daemon (creates PID and daemonizes).
    stop()    - stops the daemon (stops the child process and removes the PID).
    restart() - does stop() then start().


|

Foreground
===========
    This is useful for debugging because you can start the code without making it a daemon. The running script then depends on the open shell like any normal Python script.

    To do this, just call the run() method directly.

.. code-block::


    staff.run()


|

DESCRIPTION
===========
    This is a Python class that will daemonize your Python script so it can continue running in the background. It works on Unix, Linux and OS X, creates a PID file and has standard commands (start, stop, restart) + a foreground mode.
