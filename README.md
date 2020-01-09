# Symend
 
To run the code, copy Symend_Project.py and dev.ini files to your Home dirctory and change dev.ini file contents as follows.
In dev.ini file, the first line after [settings] is the search directory and the second line served as log file.

I should mention that the way I implemented this is I add all the files in a data frame, then sort by name and date and for each name I keep the file with the latest date.
Another way to do this is at the time I am reading the data, I decide whether I should add it to the list (if no such file is in the list yet), or replace one of the files in the list with this file (if the file with the same name is older).

If the total number of files is N, and there are K unique files, and the number of files for type i is n_i (i.e., sum_{i=1 to K}  n_i = N)  then the computational complexity of the fist (implemented) approach is O(N lg(N)).
But the computational complexity of the second method is N*K. 

In regular cases of file repositories, we assume K is very large and we don’t have that many repeatative files, i.e., K is almost N, then the complexity of the first method is smaller and that’s why I chose to implement the first method.
However, memorywise, the second method is more efficient since it does in place replacement.


dependencies:

 pathlib2==2.3.2
 pandas==0.23.4
 
