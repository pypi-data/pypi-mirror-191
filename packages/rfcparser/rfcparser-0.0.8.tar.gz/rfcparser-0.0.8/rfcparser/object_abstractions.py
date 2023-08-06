import ipaddress
from datetime import datetime, timedelta


def default_path(uri):
    uri_path = uri.path

    if not uri_path or uri_path[0] != "/":
        return "/"
    if uri_path.count("/") == 1:
        return "/"
    assert len("".join(uri_path.split("/")[:-1]))

    if uri_path.endswith("/"):
        return uri_path[:-1]
    return uri_path


def path_matches(request_path, cookie_path):
    if request_path == "":
        request_path = "/"

    if request_path == cookie_path:
        return True

    if len(request_path) > len(cookie_path) and request_path.startswith(cookie_path):
        if cookie_path[-1] == "/":
            #   The cookie-path is a prefix of the request-path, and the last
            # 	character of the cookie-path is %x2F ("/").
            return True
        if request_path[0] == "/":
            #   The cookie-path is a prefix of the request-path, and the
            #   first character of the request-path that is not included in
            #   the cookie-path is a %x2F ("/") character.
            return True
    return False


def domain_matches(string: str, domain_string: str) -> bool:
    string = string.lower()
    domain_string = domain_string.lower()
    try:
        ipaddress.ip_address(string)
        is_host = False
    except ValueError:
        is_host = True
    return string == domain_string or (
        string.endswith(domain_string)
        and string[-(len(domain_string) + 1)] == "."
        and is_host
    )


class Cookie6265:
    def __init__(self, key, value, uri, attrs):
        self.key = key
        self.value = value
        self.creation_time = self.last_access_time = datetime.now()
        self.persistent_flag = False
        self.expiry_time = None
        self.domain = attrs.get("Domain", "")

        if self.domain:
            if not domain_matches(uri.get_domain(), self.domain):
                raise ValueError()
            else:
                self.host_only_flag = False
        else:
            self.host_only_flag = True
            self.domain = uri.get_domain()

        max_age = attrs.get("Max-Age", None)
        if max_age is not None:
            self.persistent_flag = True
            time = datetime.now()
            if max_age > 0:
                time += timedelta(seconds=max_age)
            self.expiry_time = time
        else:
            expires = attrs.get("Expires", None)
            if expires:
                self.persistent_flag = True
                self.expiry_time = expires
            else:
                self.persistent_flag = False
                self.expiry_time = datetime.now()

        path = attrs.get("Path", None)
        if path:
            self.path = path
        else:
            self.path = default_path(uri)
        self.secure_only_flag = "Secure" in attrs
        self.http_only_flag = "HttpOnly" in attrs

    def __str__(self):
        return f"{self.key}={self.value}"

    def __repr__(self):
        return f"<SetCookie6265 {str(self)}"


class Uri3986:
    def __init__(self, scheme, ip, port, host, userinfo, path, query, fragment):
        self.scheme = scheme
        self.ip = ip
        self.port = port
        self.host = host
        self.userinfo = userinfo
        self._path = path
        self.query = query
        self.fragment = fragment

    def updated_relative_ref(self, value):
        if value.startswith("//"):
            value = f"{self.scheme}:{value}"
        else:
            userinfo = f"{self.userinfo}@" if self.userinfo else ""
            hostname = self.ip or ".".join(self.host)
            port = f":{self.port}" if self.port else ""
            value = f"{self.scheme}://{userinfo}{hostname}{port}{value}"
        return value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, newvalue):
        if newvalue and not newvalue.startswith("/"):
            newvalue = "/" + newvalue
        self._path = newvalue

    def get_domain(self):
        if self.ip:
            return self.ip
        return ".".join(self.host)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError()

        return all(
            (
                self.scheme == other.scheme,
                self.ip == other.ip,
                self.port == other.port,
                self.host == other.host,
                self.userinfo == other.userinfo,
                self.path == other.path,
                self.query == other.query,
                self.fragment == other.fragment,
            )
        )

    def __str__(self):
        hostname = self.ip or ".".join(self.host)
        port = f":{self.port}" if self.port else ""
        path = self.path if self.path else "/"
        userinfo = f"{self.userinfo}@" if self.userinfo else ""
        fragment = f"#{self.fragment}" if self.fragment else ""
        attrs = (
            ("?" + "&".join([f"{key}={value}" for key, value in self.query.items()]))
            if self.query
            else ""
        )
        return f"{self.scheme}://{userinfo}{hostname}{port}{path}{attrs}{fragment}"

    def __repr__(self):
        return f"<Uri3986 {str(self)}>"
