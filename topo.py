from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        # Hostlar
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Switchler
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Hostları switchlere bağla
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        # Switchler arası bağlantılar (birden fazla yol için)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s1, s3)  # Alternatif yol
        self.addLink(s2, s4)  # Alternatif yol

# Mininet'e topolojiyi tanıt
topos = {'mytopo': (lambda: MyTopo())}

