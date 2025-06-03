sudo mn --topo=mytopo --custom=topo.py --controller remote,ip=172.17.0.2 --switch ovs,protocols=OpenFlow13 --mac

sudo mn --topo=mytopo --custom=topo2.py --controller remote,ip=172.17.0.2 --switch ovs,protocols=OpenFlow13 --mac

source venv/bin/activate


sudo docker restart onos


curl "http://localhost:5000/shortest_path?src=of:0000000000000001&dst=of:0000000000000028"


uvicorn main:app --reload




