
svc::svc(string filename, int file_version){



	if(!dirExists(".svc"))   // .svc doesn't exist
	{
			cout<<"Initialization not done! Use 'svc init' to initialize the current directory\n";
			cout<<endl;
			exit(EXIT_FAILURE);
	}
	else   //.svc exists
	{

			// Requested version
		this->version = file_version; 
		// SVC initialized file
		this->filename = filename;

		// real_version variable to decrement the requested version by 1 because versions are starting with 0
		int real_version = this->version;
		// convert to string
		string real_version_str = to_string(real_version);

		// Path calculation for required files
		this->path_to_masterfile = ".svc/"+this->filename+"_repo/masterfile";
		this->path_to_version = ".svc/"+this->filename+"_repo/version/"+"v"+real_version_str;
		this->path_to_version_head = ".svc/"+this->filename+"_repo/version/version_head";

		//===================== validations starts ================================
		
		// check if entered file exists or not
		if(!fileExists(this->filename.c_str()))
		{
			cout<<"fatal: File '"+this->filename+"' doesn't exist, Please try again."<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}

		this->path_to_repo = ".svc/"+this->filename+"_repo/";
				
		if(!dirExists(this->path_to_repo.c_str()))  //repo doesn't exist!
		{
			cout<<"fatal: File repository for file '"+this->filename+"' not initialized, make atleast 1 commit using 'svc "+this->filename+"' to initialize file repository."<<endl;
			cout<<endl;
			exit(EXIT_FAILURE);
		}

		// setup to read the version_head
		string version_head_str;
		this->fin_version_head.open(this->path_to_version_head);

		// versoin_head opened or not
		if(!this->fin_version_head.is_open())
		{
			cout<<"fatal: Unable to open '"+this->path_to_version_head+"', Please try again."<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}

		getline(this->fin_version_head,version_head_str);
		int version_head_int = str_to_int(version_head_str);

		// check if entered version number exists or not
		if(version_head_int < this->version)
		{
			cout<<"fatal: Version doesn't exist yet, Number of versions available are: "+to_string(version_head_int)<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}
		// check if entered version number is leass than 0 or not
		if(this->version<0)
		{
			cout<<"fatal: Version number cannot be less then 0, version num"<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}

		// check if masterfile exists or not
		if(!fileExists(this->path_to_masterfile.c_str()))
		{
			cout<<"fatal: Masterfile file: '"+this->path_to_masterfile+"' doesn't exist for '"+this->filename+"' file, Please try again."<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}
		// check if version file exists or not
		if(!fileExists(this->path_to_version.c_str()))
		{
			cout<<"fatal: Version file: '"+this->path_to_version+"' doesn't exist, Please try again."<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}
		// check if version_head exists or not
		if(!fileExists(this->path_to_version_head.c_str()))
		{
			cout<<"fatal: Version head: '"+this->path_to_version_head+"' doesn't exist, Please try again."<<endl;
			cout<<endl;
			exit (EXIT_FAILURE);
		}

		//===================== validations ends ================================

		// Debug: variable printer
		if(SIMPLE_DEBUG)
		{
			cout<<"================ DEBUG INFO STARTS =============="<<endl;
			cout<<"Version path is = "<<this->path_to_version<<endl;
			cout<<"Masterfile path is = "<<this->path_to_masterfile<<endl;
			cout<<"================ DEBUG INFO ENDS ================"<<endl<<endl;

		}
	}
	
}
//================= constructor ends======================




string svc::retrive()
{
	// buffer variable used to store the contents for requested version and then it will be printed
	string buffer=""; 

	// Opening the required files
	this->fin_masterfile.open(this->path_to_masterfile);
	this->fin_prev_version.open(this->path_to_version);

	// masterfile opened or not
	if(!this->fin_masterfile.is_open())
	{
		cout<<"fatal: Unable to open '"+this->path_to_masterfile+"', Please try again."<<endl;
		cout<<endl;
		exit (EXIT_FAILURE);
	}

	// version file opened or not
	if(!this->fin_prev_version.is_open())
	{
		cout<<"fatal: Unable to open '"+this->path_to_version+"', Please try again."<<endl;
		cout<<endl;
		exit (EXIT_FAILURE);
	}

	//============================ Reading loop starts ==========================
	// Reading loop: It will read each line of version file of requested version,
	// it will fetch corresponding line from masterfile and will store those lines
	// in 'buffer' (string) variable 
	while(!this->fin_prev_version.eof())
	{
		int seek_position;
		string s;
		// variable s will have a line number from version file fin_prev_version
		getline(this->fin_prev_version,s);

		// string to int
		int line = str_to_int(s);
		// logic variable line, wiil be used to calculate seek_position
		line = line-1; 
		// seek_posyion calculation, multiply by 10 because each line has max 10 char including newline 
		seek_position = 10*line;
		// moving the read pointer
		this->fin_masterfile.seekg(seek_position);

		// s2 to store the line fetched from masterfile
		string s2;
		getline(this->fin_masterfile,s2);

		// appending s2 to buffer
		buffer+=s2+"\n";

		// Debug: variable printer
		if(SIMPLE_DEBUG)
		{
			cout<<"================ DEBUG INFO STARTS =============="<<endl;
			cout<<"Line number in string is = "<<s<<endl;
			cout<<"Line number in int is = "<<line<<endl;
			cout<<"Seek position is = "<<seek_position<<endl;
			cout<<"Line read from master is = "<<s2<<endl;
			cout<<"================ DEBUG INFO ENDS ================"<<endl<<endl;
		}

	}
	//============================ Reading loop ends ==========================

	// Printing the buffer
	// cout<<buffer;

	return buffer;

}
//================= functionality code ends======================
