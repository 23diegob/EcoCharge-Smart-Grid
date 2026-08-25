import streamlit as st
from dataclasses import dataclass
import pandas as pd

st.set_page_config(page_title="EcoCharge Smart Grid", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")
REDE_MAX_KW=50.0
TARIFA_KWH=1.15

@dataclass
class Veiculo:
    nome:str; bateria:float; capacidade_kwh:float; urgente:bool; potencia_max_kw:float
    potencia_atual_kw:float=0.0; energia_consumida_kwh:float=0.0; custo:float=0.0; status:str="Conectado"

if "veiculos" not in st.session_state:
    st.session_state.veiculos=[Veiculo("ECO-01",72,60,False,22),Veiculo("ECO-02",10,55,True,30),Veiculo("ECO-03",46,70,False,22)]
if "solar" not in st.session_state: st.session_state.solar=8.0
if "msg" not in st.session_state: st.session_state.msg="Central inteligente online. Monitoramento ativo."
if "pagos" not in st.session_state: st.session_state.pagos=set()

def score(v): return (100-v.bateria)+(120 if v.urgente else 0)

def redistribuir():
    ativos=[v for v in st.session_state.veiculos if v.status=="Conectado" and v.bateria<100]
    for v in st.session_state.veiculos: v.potencia_atual_kw=0
    if not ativos:return
    disp=REDE_MAX_KW+st.session_state.solar
    ativos=sorted(ativos,key=score,reverse=True)
    base=min(8.0,disp/len(ativos))
    for v in ativos:
        x=min(base,v.potencia_max_kw);v.potencia_atual_kw=x;disp-=x
    for grupo in ([v for v in ativos if v.urgente],[v for v in ativos if not v.urgente]):
        for v in grupo:
            if disp<=0:break
            x=min(v.potencia_max_kw-v.potencia_atual_kw,disp);v.potencia_atual_kw+=x;disp-=x

def avancar(n):
    for _ in range(n):
        redistribuir()
        for v in st.session_state.veiculos:
            if v.status!="Conectado" or v.potencia_atual_kw<=0:continue
            e=min(v.potencia_atual_kw/60,v.capacidade_kwh*(100-v.bateria)/100)
            v.energia_consumida_kwh+=e;v.custo=v.energia_consumida_kwh*TARIFA_KWH
            v.bateria=min(100,v.bateria+(e/v.capacidade_kwh)*100)
            if v.bateria>=99.999:v.bateria=100;v.status="Concluído"
    redistribuir();st.session_state.msg=f"IA recalculou a rede após {n} minuto(s) de simulação."

def finalizar(i):
    v=st.session_state.veiculos[i];v.status="Finalizado";v.potencia_atual_kw=0
    redistribuir();st.session_state.msg=f"{v.nome} finalizado • Total R$ {v.custo:.2f}"

redistribuir()

st.markdown("""
<style>
html,body,[class*="css"]{font-family:Arial,sans-serif}.stApp{background:radial-gradient(circle at 8% 0%,#062238 0,transparent 28%),radial-gradient(circle at 92% 4%,#06251a 0,transparent 30%),#04070a;color:#edf7f5}
header[data-testid="stHeader"]{background:transparent}#MainMenu,footer,[data-testid="stToolbar"]{visibility:hidden}.block-container{padding-top:1.2rem;max-width:1450px}
.head{display:flex;justify-content:space-between;align-items:center;padding:20px 24px;background:linear-gradient(120deg,#09121a,#07110d);border:1px solid #18303a;border-radius:22px}
.brand{font-size:29px;font-weight:900;letter-spacing:-1px}.eco{color:#32d583}.charge{color:#f2f7f6}.blue{color:#38b6ff}.sub{font-size:11px;color:#718993;letter-spacing:2.5px;margin-top:3px}.online{color:#6ee7a7;border:1px solid #1d6844;background:#092118;padding:9px 13px;border-radius:99px;font-size:11px}
.hero{margin-top:16px;padding:28px;background:linear-gradient(135deg,#0a151e,#07100d);border:1px solid #18303a;border-radius:22px}.hero h1{font-size:38px;line-height:1.05;margin:4px 0 10px}.hero p{color:#8196a0;margin:0}.section{color:#42baff;font-size:11px;font-weight:800;letter-spacing:2px;margin:25px 0 9px}
.card{background:#081017;border:1px solid #172b35;border-radius:18px;padding:18px;min-height:105px}.label{color:#6e838d;font-size:10px;letter-spacing:1.2px}.value{font-size:28px;font-weight:900;margin-top:8px}.green{color:#4ade98}
.vehicle{background:linear-gradient(145deg,#09121a,#070c11);border:1px solid #182b35;border-radius:20px;padding:19px;margin:10px 0}.vtop{display:flex;justify-content:space-between}.vname{font-size:18px;font-weight:800}.badge{font-size:10px;font-weight:800;padding:6px 9px;border-radius:99px}.urgent{color:#ffc46b;background:#291b09;border:1px solid #69471b}.normal{color:#6dcaff;background:#082035;border:1px solid #164c70}.bar{height:8px;background:#15232b;border-radius:20px;overflow:hidden;margin:11px 0 6px}.fill{height:100%;background:linear-gradient(90deg,#199cff,#38db8a)}.mini{font-size:11px;color:#70858e}.num{font-size:19px;font-weight:850}.ok,.hot{padding:13px 16px;border-radius:14px;margin-top:12px}.ok{background:#071c14;border:1px solid #185d3e;color:#77e6ad}.hot{background:#221808;border:1px solid #68471a;color:#ffc36a}
div.stButton>button{min-height:44px;border-radius:13px;border:1px solid #1b465c;background:#091923;color:#e7f8ff;font-weight:800}div.stButton>button:hover{border-color:#37b9ff;background:#0b2634}
[data-testid="stExpander"]{background:#071016;border:1px solid #172b35;border-radius:16px}[data-testid="stDataFrame"]{border:1px solid #172b35;border-radius:14px;overflow:hidden}
</style>
""",unsafe_allow_html=True)

col_logo, col_status = st.columns([5, 1])

with col_logo:
    st.image("logo.png", width=220)

with col_status:
    st.markdown(
        '<div class="online">● SISTEMA ONLINE</div>',
        unsafe_allow_html=True
    )
st.markdown('<div class="hero"><div class="section" style="margin:0 0 8px">CENTRAL DE OPERAÇÕES</div><h1>Energia distribuída com<br><span class="green">inteligência.</span></h1><p>Controle de demanda, priorização automática, geração solar e cobrança em uma única central.</p></div>',unsafe_allow_html=True)

total=sum(v.potencia_atual_kw for v in st.session_state.veiculos if v.status=="Conectado");rede=max(0,total-st.session_state.solar);uso=min(100,rede/REDE_MAX_KW*100)
st.markdown('<div class="section">VISÃO GERAL DA REDE</div>',unsafe_allow_html=True)
cs=st.columns(4)
for c,(l,v,cl) in zip(cs,[("CAPACIDADE",f"{REDE_MAX_KW:.0f} kW","blue"),("SOLAR",f"{st.session_state.solar:.1f} kW","green"),("DEMANDA",f"{total:.1f} kW","blue"),("USO DA REDE",f"{uso:.0f}%","green")]):
    c.markdown(f'<div class="card"><div class="label">{l}</div><div class="value {cl}">{v}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="hot">⚡ <b>Alta demanda:</b> priorização inteligente e redistribuição automática ativas.</div>' if uso>=90 else '<div class="ok">● <b>Operação estável:</b> rede dentro dos parâmetros seguros.</div>',unsafe_allow_html=True)

st.markdown('<div class="section">CONTROLE DA SIMULAÇÃO</div>',unsafe_allow_html=True)
a,b,c=st.columns([1,1,2])
with a:
    if st.button("▶ AVANÇAR 1 MINUTO",use_container_width=True):avancar(1);st.rerun()
with b:
    if st.button("⏩ AVANÇAR 10 MINUTOS",use_container_width=True):avancar(10);st.rerun()
with c:
    st.session_state.solar=st.slider("Geração solar simulada (kW)",0.0,20.0,float(st.session_state.solar),1.0);redistribuir()
st.caption(st.session_state.msg)

st.markdown('<div class="section">ESTAÇÕES DE RECARGA</div>',unsafe_allow_html=True)
for i,v in enumerate(st.session_state.veiculos):
    badge='<span class="badge urgent">PRIORIDADE ALTA</span>' if v.urgente else '<span class="badge normal">PRIORIDADE NORMAL</span>'
    st.markdown(f'<div class="vehicle"><div class="vtop"><div class="vname">⚡ {v.nome}</div>{badge}</div><div class="bar"><div class="fill" style="width:{min(100,v.bateria)}%"></div></div><div class="mini">BATERIA • {v.bateria:.1f}% &nbsp; | &nbsp; STATUS • {v.status}</div></div>',unsafe_allow_html=True)
    c1,c2,c3,c4,c5=st.columns([1,1,1,1,1.1])
    for c,l,val in [(c1,"POTÊNCIA",f"{v.potencia_atual_kw:.1f} kW"),(c2,"CONSUMO",f"{v.energia_consumida_kwh:.2f} kWh"),(c3,"TARIFA",f"R$ {TARIFA_KWH:.2f}"),(c4,"TOTAL",f"R$ {v.custo:.2f}")]:
        c.markdown(f'<div class="mini">{l}</div><div class="num">{val}</div>',unsafe_allow_html=True)
    with c5:
        if v.status=="Conectado":
            if st.button("FINALIZAR",key=f"f{i}",use_container_width=True):finalizar(i);st.rerun()
        elif i not in st.session_state.pagos:
            if st.button("PAGAR",key=f"p{i}",use_container_width=True):st.session_state.pagos.add(i);st.session_state.msg=f"Pagamento de {v.nome} aprovado.";st.rerun()
        else: st.success("Pagamento aprovado")

with st.expander("＋ CONECTAR NOVO VEÍCULO"):
    with st.form("novo"):
        c1,c2,c3=st.columns(3);nome=c1.text_input("Identificação","ECO-04");bat=c2.slider("Bateria (%)",1,99,25);urg=c3.checkbox("Prioridade urgente")
        c4,c5=st.columns(2);cap=c4.number_input("Capacidade (kWh)",30.,120.,60.,5.);pmax=c5.number_input("Potência máxima (kW)",5.,50.,22.,1.)
        if st.form_submit_button("CONECTAR À REDE"):
            st.session_state.veiculos.append(Veiculo(nome,float(bat),float(cap),urg,float(pmax)));redistribuir();st.session_state.msg=f"{nome} conectado.";st.rerun()

st.markdown('<div class="section">TELEMETRIA DA REDE</div>',unsafe_allow_html=True)
df=pd.DataFrame([{"Estação":v.nome,"Bateria":f"{v.bateria:.1f}%","Prioridade":"Alta" if v.urgente else "Normal","Potência":f"{v.potencia_atual_kw:.1f} kW","Consumo":f"{v.energia_consumida_kwh:.2f} kWh","Custo":f"R$ {v.custo:.2f}","Status":v.status} for v in st.session_state.veiculos])
st.dataframe(df,use_container_width=True,hide_index=True)
st.caption("EcoCharge Smart Grid • Protótipo acadêmico • Dados simulados para demonstração.")
