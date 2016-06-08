MN = -999999999
MX = 999999999

arr = [0]*100002
maxtree = [0]*((1<<18)+1)
mintree = [0]*((1<<18)+1)

def min(x,y):
	if(x<y):
		return x
	return y


def max(x,y):
	if(x>y):
		return x
	return y


def minindex(i,j):
	if arr[mintree[i]]<arr[mintree[j]]:
		return i
	return j


def maxindex(i,j):
	if arr[maxtree[i]]>arr[maxtree[j]]:
		return i
	return j


def buildmax(node, start, end):			
	if start==end:
		maxtree[node]=start
	else:
		mid=(start+end)/2
		buildmax(2*node, start, mid)
		buildmax(2*node+1, mid+1, end)
		maxtree[node]=maxtree[maxindex(2*node,2*node+1)]


def updatemax(node, start, end, idx, val):
	if start==end:
		arr[idx]=val
		maxtree[node]=start
	else:
		mid=(start+end)/2
		if(start<=idx and idx<=mid):
			updatemax(2*node, start, mid, idx, val)
		else:
			updatemax(2*node+1, mid+1, end, idx, val)
		maxtree[node]=maxtree[maxindex(2*node, 2*node+1)]


def querymax(node, start, end, l, r):
	if(r<start or l>end):
		return 0
	if(l<=start and r>=end):
		return node

	mid=(start+end)/2
	lt=querymax(2*node, start, mid, l, r)
	rt=querymax(2*node+1, mid+1, end, l, r)
	return maxindex(lt,rt)


def buildmin(node, start, end):		
	if start==end:
		mintree[node]=start
	else:
		mid=(start+end)/2
		buildmin(2*node, start, mid)
		buildmin(2*node+1, mid+1, end)
		mintree[node]=mintree[minindex(2*node,2*node+1)]


def updatemin(node, start, end, idx, val):
	if start==end:
		arr[idx]=val
		mintree[node]=start
	else:
		mid=(start+end)/2
		if(start<=idx and idx<=mid):
			updatemin(2*node, start, mid, idx, val)
		else:
			updatemin(2*node+1, mid+1, end, idx, val)
		mintree[node]=mintree[minindex(2*node, 2*node+1)]


def querymin(node, start, end, l, r):
	if(r<start or l>end):
		return 0
	if(l<=start and r>=end):
		return node
	mid=(start+end)/2
	lt=querymin(2*node, start, mid, l, r)
	rt=querymin(2*node+1, mid+1, end, l, r)
	return minindex(lt,rt)



def main():
	maxtree[0]=0
	arr[0]=MN
	mintree[0]=100001
	arr[100001]=MX

	n,q = map(int,raw_input().split(' '))

	temp = map(int,raw_input().split(' '))

	arr[1:n+1] = temp[0:n]

	buildmin(1, 1, n)
	buildmax(1, 1, n)

	while q:
		q-=1
		ip = map(str,raw_input().split(' '))
		c = ip[0]
		if(c=="P"):
			idx = int(ip[1])
			val = int(ip[2])
			updatemin(1, 1, n, idx, val)
			updatemax(1, 1, n, idx, val)

		elif(c=="C"):
			l = int(ip[1])
			r = int(ip[2])
			idx1=querymax(1, 1, n, l, r)
			idx1=maxtree[idx1]
			temp=arr[idx1]
			updatemax(1, 1, n, idx1, -2222222)
			idx2=querymax(1, 1, n, l, r)
			idx2=maxtree[idx2]
			mx1=temp*arr[idx2]
			updatemax(1, 1, n, idx1, temp)

			idx1=querymin(1, 1, n, l, r)
			idx1=mintree[idx1]
			temp=arr[idx1]
			updatemin(1, 1, n, idx1, 2222222)
			idx2=querymin(1, 1, n, l, r)
			idx2=mintree[idx2]
			mx2=temp*arr[idx2]
			updatemin(1, 1, n, idx1, temp)
			print max(mx1,mx2)			

	return 0

main()