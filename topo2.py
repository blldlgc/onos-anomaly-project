from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        # 30 Host oluştur
        hosts = []
        for i in range(1, 61):
            hosts.append(self.addHost(f'h{i}'))

        # 20 Switch oluştur
        switches = []
        for i in range(1, 41):
            switches.append(self.addSwitch(f's{i}'))

        # Hostları switchlere bağla (dağıtarak)
        for idx, host in enumerate(hosts):
            switch_idx = idx % len(switches)  # Dağıtımı dengeli yap
            self.addLink(host, switches[switch_idx])

        # Switchler arası bağlantılar (omurga ağı gibi)
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])  # Lineer bağlantı

        # Ekstra bağlantılar (alternatif yollar için çapraz bağlantılar)
        for i in range(0, len(switches) - 2, 2):
            self.addLink(switches[i], switches[i + 2])

        for i in range(0, len(switches) - 3, 3):
            self.addLink(switches[i], switches[i + 3])

        # Uçtan uca bağlantılar (opsiyonel)
        self.addLink(switches[0], switches[-1])

# Mininet'e topolojiyi tanıt
topos = {'mytopo': (lambda: MyTopo())}

