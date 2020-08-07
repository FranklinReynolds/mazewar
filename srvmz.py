import web

urls = (
    "/ping", 'ping',
    "/status", 'status',
    "/move", 'move',
    "/shoot", 'shoot'
)

class ping:
    def GET(self):
        return "PING - ACK"


class status:
    def GET(self):
        return "status - ACK"


class move:
    def POST(self):
        pargs = web.input()


class shoot:
    def POST(self):
        pargs = web.input()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
