# 实现 HTTP1.0

class HTTPRequestHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_request(self):
        # 处理 HTTP 请求的逻辑
        # ...

        # 发送响应数据到客户端
        # ...

        self.client_socket.close()