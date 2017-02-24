import Queue

client_conf = "a5000_0.8"
attacker_conf = "cpa"
fc = open("../conf/" + client_conf + ".conf", "r")
fa = open("../conf/" + attacker_conf + ".conf", "r")
client_traffic = fc.read().split(" ")
attacker_traffic = fa.read().split(" ")


client_rate = 1000
attacker_rate = 1000
router_log = client_conf + "_" + attacker_conf + "_" + str(attacker_rate)
fr = open("../log/" + router_log + ".csv", 'w')

cs_length = 200
hit = miss = attack = 0
cs = set()
q = Queue.Queue()


def log():
    global hit, miss, attack
    hit_rate = 1.0 * hit / (hit + miss)
    pit = 15.3 / 1000 * (miss + attack)
    rtt = (15.7 * hit + 31 * miss) / (hit + miss)
    line = str(hit) + "," + str(miss) + "," + str(attack) + "," +\
           str(hit_rate) + "," + str(int(pit)) + "," + str(rtt) + ",\n"
    fr.write(line)
    hit = miss = attack = 0

client_cnt = 0
attacker_cnt = 0

for i in range(30):
    for j in range(client_rate):
        x = client_traffic[client_cnt]
        client_cnt += 1
        if x in cs:
            hit += 1
        else:
            miss += 1
            while len(cs) >= cs_length :
                cs.remove(q.get())
            q.put(x)
            cs.add(x)
    log()

for i in range(60):
    for j in range(client_rate):
        x = client_traffic[client_cnt]
        client_cnt += 1
        if x in cs:
            hit += 1
        else:
            miss += 1
            while len(cs) >= cs_length:
                cs.remove(q.get())
            q.put(x)
            cs.add(x)

        if 1:
            x = attacker_traffic[attacker_cnt]
            attacker_cnt += 1
            attack += 1
            if attacker_conf is "cpa":
                if x not in cs:
                    while len(cs) >= cs_length:
                        cs.remove(q.get())
                    q.put(x)
                    cs.add(x)
    log()
