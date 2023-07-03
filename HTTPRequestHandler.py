import socket
import os
import subprocess
# 实现 HTTP1.0

class HTTPRequestHandler:
    def __init__(self, client_socket):
        # 处理的socket
        self.client_socket = client_socket
        # 超时时间
        self.timeout=10
        # 处理http请求相关信息
        self.msg=None
        self.status_code=-1
        self.file_handle=None
        self.subproc=None

    # 释放本次连接的所有相关资源
    def release_resource(self):
        # 文件句柄
        if (self.file_handle!=None):
            self.file_handle.close()
        # socket 套接字
        if(self.client_socket!=None):
            try:
                # 通知关闭双方的套接字连接
                self.client_socket.shutdown(socket.SHUT_RDWR)
                # 关闭套接字
                self.client_socket.close()
            except Exception as e:
                print("socket close error:",e)
        
    
    # 错误对应的响应构造
    def build_error_response(self,isHead=False):
        code=self.status_code
        if (code==400):
            content=b'HTTP/1.0 400 Bad Request\r\nContent-Type: text/html;charset=utf-8\r\n'
            file_path='400.html'
        elif (code==404):
            content= b"HTTP/1.0 404 Not Found\r\nContent-Type: text/html;charset=utf-8\r\n"
            file_path='404.html'
        elif (code==403):
            content=b"HTTP/1.0 403 Forbidden\r\nContent-Type: text/html;charset=utf-8\r\n"
            file_path='403.html'
        # response header
        content+=b'\r\n'
        self.client_socket.sendall(content)

        # response body
        # 发送对应的错误提示页面
        if (not isHead):
            with open(file_path,'rb') as file:
                self.file_handle=file
                for line in file:
                    self.client_socket.sendall(line)

        

            
    def handle_get(self,file_path):
        #print("enter GET")
        if(os.path.isfile(file_path)):
            self.status_code=200
            # 需要区分css和html文件，设置正确的content-type
            suffix=(file_path.split('.'))[-1].encode()
            # response header
            content= b"HTTP/1.0 200 OK\r\nContent-Type: text/"+suffix+b";charset=utf-8\r\n"
            content+=b'\r\n'
            self.client_socket.sendall(content)
            # response body~
            with open(file_path,'rb') as file:
                self.file_handle=file
                for line in file:
                    #print(line)
                    self.client_socket.sendall(line)
        else:
            self.status_code=404
            self.build_error_response()

    def handle_post(self,file_path,args):
        cmd = ['python', file_path, args]
        self.subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.subproc.wait()
        if(self.subproc.poll()==2):
            self.status_code=403
            self.build_error_response()
        else:
            self.status_code=200
            content= b"HTTP/1.0 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
            content+=b'\r\n'
            content+=self.subproc.stdout.read()
            self.client_socket.sendall(content)



    def handle_head(self,file_path):
        if(os.path.isfile(file_path)):
            self.status_code=200
            # response header
            content= b"HTTP/1.0 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
            content+=b'\r\n'
            self.client_socket.sendall(content)
        else:
            self.status_code=404
            self.build_error_response(isHead=True)
    # 解析http请求函数
    def handle_request(self):
        # 设置超时时间，避免处理时间过长拖慢服务性能
        self.client_socket.settimeout(self.timeout);
        try:
            # 处理 HTTP 请求的逻辑
            # 获取request数据
            request_data=b''
            while True:
                chunk=self.client_socket.recv(1024)
                if not chunk:
                    break
                request_data+=chunk
                # 检查结束标志
                if b'\r\n\r\n' in request_data:
                    break
            # 解析请求
            # 解码并按行拆分
            self.msg=request_data.decode('utf-8').split('\r\n')
            #print(self.msg )
            # 先判断请求长度非空
            if(self.msg):
                # # 解析header的键值对
                # for line in self.msg[1:]:
                #     if line.strip():
                #         key,value=line.split(':',1)
                #         self.header[key]=value

                # 解析首行的request line
                request_line=self.msg[0].split()
                #print(request_line )
                if(len(request_line)<2):
                    raise ValueError("incorret request line")
                # 获得url和method
                method=request_line[0]
                url=request_line[1]
              
                target_file_path=None
                # 解析目标文件路径
                if(url=="/"):
                    target_file_path='index.html'
                else:
                    # 略去首个"/"
                    target_file_path=url[1:]
                #print("file:",target_file_path)
                # 按照method不同，进行处理
                if(method=='GET'):
                    self.handle_get(target_file_path)
                elif(method=="POST"):
                    # msg的最后一个元素(即body)装载参数
                    self.handle_post(target_file_path,self.msg[-1])
                elif(method=="HEAD"):
                    self.handle_head(target_file_path)
                else:
                    self.status_code=400
                    self.build_error_response()
            else:
                raise ValueError("blank request")
        except socket.timeout:
            print('error: process timeout')
        except ValueError as e:
            print("error: ",str(e))
        finally:
            # 发送完毕，清理资源    
            self.release_resource()