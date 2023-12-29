all:
	if ! test -d venv; then python3 -m venv venv; fi;
	. ./venv/bin/activate
	pip3 install -r requirements.txt
	rm -f ../../core/pyspec/zond2spec/test/phase0/random/test_random.py
	rm -f ../../core/pyspec/zond2spec/test/altair/random/test_random.py
	rm -f ../../core/pyspec/zond2spec/test/bellatrix/random/test_random.py
	rm -f ../../core/pyspec/zond2spec/test/capella/random/test_random.py
	rm -f ../../core/pyspec/zond2spec/test/deneb/random/test_random.py
	python3 generate.py phase0 > ../../core/pyspec/zond2spec/test/phase0/random/test_random.py
	python3 generate.py altair > ../../core/pyspec/zond2spec/test/altair/random/test_random.py
	python3 generate.py bellatrix > ../../core/pyspec/zond2spec/test/bellatrix/random/test_random.py
	python3 generate.py capella > ../../core/pyspec/zond2spec/test/capella/random/test_random.py
	python3 generate.py deneb > ../../core/pyspec/zond2spec/test/deneb/random/test_random.py
