Python Implementation of Apriori & FpGrowth
==========================================

List of files
-------------
1. apriori.py
2. FpGrowth.py
3. test.py (in order to test some dependencies)
2. README(this file)
3. Data/ 
		1.adult.data
		2.adult.names
	    3.adult.test
	    4.old.adult.names
		5.test.txt

The dataset is a copy of the "Adult Data Set" 
dataset in the `http://archive.ics.uci.edu/ml/datasets/Adult`_

Usage
-----
To run the program with dataset provided and default values for *minSupport* = 0.3 and *minConfidence* = 0.6

    python apriori.py|FpGrowth.py 

To run program with dataset  

    python apriori.py|FpGrowth.py  -f [dataset] -s [minsupport] -c [minconfidence]

License
-------
MIT-License

-------