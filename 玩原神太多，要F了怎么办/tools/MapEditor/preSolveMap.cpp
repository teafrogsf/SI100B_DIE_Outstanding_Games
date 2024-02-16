#include<bits/stdc++.h>
using namespace std;
char ch;
signed main()
{
	freopen("item_map_in_code.txt","r",stdin);
	freopen("item_map.txt","w",stdout);
	ch=getchar();
	bool space=false;
	while(ch!=EOF) {
		if(ch=='[') {
			space=true;
		}
		else if(ch==']') {
			space=false;
			cout<<endl;
		}
		else if(isdigit(ch)) {
			cout<<ch; 
		}
		else if(ch==','&&space) {
			cout<<" ";
		}
		ch=getchar();
	}
	return 0;
}
