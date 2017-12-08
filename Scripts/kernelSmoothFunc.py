






cmds.getPosition()

#nPosition = new position of one particle 
def kernel( nPosition, H ): #H = 0.1
	q = ( position-nPosition )/H
	return ( 1/( PI*H*H*H ))*( 1-1.5*q*q + 0.75*q*q*q )

def gradientKernel ( nPosition, H ):
	p = position-nPosition 
	q = p/H
	if p = ( 0,0,0 ):
		return ( 1,1,1 )
	else:
		return p * ( 1 / ( PI*H*H*H * ( len(p) ) ) ) * ( -3*q + 2.25*q*q )