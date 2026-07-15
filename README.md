1. Установите awg на сервер
2. В awg_dir (по умолчанию /etc/amnezia/amneziawg) напишите awg0.base.conf и awg0.conf. Примеры:

```awg0.base.conf
[Interface]
PrivateKey = ...
Address = 10.66.0.1/16, fd66:66:66::1/64
ListenPort = 35533

Jc = 8
Jmin = 8
Jmax = 80
S1 = 71
S2 = 147
H1 = 123456789
H2 = 987654321
H3 = 112233445
H4 = 556677889

```

```client.base.conf
[Interface]
PrivateKey = {private_key}
Address = {free_ip}/32, {calculate_ipv6_from_ipv4(free_ip)}/128
DNS = 1.1.1.1, 1.0.0.1, 2606:4700:4700::1111, 2606:4700:4700::1001

Jc = 8
Jmin = 8
Jmax = 80
S1 = 71
S2 = 147
H1 = 123456789
H2 = 987654321
H3 = 112233445
H4 = 556677889

[Peer]
PublicKey = {public_key}
Endpoint = {conf["awg_endpoint"]}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```