

virtualenv --python=3.11 venv
source venv/bin/activate
pip install -r requirements.txt

executar o python no modo interativo:

from question\_1 import Q1
from question\_2 import Q2
from question\_3 import Q3

q1=Q1()
q1.get\_summary()
q1.get\_data()

q2= Q2()

q2.get\_summary()
q2.get\_metrics()
q2.get\_inactive()
q2.get\_monthly\_sales()

q3 = Q3() 
