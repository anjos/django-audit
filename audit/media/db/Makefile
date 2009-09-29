# Created by Andre Anjos <andre.dos.anjos@cern.ch> 
# Qua 23 Set 2009 15:30:14 CEST 

REFRESH=32 # the dbs are updated monthly - we wait a bit longer

all: clean
	@./install.sh

clean:
	@rm -vf *~
	@find . -mtime +$(REFRESH) -name '*.dat' -print0 | xargs -0 rm -vf;
	@find . -mtime +$(REFRESH) -name '*.csv' -print0 | xargs -0 rm -vf;

reset: clean
	@rm -vf *.dat *.csv
