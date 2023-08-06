U='<h'
T=len
L=bytes
K=int
A=list
F=''
C='utf-8'
B=str
from Cryptodome.Random import get_random_bytes as I
from Cryptodome.Cipher import AES as D,PKCS1_v1_5 as O
from nacl.public import PublicKey as P,SealedBox as Q
from Cryptodome.PublicKey import RSA
from Cryptodome import Random as R
from typing import Union
from uuid import UUID as E
import base64 as G,datetime as H,struct as J,io,time,datetime as H,random as M,string as N,binascii as S
class V:
	def __init__(A):A.defkey1=F;A.pkey1=F;A.defkey2=F;A.pkey2=F
	def _encpw(X,id,key,password):E=I(32);F=I(12);P=G.b64decode(key);Q=RSA.import_key(P);R=O.new(Q);H=R.encrypt(E);M=D.new(E,D.MODE_GCM,nonce=F);N=K(time.time());M.update(B(N).encode(C));S,V=M.encrypt_and_digest(password.encode(C));A=io.BytesIO();A.write(L([1,K(id)]));A.write(F);A.write(J.pack(U,T(H)));A.write(H);A.write(V);A.write(S);W=G.b64encode(A.getvalue()).decode(C);return f"#PWD_INSTAGRAM:4:{N}:{W}"
	def _encpwd(Z,key_id,pub_key,password,version=10):F=R.get_random_bytes(32);O=L([0]*12);I=K(H.datetime.now().timestamp());M=D.new(F,D.MODE_GCM,nonce=O,mac_len=16);M.update(B(I).encode(C));V,W=M.encrypt_and_digest(password.encode(C));X=S.unhexlify(pub_key);Y=Q(P(X));N=Y.encrypt(F);E=L([1,key_id,*A(J.pack(U,T(N))),*A(N),*A(W),*A(V)]);E=G.b64encode(E).decode(C);return f"#PWD_INSTAGRAM_BROWSER:{version}:{I}:{E}"
	def _generate(D,seed):A=M.Random(seed+B(H.date.today()));C=B(E(int=A.getrandbits(128),version=4));G=B(E(int=A.getrandbits(128),version=4));id=f"android-{F.join(A.choices(N.hexdigits,k=16))}".lower();I=B(E(int=A.getrandbits(128),version=4));J=B(E(int=A.getrandbits(128),version=4));K=D._jazoest(C);return id,C,G,I,J,K
	def _jazoest(A,phone_id):return f"2{sum((ord(A)for A in phone_id))}"