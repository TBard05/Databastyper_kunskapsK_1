import redis
import pandas as pd
import json
import qrcode

PWD = open("Databastyper/Kunskapkontroll_1/Redis/redis.pwd", "r").read().strip()
r = redis.Redis("redis-15234.crce175.eu-north-1-1.ec2.redns.redis-cloud.com", 15234, password=PWD, decode_responses=True)

df = pd.read_csv("Databastyper\Kunskapkontroll_1\Redis\orders.csv", index_col=False, encoding="utf")
df.head()

df.index = pd.Index(pd.util.hash_pandas_object(df))
df.head()

#trying to locate the problem with converion from null vaulues
print(df.isnull().sum())
df.dropna(inplace=True) 
print(df.isnull().sum())
r.ping

data = json.loads(df.to_json(orient="index",force_ascii=False))
data

for k, v in data.items():
    r.hset(k, mapping=v)

p = r.hgetall(list(data.keys())[5])

qrcode.make(list(data.keys())[5])

for idx in df.index:
    qr = qrcode.make(idx)
    qr.save(f"Databastyper\Kunskapkontroll_1\Redis\qr_codes{idx}.png")