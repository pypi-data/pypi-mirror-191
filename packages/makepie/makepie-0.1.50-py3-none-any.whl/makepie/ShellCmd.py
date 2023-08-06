from io import BytesIO, TextIOWrapper
import logging, os, time, sys
from subprocess import PIPE, Popen
from .MakepieLogging import applog
from .Exceptions import MakepieException
from .Config import config

log = logging.getLogger(__name__)

class ShellCommand:
	def __init__(
		self,
		cmd: str,
		logger: logging.Logger,
		env=os.environ,
		quiet=False,
		timeout: float=None,
		throws: bool=True,
		use_pipes: bool=False,
		stdin=sys.stdin,
	):
		self.cmd = cmd
		self.logger = logger
		self.env = env
		self.quiet = quiet
		self.timeout = timeout
		self.throws = throws
		self.use_pipes = use_pipes
		
		self.tty = True

		if isinstance(stdin, str):
			stdin = stdin.encode()
		if isinstance(stdin, bytes):
			self.tty = False
			stdin = BytesIO(stdin)
		# if isinstance(stdin, TextIOWrapper):
		# 	stdin = stdin.buffer
		self.stdin = stdin
		self.stdout = BytesIO() if use_pipes else None
		self.stderr = BytesIO() if use_pipes else None

		self.subprocess: Popen = None
		self.exec_time = None

	def logdata(self, data: bytes, name: str):
		if len(data) == 0 or self.quiet:
			return

		text = data.decode(errors="replace")
		if not config("PRINT_STREAM_NAME", False):
			self.logger.info(text)
			return

		# Remove last character if it is a newline
		if text[-1] == "\n":
			text = text[:-1]

		# Insert prefix at the beginning of each line
		prefix = f"{name}> "
		formatted = prefix + text.replace("\n", "\n" + prefix) + "\n"
		self.logger.info(formatted)

	def log_stream(self, name: str):
		outdata = self.subprocess.__getattribute__(name).read(config("MAX_READ_SIZE", 4096))
		if outdata is None:
			return False

		self.__getattribute__(name).write(outdata)
		self.logdata(outdata, "out")
		return outdata != b""

	def log_streams(self):
		if not self.use_pipes:
			return False
		return self.log_stream("stdout") or self.log_stream("stderr")

	# Wait for the process to finish and log its output
	# stdin, process stdout & stderr should be set to non-blocking
	# Logger should have no terminator
	def subprocess_wait_loop(self):
		start = time.time()

		# Wait for command to finish/timeout
		while True:
			if (self.timeout is not None) and (time.time() - start > self.timeout):
				self.subprocess.kill()
				self.subprocess.wait()
				raise MakepieException(f"Command timed out after {self.timeout} seconds")

			if self.subprocess.stdin is not None:
				data = self.stdin.read(config("MAX_READ_SIZE", 4096))
				if data is not None:
					if len(data) > 0:
						self.subprocess.stdin.write(data)
					else:
						self.subprocess.stdin.close()

			self.log_streams()

			# Exit condition
			if self.subprocess.poll() is not None:
				self.subprocess.wait()
				break

			time.sleep(config("POLL_INTERVAL", 0.01))

		# Empty streams
		while self.log_streams():
			pass

		self.exec_time = time.time() - start

	def _run(self):
		if not self.quiet:
			self.logger.debug(f"shell> {self.cmd}")

		# Trick to avoid handling newline mess of streams
		previous_val = self.logger.handlers[0].terminator
		self.logger.handlers[0].terminator = ""

		# Save blocking state & set to non-blocking
		if self.subprocess.stdout is not None:
			out_no = self.subprocess.stdout.fileno()
			b_out = os.get_blocking(out_no)
			os.set_blocking(out_no, False)
		if self.subprocess.stderr is not None:
			err_no = self.subprocess.stderr.fileno()
			b_err = os.get_blocking(err_no)
			os.set_blocking(err_no, False)

		try:
			in_no = self.stdin.fileno()
			b_in = os.get_blocking(in_no)
			os.set_blocking(in_no, False)
		except Exception:
			in_no = None

		try:
			self.subprocess_wait_loop()
		finally:
			# Restore old terminator
			self.logger.handlers[0].terminator = previous_val

			# Restore blocking state
			if self.subprocess.stdout is not None:
				os.set_blocking(out_no, b_out)
			if self.subprocess.stderr is not None:
				os.set_blocking(err_no, b_err)
			if in_no is not None:
				os.set_blocking(in_no, b_in)

			# Close streams
			if self.subprocess.stdin is not None: self.subprocess.stdin.close()
			if self.subprocess.stdout is not None: self.subprocess.stdout.close()
			if self.subprocess.stderr is not None: self.subprocess.stderr.close()

		# Post execution
		log.info(f"Returned code: {self.subprocess.returncode} after {round(self.exec_time * 1000)} ms")

		if self.throws and self.subprocess.returncode != 0:
			raise MakepieException(f"Command returned error code {self.subprocess.returncode}")

	def run(self):
		# Not implemented for windows
		if os.name == "nt":
			raise MakepieException("Shell commands are not yet implemented on Windows")

		self.subprocess = Popen(
			self.cmd,
			shell=True,
			stdin=PIPE if not self.tty else self.stdin,
			stdout=PIPE if self.use_pipes else sys.stdout,
			stderr=PIPE if self.use_pipes else sys.stderr,
			env=self.env
		)

		try:
			self._run()
		except Exception as e:
			self.subprocess.kill()
			self.subprocess.wait()
			raise e

	def results(self):
		if not self.use_pipes:
			return (self.subprocess.returncode, None, None)
		return (self.subprocess.returncode, self.stdout.getvalue(), self.stderr.getvalue())

def sh(
	cmd: str,
	logger: logging.Logger = applog,
	env=os.environ,
	quiet=False,
	timeout: float=None,
	throws: bool=True,
	use_pipes: bool=False,
	stdin=sys.stdin,
):
	cmd: ShellCommand = ShellCommand(cmd, logger, env, quiet, timeout, throws, use_pipes, stdin)
	cmd.run()
	return cmd
