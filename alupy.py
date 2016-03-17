from myhdl import *
from random import randrange

def clamp(no, smallest, largest): return max(smallest, min(no, largest))
#As +,* or- may lead to values which are out of bound of number of bits so we need to clamp those values for ALU to be functional 
def alupy (a_in,b_in,out,sel,n):
	@always_comb
	def logic():
		if sel ==0 :
			out.next =~a_in
		elif sel==1 :
			out.next=a_in|b_in
		elif sel==2 :
			out.next=a_in&b_in
		elif sel==3 :
			out.next=a_in^b_in
		elif sel ==4 :
			out.next =clamp(a_in+b_in,0,2**n-1)
		elif sel==5 :
			out.next=clamp(a_in-b_in,0,2**n-1)
		elif sel==6 :
			out.next=clamp(a_in*b_in,0,2*n-1)
		elif sel==7 :
			out.next=0
	return logic

def test_bench():
	sel_display =('~','|','&','^','+','-','*','0')
	for i in range (10):
		a_in.next,sel.next,b_in.next = randrange(16), randrange(8), randrange(16)
		yield delay(10)
		print "{0:04b} {1} {2:04b} = {3:04b}".format(int(a_in),sel_display[sel],int(b_in),int(out))

out,a_in,b_in=[Signal(intbv(0)[4:]) for i in range(3) ]
sel =Signal(intbv(0)[3:])

aludesgn=alupy(a_in,b_in,out,sel,4)
alutest1= test_bench()
sim= Simulation(aludesgn,alutest1).run()
