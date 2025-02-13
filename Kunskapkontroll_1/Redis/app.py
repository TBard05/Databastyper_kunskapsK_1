import redis
import pandas as pd
import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

PWD = open("Databastyper/Kunskapkontroll_1/Redis/redis.pwd", "r").read().strip()
r = redis.Redis("redis-15234.crce175.eu-north-1-1.ec2.redns.redis-cloud.com", 15234, password=PWD, decode_responses=True)

qr_data = qrcode_scanner(key="qr")

# Can add a sound but with the current liberary the sound i bult in and can not be removed byt the library itself
# meaning that you hear the standard sound and then the sound you added. Read that you can mute the sound using
# javascript but it seemd to mutch work for a little gimmick
 
# if qr_data:
#     st.success(f"QR-kod skannad: {qr_data}")
# st.audio("Databastyper/Kunskapkontroll_1/Redis/pew.mp3", autoplay=True)

if qr_data:
    p = r.hgetall(str(qr_data))
    df = pd.DataFrame(p.values(), index=p.keys())
    st.dataframe(df)
    

    
