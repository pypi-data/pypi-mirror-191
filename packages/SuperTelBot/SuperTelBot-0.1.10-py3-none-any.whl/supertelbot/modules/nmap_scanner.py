from ipaddress import IPv4Network
import nmap


class Scanner:

    def __init__(self, target, ports="0-1024"):
        try:
            self.target = [str(ip) for ip in IPv4Network(target)]
        except Exception:
            self.target = [target]
        self.ports = ports
        self.scanner = nmap.PortScanner()
        self.results = dict()

    def scan(self):
        for ip in self.target:
            self.scanner.scan(ip, self.ports)
            hostnames = []
            for hostname in self.scanner[ip].get("hostnames"):
                if hostname.get("name") != ip:
                    hostnames.append(hostname.get("name"))
            open_ports = []
            for open_port, value in self.scanner[ip].get("tcp").items():
                if value.get("state", "closed") == "open":
                    open_ports.append(open_port)
            mac = self.scanner[ip].get("addresses").get("mac")
            brand = self.scanner[ip].get("vendor").get(mac)
            self.results[ip] = dict(mac=mac,
                                    ports=open_ports,
                                    brand=brand,
                                    hostnames=hostnames)
        return self.results

    @staticmethod
    def parse_result(result, port_range):
        api_save = list()
        bot_send = list()
        for ip, ip_data in result.items():
            result_json = dict(ip=ip)
            result_msg = """Scan result:"""
            result_msg += f"""\n\t\t*Target ip:* {ip}"""
            if ip_data.get('hostnames'):
                result_json["hostnames"] = ip_data.get('hostnames')
                result_msg += f"""\n\t\t*Hostnames:* {', '.join(ip_data.get('hostnames'))}"""
            if ip_data.get('ports'):
                result_json["open_ports"] = ip_data.get('ports')
                result_msg += f"""\n\t\t*Open ports ({port_range}):* {', '.join([str(port) for port in ip_data.get('ports')])}"""
            if ip_data.get('mac'):
                result_json["mac"] = ip_data.get('mac')
                result_msg += f"""\n\t\t*Mac:* {ip_data.get('mac')}"""
            if ip_data.get('brand'):
                result_json["brand"] = ip_data.get('brand')
                result_msg += f"""\n\t\t*Brand:* {ip_data.get('brand')}"""
            api_save.append(result_json)
            bot_send.append(result_msg)
        return api_save, bot_send
