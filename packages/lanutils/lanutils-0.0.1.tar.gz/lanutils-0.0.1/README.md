# lanutils
Small package to probe ip addresses and ports on a local network <br>
Install with:<br>
<pre>
pip install lanutils
</pre>
<br>
Usage (assuming your local ip is 10.0.0.10 with prefix 24, you're connected via ethernet, you have a http server running on port 8000, and there are a few other devices on your network):
<pre>
>>> from lanutils import lanutils
>>> lanutils.get_myip()
>>> [("10.0.0.10", 24, "Ethernet")]
>>> lanutils.ip_is_alive("10.0.0.10")
>>> True
>>> lanutils.ip_is_alive("10.0.0.11")
>>> False
>>> lanutils.enumerate_devices()
>>> ["10.0.0.7", "10.0.0.10", "10.0.0.133", "10.0.0.187"]
>>> lanutils.port_is_open("10.0.0.10", 8000)
>>> True
>>> lanutils.scan_ports("10.0.0.10", (7990, 8010))
>>> [8000]
>>> lanutils.get_available_port("10.0.0.10", (8000, 8001))
>>> 8001
</pre>