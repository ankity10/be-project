/*
		FILE STRUCTURE:

					     .svc
						   |
					  filename_repo
					/               \
				   /				 \
				-masterfile           version
				-master_head        /         \
								ver_head	  -v1
											  -v2
											  -v3
												:
												:
*/

#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>

using namespace std;

class svc
{
	private:
		int version;
		string filename;
		string path_to_prev_version;
		// char lines[20][10];
		string path_to_repo;
		string path_to_version;
		string path_to_masterfile;
		string path_to_master_head;
		string path_to_version_head;
		string path_to_current_version;
		ifstream fin_masterfile;
		ifstream fin_master_head;
		ofstream fout_masterfile;
		ofstream fout_master_head;
		ifstream fin_version_head;
		ofstream fout_version_head;
		ofstream fout_current_version;
		ifstream fin_filename;
		ifstream fin_prev_version;
		int master_head;

	public:
		svc();
		svc(string);
		svc(string, int);
		bool dirExists(const char*);
		bool fileExists(const char*);
		void initialize_all();
		void commit_ver0();
		void commit();
		int stoi(string);
		string itos(int);
};

svc::svc()
{
	cout<<"Available commands:\n\
	svc init -- Initialize svc on current directory\n\
	svc filename -- To commit the changes of file 'filename'\n\
	svc filename version -- retrieval of the 'version'th commit of file 'filename'\n";
}

int svc::stoi(string s)
{
	int sum=0;
	int p=1;
	for(int i=s.length()-1;i>=0;i--)
	{
		sum+=p*(s[i]-'0');
		p*=10;
	}
	return sum;
}

string svc::itos(int n)
{
	int p=1;
	int len=0;
	while(n/p)
	{
		len++;
		p*=10;
	}
	string s;
	s.resize(len);
	for(int i=len-1;i>=0;i--)
	{
		s[i]=n%10+'0';
		n/=10;
	}
	return s;
}


bool svc:: dirExists(const char *path)
{
    struct stat info;

    if(stat( path, &info ) != 0)
        return 0;
    else if(info.st_mode & S_IFDIR)
        return 1;
    return 0;
}

bool svc:: fileExists(const char *path)
{
    struct stat info;

    if(stat( path, &info ) != 0)
        return 0;
    else if(info.st_mode & S_IFREG)
        return 1;
    return 0;
}

void svc:: commit_ver0()
{
// Creating files	
	system(("touch "+this->path_to_masterfile).c_str());
	system(("touch "+this->path_to_master_head).c_str());
	system(("mkdir "+this->path_to_version).c_str());
	system(("touch "+this->path_to_version_head).c_str());

	this->path_to_current_version = this->path_to_version+"v0";
	
	system(("touch "+this->path_to_current_version).c_str());


//Opening files
	this->fin_masterfile.open(path_to_masterfile.c_str());
	this->fin_master_head.open(path_to_master_head.c_str());
	this->fout_masterfile.open(path_to_masterfile.c_str());
	this->fout_master_head.open(path_to_master_head.c_str());
	this->fin_version_head.open(path_to_version_head.c_str());
	this->fout_version_head.open(path_to_version_head.c_str());
	this->fin_filename.open(this->filename.c_str());

	
	this->fout_current_version.open(this->path_to_current_version.c_str());
	
	this->fout_version_head<<"0";
	this->master_head=0;

	fin_filename.seekg(0,ios::beg);
	while(!this->fin_filename.eof())
	{
		this->master_head++;
		this->fout_current_version<<this->master_head<<endl;

		string s;
		getline(this->fin_filename, s);
		this->fout_masterfile<<s;
		for(int i=s.length()+1;i<10;i++)
		{
			this->fout_masterfile<<" ";
		}
		this->fout_masterfile<<endl;
	}

	this->fout_master_head<<this->master_head;   //Updating master head

	//Closing all
	this->fin_masterfile.close();
	this->fin_master_head.close();
	this->fout_masterfile.close();
	this->fout_master_head.close();
	this->fin_version_head.close();
	this->fout_version_head.close();
	this->fin_filename.close();
	this->fout_current_version.close();
}



void svc::commit()
{
	this->fin_version_head.open(this->path_to_version_head.c_str());
	
	string version_head;
	getline(this->fin_version_head, version_head);
	this->fin_version_head.close();
	
	this->path_to_prev_version = path_to_version+"v"+version_head;
	this->fin_prev_version.open(this->path_to_prev_version.c_str());

	int ver_head = stoi(version_head);
	ver_head++;
	string current_version = "v"+itos(ver_head);
	this->fout_version_head.open(this->path_to_version_head.c_str());
	fout_version_head<<ver_head;
	this->fout_version_head.close();

	this->path_to_current_version = path_to_version+current_version;
	this->fout_current_version.open(path_to_current_version.c_str());
	this->fin_filename.open(filename.c_str());
	

	this->fout_masterfile.open(path_to_masterfile.c_str(),ios::app);
	this->fin_master_head.open(path_to_master_head.c_str());
	

	int file_last = 0;
	string last_line;
	this->fin_filename.seekg(0, ios::beg);
	while(!this->fin_filename.eof())
	{
		getline(fin_filename,last_line);
		file_last++;
	}
	fin_filename.close();
	cout<<last_line<<endl;

	fin_prev_version.seekg(0, ios::beg);
	int prev_last=0;


	while(!this->fin_prev_version.eof() )
	{
		string temp;
		getline(this->fin_prev_version, temp);
		prev_last++;
		// cout<<temp<<endl;
	}
	prev_last--;
	fin_prev_version.close();

	/*if(file_last>prev_last)  //Append the last line
	{
		cout<<"In if!!";
		
		fin_prev_version.open(path_to_prev_version.c_str());
		cout<<"Prev_last="<<prev_last<<endl;
		while(prev_last--)
		{
			string s="";
			getline(this->fin_prev_version, s);
			cout<<"s="<<s<<endl;
			fout_current_version<<s<<endl;
		}

		
		fout_masterfile<<last_line;
		for(int i=last_line.length()+1;i<10;i++)
			fout_masterfile<<" ";
		fout_masterfile<<endl;
		
		string master_head;
		fin_master_head>>master_head;
		this->master_head=stoi(master_head);
		this->master_head++;
		master_head=itos(this->master_head);

		this->fout_master_head.open(path_to_master_head.c_str());
		this->fout_master_head<<master_head;

		this->fout_current_version<<this->master_head<<endl;
	} */

	if(file_last>prev_last)   //Insert line in between
	{
		cout<<"In if!!\n";
		this->fin_masterfile.open(this->path_to_masterfile.c_str());
		this->fin_prev_version.open(this->path_to_prev_version.c_str());
		this->fin_filename.open(this->filename.c_str());

		string prev_line;
		string file_line;
		string line_no;
		string temp;
		file_line.resize(9);

		getline(fin_prev_version, line_no);
		int line = stoi(line_no);

		int file_ptr = (line-1)*10;
		fin_masterfile.seekg(file_ptr);
		getline(fin_masterfile, prev_line);

		getline(fin_filename, temp);
		for(int i=0;i<temp.length();i++)
			file_line[i]=temp[i];
		for(int i=temp.length();i<9;i++)
			file_line[i]=' ';

		
		while(file_line==prev_line && prev_last)
		{
			prev_last--;
			fout_current_version<<line_no<<endl;

			getline(fin_filename, temp);
			for(int i=0;i<temp.length();i++)
				file_line[i]=temp[i];
			for(int i=temp.length();i<9;i++)
				file_line[i]=' ';

			getline(fin_prev_version, line_no);
			line = stoi(line_no);

			int file_ptr = (line-1)*10;
			fin_masterfile.seekg(file_ptr);
			getline(fin_masterfile, prev_line);
		}		

		fout_masterfile<<file_line<<endl;   //Adding the inserted line in masterfile
		string master_no;
		fin_master_head>>master_no;
		int master_line_no = stoi(master_no);
		master_line_no++;
		fout_master_head.open(path_to_master_head.c_str());
		fout_master_head<<master_line_no;   //Updating the master_head

		fout_current_version<<master_line_no<<endl; //Adding the inserted line to current version

		while(prev_last--)
		{
			fout_current_version<<line_no<<endl;
			getline(fin_prev_version, line_no);
		}

	}
	else    //Delete one line
	{
		cout<<"In else!!\n";
		this->fin_masterfile.open(this->path_to_masterfile.c_str());
		/*
		List of files open:
		fin_prev_version
		fout_current_version
		fin_filename
		fin_masterfile
		*/
		this->fin_prev_version.open(path_to_prev_version.c_str());
		this->fin_filename.open(filename.c_str());

		string prev_line;
		string file_line;
		string line_no;
		string temp;
		file_line.resize(9);

		getline(fin_prev_version, line_no);
		int line = stoi(line_no);

		int file_ptr = (line-1)*10;
		fin_masterfile.seekg(file_ptr);
		getline(fin_masterfile, prev_line);

		if(!fin_filename.eof())
		{
			getline(fin_filename, temp);
			for(int i=0;i<temp.length();i++)
				file_line[i]=temp[i];
			for(int i=temp.length();i<9;i++)
				file_line[i]=' ';

			
			while(file_line==prev_line)
			{
				fout_current_version<<line_no<<endl;

				if(fin_filename.eof())
					break;

				getline(fin_filename, temp);
				for(int i=0;i<temp.length();i++)
					file_line[i]=temp[i];
				for(int i=temp.length();i<9;i++)
					file_line[i]=' ';

				getline(fin_prev_version, line_no);
				int line = stoi(line_no);

				int file_ptr = (line-1)*10;
				fin_masterfile.seekg(file_ptr);
				getline(fin_masterfile, prev_line);
			}


			while(!fin_prev_version.eof() )
			{
				getline(fin_prev_version, temp);
				if(!fin_prev_version.eof())
					fout_current_version<<temp<<endl;
			}
		}

		this->fin_masterfile.close();

	}
	
	
	this->fout_masterfile.close();
	this->fin_master_head.close();
	this->fout_master_head.close();	
	this->fin_filename.close();
	this->fout_current_version.close();
	this->fin_prev_version.close();

}




void svc:: initialize_all()
{
	path_to_masterfile = this->path_to_repo + "masterfile";
	path_to_master_head = this->path_to_repo + "master_head";
	path_to_version = this->path_to_repo + "version/";
	path_to_version_head = this->path_to_version + "version_head";
}


svc::svc(string filename)
{
	this->filename = filename;

	if(filename=="init")
	{
		system("mkdir .svc");
		cout<<"Initialized svc on current directory\n";
	}
	else
	{

		if(!dirExists(".svc"))   // .svc doesn't exist
		{
			cout<<"Initialization not done! Use 'svc init' to initialize the current directory\n";
		}
		else   //.svc exists
		{
			if(!fileExists(this->filename.c_str()))   // filename doesn't exist
			{
				cout<<"File "<<this->filename<<" doesn't exist!\n";
			}
			else  // filename exists
			{
				this->path_to_repo = ".svc/"+this->filename+"_repo/";
				
				if(!dirExists(this->path_to_repo.c_str()))  //repo doesn't exist!
				{
					system(("mkdir "+this->path_to_repo).c_str()); //repo created - will be a first commit to repo

					//Initializing all paths
					initialize_all();

					// call commit func
					commit_ver0();

				}

				else //repo exist - first commit is already done
				{
					initialize_all();
					commit();	
				}
			}
		}
	}
}




int main(int argc, char const *argv[])
{
	ios_base::sync_with_stdio(false);

	if(argc==2)
	{
		svc obj(argv[1]);   //Testing			
	}
	return 0;
}