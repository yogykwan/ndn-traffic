import Queue

client_conf = "a5000_0.8"
attacker_conf = "cpa_ifa"
fc = open("../conf/" + client_conf + ".conf", "r")
fa = open("../conf/" + attacker_conf + ".conf", "r")
client_traffic = fc.read().split(" ")
attacker_traffic = fa.read().split(" ")


client_rate = 1000
attacker_rate = 500
router_log = client_conf + "_" + attacker_conf + "_" + str(attacker_rate)
fr = open("../log/" + router_log + ".csv", 'w')

cs_length = 200
pit_length = 1000
hit = miss = attack = 0
cs = set()
q = Queue.Queue()


def log(n):
    global hit, miss, attack
    hit_rate = 1.0 * hit / client_rate
    pit = 15.3 / 1000 * (miss + attack)
    if n >= 0:
        pit += attacker_rate
    if n > 0:
        pit += attacker_rate
        pit = pit_length
    if pit > pit_length:
        pit = pit_length

    rtt = (15.7 * hit + 31 * miss + 4000 * (client_rate - hit - miss)) / client_rate

    line = str(hit) + "," + str(miss) + "," + str(attack) + "," +\
           str(hit_rate) + "," + str(min(pit_length,int(pit))) + "," + str(rtt) + ",\n"
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
    log(-1)

for i in range(30):
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

        if j & 1:
            x = attacker_traffic[attacker_cnt]
            attacker_cnt += 1
            attack += 1

            if x not in cs:
                while len(cs) >= cs_length:
                    cs.remove(q.get())
                q.put(x)
                cs.add(x)
    log(i - 100)

for i in range(30):
    for j in range(client_rate):
        if j & 1:
            x = client_traffic[client_cnt]
            client_cnt += 2
            if x in cs:
                hit += 1
            else:
                miss += 1
                while len(cs) >= cs_length:
                    cs.remove(q.get())
                q.put(x)
                cs.add(x)

        if j & 1:
            x = attacker_traffic[attacker_cnt]
            attacker_cnt += 1
            attack += 1

    log(i)
