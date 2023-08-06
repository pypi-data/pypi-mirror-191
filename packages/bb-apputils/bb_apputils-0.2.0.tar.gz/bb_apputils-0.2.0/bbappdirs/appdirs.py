import sys, os, json, tempfile, atexit, logging
from glob import glob
from datetime import datetime as dt
from os.path import ( dirname as DN,
                      expanduser,
                      isdir,
                      isfile,
                      join as JN )

log = None

class AppDirs:
    """
    Get system specific app directories
        - for initiating app configurations

        A temporary file is created and read for reading by other
      modules within the app.

      Module Data > 'expire' : expiration time in seconds
                    'name'   : application name
                    'logfile': logfile path
                    'logs'   : list of stored logs from SimpleLog
                    'time'   : initial AppDirs call time
                    'tmp'    : temporary file path
                    'shared' : shared dictionary data


        self.data['logs'] = [{ 'levelname': str(),
                               'level'    : int()
                               'time'     : datetime.timestamp(),
                               'msg'      : str(),
                               'formatted': str()  },
                                etc...  ]

    """

    def __init__( self, *, name = "", expire = 0, unique = "", simplelog = False, loglevel = 0, noerrors = False, shared = {} ):
        """
        name = provide application name
            - required
        expire = set an expiration time in seconds
            - temporary file is abandoned/deleted if older than this time
            - expire <= 0 = no expiration
            - default = 0
        unique = provide a name or unique set of characters
            - prevent other programs or modules from unintentionally reading
              or deleting the wrong temp files
            - required with every call that wants to access this data
        simplelog = use SimpleLog instead of python's built-in logging module
            - default False
        loglevel = log level for SimpleLog
            - ignored for python's logging module
        noerrors = don't print logs at exit due to errors
            - only applies if loglevel not set for SimpleLog
        shared = data to share throughout the application
            - must be in dictionary format

            SimpleLog is used for initial call. Subsequent calls, if the temp file
          is created, will load python's built-in logging module unless 'simplelog'
          is set to True.

        """
        global log

        cb = self._fromSimpleLog
        log = SimpleLog( loglevel, log_to_data = cb, init = True )

        newtmp = False
        try:
            tmp = sorted( glob( f'??????????-{name}{unique}*.pyconfig', root_dir = tempfile.gettempdir() ), reverse = True )[0]
            if expire > 0:
                now   = dt.now()
                init  = dt.fromtimestamp( int(tmp.split('-')[0] ))
                delta = now - init
                if delta.seconds > expire:
                    log.error(f"Temporary file has reached expiration set time of {expire} seconds")
                    self.cleanTmp(name, unique)
                    newtmp = True

        except IndexError:
            newtmp = True

        if tmp:
            with open( JN( tempfile.gettempdir(), tmp ), 'r' ) as f:
                self.data = json.load(f)

            if not self.data['simplelog']:
                log = logging.getLogger(__name__)

            log.debug("Loaded existing temp data")
            if self.data['logs']:
                func = { 'debug': log.debug, 'info': log.info, 'warning': log.warning, 'error': log.eror, 'critical': log.critical }
                for i in sorted( self.data['logs'], key = lambda x: x['time'] )]:
                    func[ i['levelname'] ]( i['msg'] )

        else:
            if not name:
                raise ValueError( "Initial call from application must include a name" )

            time = int( dt.now().timestamp() )
            tmp  = tempfile.NamedTemporaryFile( delete = False, prefix = f"{time}-{name}{unique}", suffix = '.pyconfig' ).name
            self.data = { 'name'     : name,
                          'time'     : time,
                          'logfile'  : JN( self.getDir('log'), f"log-{time}.html" ),
                          'logs'     : [],
                          'tmp'      : tmp.name,
                          'expire'   : expire,
                          'shared'   : {},
                          'loglevel' : loglevel,
                          'noerrors' : noerrors,
                          'simplelog': simplelog }

            self.save( self.data )
            atexit.register( self.onExit )

        if shared:
            self.addSharedData( **shared )

    @staticmethod
    def save(obj):
        log.info(f"Temporary file saved as '{obj['tmp']}'")

        with open( obj['tmp'], 'w' ) as f:
            json.dump( obj, f, separators = ( ',', ':' ))

    @staticmethod
    def getRuntime( obj ):
        now = dt.now()
        start = dt.fromtimestamp( self.data['start'] )
        delta = now - start

        secs, mins, hrs = delta.seconds, 0, 0
        if secs > 60:
            mins = int( secs / 60 )
            secs = secs % 60

        if mins > 60:
            hrs = int( mins / 60 )
            mins = mins % 60

        return { 'start'  : start.strftime('%A, %b %d, %Y @ %r'),
                 'end'    : now.strftime('%A, %b %d, %Y @ %r'),
                 'runtime': f"{hrs:02d}:{mins:02d}:{secs:02d}" }

    def _fromSimpleLog(self, level, **log):
        self.data['logs'].append({ 'level': level, **log })
        self.save( self.data )

    def addSharedData(self, **kwargs):
        """
        Add dictionary data to the tmp file to share with other modules during session
            - available using the __call__ method, first argument 'shared'
        """
        if isinstance( shared, dict ):
            self.data['shared'] = { **self.data['shared'], **shared }
        else:
            log.error("Shared data must be in dictionary form")

        self.save( self.data )

    def cleanTmp(self, name, unique):
        for i in glob( f'??????????-{name}{unique}*.pyconfig', root_dir = tempfile.gettempdir() ):
            os.remove( JN( tempfile.gettempdir(), i ))

    def clearSharedData(self, *args):
        log.info("Clearing shared data from temp file")
        self.data['shared'] = {}

        self.save( self.data )

    def getDir(self, _dir ):
        """
        Return user application directories
            _dir = 'cache' - user cache directory
                   'data'  - user app data directory
                   'log'   - log directory in user app data

            - creates directory if it doesn't exist
        """
        DIR = { 'darwin' : { 'cache': JN( expanduser('~'), "Library", "Application Support", self.data['name'], "cache" ),
                             'data' : JN( expanduser('~'), "Library", "Application Support", self.data['name'] ),
                             'log'  : JN( expanduser('~'), "Library", "Application Support", self.data['name'], 'log' )},
                'windows': { 'cache': JN( expanduser('~'), "AppData", self.data['name'], "cache" ),
                             'data' : JN( expanduser('~'), "AppData", self.data['name'] ),
                             'log'  : JN( expanduser('~'), "AppData", self.data['name'], 'log' )},
                'linux'  : { 'cache': JN( expanduser('~'), ".cache", self.data['name'] ),
                             'data' : JN( expanduser('~'), ".config", self.data['name'] ),
                             'log'  : JN( expanduser('~'), ".config", self.data['name'], 'log' )}}

        d = DIR[ sys.platform ][ _dir ]
        os.makedirs( d, exist_ok = True )

        return d

    def getLogfile(self):
        logdir = DN( self.data['logfile'] )

        if not self.hasLogfile():
            loglist = sorted( os.listdir( logdir ), reverse = True )
            date = dt.fromtimestamp( self.data['time'] ).strftime('%A, %b %d, %Y - %r')

            while len( loglist ) >= 10:
                os.remove( JN( logdir, loglist.pop(0) ))

            with open( self.data['logfile'], 'w' ) as f:
                f.write( f"# {self.data['name']} Log - {date}\n\n" )

        return logfile

    def getAppName(self):
        return self.data['name']

    def getTmpFile(self):
        return self.data['tmp']

    def getStartTime(self):
        return dt.fromtimestamp( self.data['time'] )

    def hasLogFile(self):
        if isfile( self.data['logfile'] ):
            return True
        return False

    def onExit(self):
        tmpfiles = [ JN( tempfile.gettempdir(), i ) for i in \
            sorted( glob( f'[0-9]-{code}*.pyconfig', root_dir = tempfile.gettempdir() ), reverse = True )]
        if not tmpfiles:
            sys.stderr.write( "\x1b[1;31m  [ERROR]\x1b[0m no tempfile found to remove" )
            return

        with open( tmpfiles[0], 'r' ) as f:
            self.data = json.load(f)

        cnt = 1
        for i in tmpfiles:
            os.remove(i)
            if cnt > 1:
                sys.stderr.write( f"\n\x1b[1;33m  [WARNING]\x1b[0m extra tmp file deleted - {i}\n" )
            cnt += 1

        rt = self.getRuntime( self.data )
        log.info("Process completed")
        log.info(f"Started: {rt['start']}")
        log.info(f"Ended: {rt['end']}")
        log.info(f"Total Runtime: {rt['runtime']}")
        log.info("Exiting now...")

        if not isinstance( log, logging.getLoggerClass() ):
            if self.print_log_on_exit and self.loglevel == 0:
                hasErrors = False
                for i in self.data['logs']:
                    if i['level'] in ( 4, 5 ):
                        hasErrors = True
                        break

                if hasErrors:
                    log_msgs = [ i['formatted'] for i in sorted( logs, key = lambda x: x['time'] )]
                    sys.stderr.write('\n')
                    for i in log_msgs:
                        sys.stderr.write(f"{i}\n")

class SimpleLog:
    """
    SimpleLog

      A simple logger. Is used during initial call to AppDirs to give the application
    the chance to initiate python's logging module before loading it here.

    """

    def __init__(self, level = 0, *, log_to_data = None):
        """
        Initiate SimpleLog

          *args
            - level = 0: off [default]
                      1: debug
                      2: info
                      3: warning
                      4: error
                      5: critical

          **kwargs:
            - log_to_data = callback function to write log data to temp file

            Similar to the standard built-in logging, messages from set level and above
          will be displayed. Level set to 0 will turn SimpleLog off. This does not effect
          python's built-in logging module.

        """
        try:
            assert level >= 0 and level <= 5
            self.level = level
        except:
            sys.stderr.write("\n\x1b[1;31m  [CRITICAL]\x1b[0;3m Invalid log level for SimpleLog\x1b[0m\n\n")
            sys.stderr.write("\x1b[1;33m  [WARNING]\x1b[0;3m Setting log level to 0 (off)\x1b[0m\n\n")
            self.level = 0

        self.CB = log_to_data

    def debug(self, _str):
        self._log( "\x1b[2;37m", 'debug', _str )

    def info(self, _str):
        self._log( "\x1b[0;36m", 'info', _str )

    def warning(self, _str):
        self._log( "\x1b[1;33m", 'warning', _str )

    def error(self, _str):
        self._log( "\x1b[0;31m", 'error', _str )

    def critical(self, _str):
        self._log( "\x1b[1;31m", 'critical', _str )

    def _log(self, col, L, _str):
        levels = { 'debug'   : 1,
                   'info'    : 2,
                   'warning' : 3,
                   'error'   : 4,
                   'critical': 5 }

        formatted = f"{col}  [{L.upper()}]\x1b[0;3m {_str}\x1b[0m"
        T = dt.now()

        if self.CB:
            time = int( T.timestamp() )
            self.CB( levels[L],
                     levelname = L,
                     msg = _str,
                     time = time,
                     formatted = formatted )

        if self.level > 0 and self.level <= levels[L]:
            colors = { 'debug'   : '\x1b[2;37m',
                       'info'    : '\x1b[0;36m',
                       'warning' : '\x1b[1;33m',
                       'error'   : '\x1b[0;31m',
                       'critical': '\x1b[1;31m' }

            lname = L.upper()
            width = os.get_terminal_size().columns
            if len(_str) + len(lname) + 21 > width:
                words, msg_lines, first = [], [], len(lname) + 5
                for i in msg.split():
                    if len(' '.join( words )) + first + len(i) + 1 > width:
                        first = 0
                        msg_lines.append( ' '.join( words ))
                        words = [ '          ', i ]
                        continue
                    words += [i]

                if words:
                    msg_lines.append( ' '.join(words) )

                space = width - 11 - len(lname) - ( len(msg_lines[-1]) - ( int(len(msg_lines[-1]) / width) * width ))
                if space < 0:
                    msg_lines[-1] += f"{' ':.<{-i - 1}}"
                    msg_lines += [ "          " ]
                    space = width - 16

                record.msg = '\n'.join(msg_lines)

            else:
                space = width - 21 - len(lname) - ( len(_str) - ( int(len(_str) / width) * width ))

            msg = f"{colors[L]}  [{lname}]\x1b[0;3m {_str}\x1b[0m  {' ':.>{space}}-\x1b[1;37m {T.strftime('[%R:%S]')}\x1b[0m"
            sys.stderr.write( '\n' + msg + '\n' )
