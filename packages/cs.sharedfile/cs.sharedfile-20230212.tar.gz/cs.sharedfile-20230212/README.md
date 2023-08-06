Facilities for shared access to files.

*Latest release 20230212*:
Remove dependency on cs.logutils.

## Function `lockfile(path, ext=None, poll_interval=None, timeout=None)`

A context manager which takes and holds a lock file.

Parameters:
* `path`: the base associated with the lock file.
* `ext`:
  the extension to the base used to construct the lock file name.
  Default: `".lock"`
* `timeout`: maximum time to wait before failing,
  default None (wait forever).
* `poll_interval`: polling frequency when timeout is not 0.

## Class `SharedAppendFile`

A base class to share a modifiable file between multiple users.

The use case was driven from the shared CSV files used by
`cs.nodedb.csvdb.Backend_CSVFile`, where multiple users can
read from a common CSV file, and coordinate updates with a
lock file.

This presents the following interfaces:
* `__iter__`: yields data chunks from the underlying file up
  to EOF; it blocks no more than reading from the file does.
  Note that multiple iterators share the same read pointer.

* `open`: a context manager returning a writable file for writing
  updates to the file; it blocks reads from this instance
  (though not, of course, by other users of the file) and
  arranges that users of `__iter__` do not receive their own
  written data, thus arranging that `__iter__` returns only
  foreign file updates.

Subclasses would normally override `__iter__` to parse the
received data into their natural records.

*Method `SharedAppendFile.__init__(self, pathname, read_only=False, write_only=False, binary=False, newline=None, lock_ext=None, lock_timeout=None, poll_interval=None)`*:
Initialise this SharedAppendFile.

Parameters:
* `pathname`: the pathname of the file to open.
* `read_only`: set to true if we will not write updates.
* `write_only`: set to true if we will not read updates.
* `binary`: if the file is to be opened in binary mode, otherwise text mode.
* 'newline`: passed to `open()`
* `lock_ext`: lock file extension.
* `lock_timeout`: maxmimum time to wait for obtaining the lock file.
* `poll_interval`: poll time when taking a lock file,
  default `DEFAULT_POLL_INTERVAL`

*Method `SharedAppendFile.__iter__(self)`*:
Iterate over the file, yielding data chunks until EOF.

This skips data written to the file by this instance so that
the data chunks returned are always foreign updates.
Note that all iterators share the same file offset pointer.

Usage:

    for chunk in f:
        ... process chunk ...

*Method `SharedAppendFile.close(self)`*:
Close the SharedAppendFile: close input queue, wait for monitor to terminate.

*Property `SharedAppendFile.filestate`*:
The current FileState of the backing file.

*Method `SharedAppendFile.open(self)`*:
Open the file for append write, returing a writable file.
Iterators are blocked for the duration of the context manager.

*Method `SharedAppendFile.rewrite(self)`*:
Context manager for rewriting the file.

This writes data to a new file which is then renamed onto the original.
After the switch, the read pointer is set to the end of the new file.

Usage:

    with f.rewrite() as wfp:
        ... write data to wfp ...

*Method `SharedAppendFile.tail(self)`*:
A generator returning data chunks from the file indefinitely.

This supports writing monitors for file updates.
Note that this, like other iterators, shares the same file offset pointer.
Also note that it calls the class' iterator, so that if a
subsclass returns higher level records from its iterator,
those records will also be returned from tail.

Usage:

    for chunk in f:
        ... process chunk ...

## Class `SharedAppendLines(SharedAppendFile)`

A line oriented subclass of `SharedAppendFile`.

## Class `SharedCSVFile(SharedAppendLines, SharedAppendFile)`

Shared access to a CSV file in UTF-8 encoding.

*Method `SharedCSVFile.__iter__(self)`*:
Yield csv rows.

*Method `SharedCSVFile.writer(self)`*:
Context manager for appending to a CSV file.

## Class `SharedWriteable`

Wrapper for a writable file with supported mutex based cooperation.

This is mostly a proxy for the wrapped file
exceptthat all `.write` calls are serialised
and when used as a context manager
other writers are blocked.

This is to support shared use of an output stream
where certain outputs should be contiguous,
such as a standard error stream used to maintain a status line
or multiline messages.

*Method `SharedWriteable.__enter__(self)`*:
Take the lock and return.

*Method `SharedWriteable.__exit__(self, *_)`*:
Release the lock and proceed.

*Method `SharedWriteable.__getattr__(self, attr)`*:
This object is mostly a proxy for the wrapped file.

*Method `SharedWriteable.write(self, s)`*:
Obtain the lock and then run the wrapped `.write` method.

# Release Log



*Release 20230212*:
Remove dependency on cs.logutils.

*Release 20211208*:
Update import.

*Release 20201228*:
New SharedWriteable class to manage concurrent output with a mutexed .write method and a context manager for grouping larger uses.

*Release 20190102*:
Context manager bugfix.

*Release 20170608*:
* Facilities for shared files, split out from cs.fileutils.
* SharedAppend* classes. lockfile function.
