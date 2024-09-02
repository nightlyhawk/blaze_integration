$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker stop $(docker -p -q)
$ docker rm $(docker -p -a -q)
$ docker logs "container_name"
$ scp -i /path/to/your-key.pem -r /path/to/local/directory username@ec2-instance-public-ip:/path/to/remote/directory

com.bigdata.rdf.sail.namespace=
com.bigdata.rdf.store.AbstractTripleStore.textIndex=false
com.bigdata.rdf.sail.truthMaintenance=false
com.bigdata.rdf.store.AbstractTripleStore.quads=false
com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
com.bigdata.rdf.store.AbstractTripleStore.justify=false
com.bigdata.rdf.sail.isolatableIndices=false
com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false

curl -D- -H 'Content-Type: text/turtle' --upload-file tbox.ttl -X POST 'http://localhost:80/bigdata/sparql?context-uri=http://example.org/tbox'