#!/usr/bin/env python3

# author : renpeng
# github : https://github.com/laodifang
# description : Python daemonizer for Unix, Linux and OS X
# date : 2015-09-28

import os
import sys
import time
import signal
import atexit

class DaemonLite(object) :
    def __init__( self, 
                  pidFile, 
                  stdin     = os.devnull, 
                  stdout    = os.devnull, 
                  stderr    = os.devnull, 
                  homeDir   = '.', 
                  umask     = 0o22, 
                  verbose   = 1, 
                  useGevent = False
                ) :
        self.pidFile     = pidFile
        self.stdin       = stdin
        self.stdout      = stdout
        self.stderr      = stderr
        self.homeDir     = homeDir
        self.umask       = umask
        self.verbose     = verbose
        self.useGevent   = useGevent
        self.daemonAlive = True

    def daemonize(self) :
        try :
            pid = os.fork()
            if pid > 0 :
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment
        os.chdir(self.homeDir)
        os.setsid()
        os.umask(self.umask)

        try :
            pid = os.fork()
            if pid > 0 :
                sys.exit(0)
        except OSError as e :
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        if sys.platform != 'darwin' :
            # Redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()

            stdInput  = open(self.stdin,  'r')
            stdOutput = open(self.stdout, 'a+')
            if self.stderr :
                stdError = open(self.stderr, 'a+')
            else:
                stdError = stdOutput

            os.dup2(stdInput.fileno(),  sys.stdin.fileno())
            os.dup2(stdOutput.fileno(), sys.stdout.fileno())
            os.dup2(stdError.fileno(),  sys.stderr.fileno())

        def sigtermhandler(signum, frame) :
            self.daemon_alive = False
            sys.exit()

        if self.useGevent :
            import gevent
            gevent.reinit()
            gevent.signal(signal.SIGTERM, sigtermhandler,  signal.SIGTERM, None)
            gevent.signal(signal.SIGINT,  sigtermhandler,  signal.SIGINT,  None)
        else:
            signal.signal(signal.SIGTERM, sigtermhandler)
            signal.signal(signal.SIGINT,  sigtermhandler)

        if self.verbose >= 1 :
            print("Started")

        # Make sure pid file is removed if we quit
        atexit.register(self._delPid)
        
        pid = str(os.getpid())

        with open(self.pidFile,'w+') as pidFile :
            pidFile.write(pid + '\n')

    def _delPid(self) :
        os.remove(self.pidFile)

    def start(self, *args, **kwargs) :
        if self.verbose >= 1 :
            print("Starting...")

        try :
            with open(self.pidFile, 'r') as pidFile :
                pid = int(pidFile.read().strip())
        except IOError :
            pid = None
        except SystemExit :
            pid = None

        if pid :
            message = "pid file %s already exists. Is it already running?\n"
            sys.stderr.write(message % self.pidFile)
            sys.exit(1)

        self.daemonize()
        self.run(*args, **kwargs)

    def stop(self) :
        if self.verbose >= 1:
            print("Stopping...")

        pid = self._getPid()

        if not pid :
            message = "pid file %s does not exist. Not running?\n"
            sys.stderr.write(message % self.pidFile)

            if os.path.exists(self.pidFile):
                os.remove(self.pidFile)

            return

        try :
            i = 0
            while 1 :
                os.kill(pid, signal.SIGTERM)
                time.sleep(1)
                i = i + 1
                if i % 10 == 0 :
                    os.kill(pid, signal.SIGHUP)
        except OSError as e :
            error = str(e)
            if error.find("No such process") > 0:
                if os.path.exists(self.pidFile):
                    os.remove(self.pidFile)
            else :
                print(str(err))
                sys.exit(1)

        if self.verbose >= 1:
            print("Stopped")

    def restart(self) :
        self.stop()
        self.start()

    def _getPid(self) :
        try :
            with open(self.pidFile, 'r') as pidFile :
                pid = int(pidFile.read().strip())
        except IOError :
            pid = None
        except SystemExit:
            pid = None
        
        return pid

    def isRunning(self) :
        pid = self._getPid()

        if pid is None :
            print('Process is stopped')
        elif os.path.exists('/proc/%d' % pid) :
            print('Process (pid %d) is running...' % pid)
        else :
            print('Process (pid %d) is killed' % pid)

        return pid and os.path.exists('/proc/%d' % pid)

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplementedError

