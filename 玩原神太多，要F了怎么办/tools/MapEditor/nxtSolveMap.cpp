#include<bits/stdc++.h>
using namespace std;
signed main()
{
	freopen("ground_map.txt","r",stdin);
	freopen("ground_map_to_code.txt","w",stdout);
	cout<<"[[";
	char ch=getchar();
	while(ch!=EOF) {
		if(ch=='\n') {
			cout<<"],"<<endl<<"[";
		}
		else if(ch==' ') {
			cout<<",";
		}
		else {
			cout<<ch;
		}
		ch=getchar();
	}
	cout<<"]";
	return 0;
}
