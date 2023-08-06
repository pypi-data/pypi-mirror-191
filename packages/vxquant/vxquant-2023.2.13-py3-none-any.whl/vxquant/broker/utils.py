from vxutils import to_binary
from vxutils.zmqsocket import vxZMQContext
from vxsched import vxEvent


def init_socket(socket_type, settings):
    ctx = vxZMQContext().instance()
    socket_ = ctx.socket(socket_type)
    if settings["connect_mode"].lower() == "connect":
        socket_.connect(settings["addr"], settings["public_key"])
    else:
        socket_.bind(settings["addr"], settings["public_key"])
    return socket_


def frontend_reply(context, reply_event):
    with context.lock:
        context.frontend_sender.send_multipart(
            [to_binary(reply_event.channel), b"", vxEvent.pack(reply_event)]
        )


def backend_publish(context, publish_event):
    with context.lock:
        context.backend_sender.send_multipart(
            [to_binary(publish_event.channel), vxEvent.pack(publish_event)]
        )
