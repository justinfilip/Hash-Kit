import json, socket, traceback

class XMinerWrapper():

    def __init__(self, host, port):

        self.host = host
        self.port = port

        try:

            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.connection.settimeout(3)

        except socket.error:

            self._close()
            return b'timeout'

    def __del__(self):

        self._close()

    def _close(self):

        self.connection.close()

    def _connect(self):

        try:

            self.connection.connect((self.host, self.port))
            return ""

        except socket.error:

            self._close()
            return b'timeout'

    def _send(self, request):

        try:

            self.connection.sendall(bytes(request, "utf-8"))

        except socket.error:

            traceback.print_exc()
            raise

    def _receive(self):

        chunks = []
        chunk = 1

        try:

            while chunk:

                chunk = self.connection.recv(4096)
                chunks.append(chunk)

        except socket.error:

            traceback.print_exc()
            raise

        return b"".join(chunks)

    def issue_command(self, command, param = None):

        response = ""
        request = {"command": command}

        if param is not None:

            request.update({"parameter": param})

        try:

            connection_status = self._connect()

            if connection_status == b'timeout':

                response = b'timeout'
            
            else:
                
                self._send(json.dumps(request))
                response = self._receive()

        finally:

            self._close()

        return response