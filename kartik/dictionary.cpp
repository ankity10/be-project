#include <iostream>
#include<stdio.h>
#include<string.h>
using namespace std;

class node
{
public:
	string mng;
    	string w;
	node *left;
	node *right;
};
class dictionary
{
	node *top;
	node *temp;
public:
	dictionary();
	int check(string,string);
	void insert();
	void search();
	void display();
	void disp(node *t);
	

};

dictionary::dictionary()
{
	top=NULL;
}

void dictionary::display()
{
	disp(temp);
}

void dictionary::disp(node *t)
{
	if(t==NULL)
		return;
	disp(t->left);
	cout<<"Returned";
	cout<<"Word :"<<t->w<<endl;
	cout<<"Meaning :"<<t->mng<<endl;
	disp(t->right);	
}


void dictionary::search()
{
	string sea;
	cout<<"Enter the word you want to search :";
	cin>>sea;
	temp=top;
	int flag;
	flag=check(sea,temp->w);
	while(temp!=NULL)
	{
		flag=check(sea,temp->w);
		if(flag==0)
		{
			cout<<"\nWord :"<<temp->w;
			cout<<"\nMeaning :"<<temp->mng;
			break;
		}
		else if(flag==-1)
		{
			cout<<"****left";
			temp=temp->left;
		}
		else if(flag==1)
		{
			cout<<"****Right";
			temp=temp->right;
		}
	}
	if(flag!=0)
		cout<<"Word not found...";
	temp=top;
}

void dictionary::insert()
{
	temp=new node();
	cout<<"Enter the word you want to insert :";
	cin>>temp->w;
	cout<<endl;
	cout<<"Enter its meaning :";
	cin>>temp->mng;
	temp->left=NULL;
	temp->right=NULL;
	if (top==NULL)
	{
		top=temp;
		top->left=NULL;
		top->right=NULL;
	}
	else
	{
		node *temp2=top;
		int flag;
		while(temp2->left!=NULL || temp2->right!=NULL)
		{
			flag=check(temp->w,temp2->w);
			if(flag==-1)
			{
				temp2=temp2->left;
			}
			else if(flag==1)
			{
				temp2=temp2->right;
			}
		}
		flag=check(temp->w,temp2->w);
		if(flag==-1)
		{
			temp2->left=temp;
		}
		else if(flag==1)
		{
			temp2->right=temp;
		}
	}
	temp=top;
}

int dictionary::check(string a,string b)
{
	if(a<b)
		return -1;
	else if(a>b)
		return 1;
	else if(a==b	)
		return 0;
}

int main()
{
    dictionary a;
    int x;
    while(x!=5)
    {
        cout<<"\n1.Insert word\n2.Search word\n3.Display all words\n4.Exit\nSelect you choice :";
        cin>>x;
        switch(x)
        {
		case 1: a.insert();
			break;
		case 2: a.search();
		    	break;
		case 3:	a.display();
			break;		 
		case 4: break;
		default:cout<<"Please enter a valid choice...";
		    break;
        }
    }
	return 0;
}
