import dns.resolver

class DNSHelper():
    def dns_zone_transfer(self, target):
        ns = dns.resolver.resolve(target, 'NS')
        for server in ns:
            print("[*] Found NS: {}".format(server))
            ip_answer = dns.resolver.resolve(server.target, 'A')
            for ip in ip_answer:
                print("[*] IP for {} is {}".format(server, ip))
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ip), address))
                    for host in zone:
                        print("[*] Found Host: {}".format(host))
                except Exception as e:
                    print("[!] NS {} refused zone transfer!".format(server))
                    continue

    def records(self, target):
        records = [
            {
                "name": "MX",
                "decription": "Directs mail to an email server"
            }, 
            {
                "name": "A",
                "decription": "Record that holds the IP address of a domain"
            },
            {
                "name": "AAAA",
                "decription": "Record that contains the IPv6 address for a domain"
            }, 
            {
                "name": "NS",
                "decription": "Stores the name server for a DNS entry"
            },
            {
                "name": "TXT",
                "decription": "Lets an admin store text notes in the record"
            }, 
        ]

        for rec in records:
            print("[*] Processing {}: {}".format(rec["name"], rec["decription"]))
            try:
                answers = dns.resolver.resolve(target, rec["name"])
                for note in answers:
                    print('[*] -> ', note.to_text())
            except Exception as ex:
                print(f"[!] Exception: {ex}")
                
    def scan(self, target):
        try:
            print("[*] DNS Zone transfer check:")
            self.dns_zone_transfer(target)
        except Exception as ex:
            print(f"[!] Exception: {ex}")

        print("[*] DNS records processing")
        self.records(target)
            
        