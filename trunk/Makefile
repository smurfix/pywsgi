PACKAGE_NAME=pywsgi
PREFIX=/usr/local/

clean:
	find . -name "*.pyc" -o -name "*.pyo" | xargs -n1 rm -f

install:
	python setup.py install --prefix $(PREFIX)

dist:
	python setup.py sdist

deb:
	debuild -S -sa
	VERSION=`python setup.py --version`; \
	cd ..; sudo pbuilder build $(PACKAGE_NAME)_$$VERSION-0ubuntu1.dsc; cd -
