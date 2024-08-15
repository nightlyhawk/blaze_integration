import requests
from django.shortcuts import render, redirect
from rdflib import Graph
from .forms import UploadTTLForm
from django.http import HttpResponse

BLAZEGRAPH_URL = "http://localhost:9999/blazegraph"

def upload_ttl(request):
    if request.method == 'POST':
        form = UploadTTLForm(request.POST, request.FILES)
        if form.is_valid():
            ttl_file = request.FILES['ttl_file']
            graph = Graph()
            graph.parse(ttl_file, format="ttl")

            data = graph.serialize(format="nt").decode("utf-8")

            response = requests.post(f"{BLAZEGRAPH_URL}/namespace/kb/sparql", 
                                     data=data, 
                                     headers={"Content-Type": "application/x-turtle"})
            return response
            # if response.status_code == 200:
            #     return redirect('success')
            # else:
            #     return render(request, 'upload_ttl.html', {'form': form, 'error': response.text})
    response = HttpResponse("Here's the text of the web page.")
    return response
    # else:
    #     form = UploadTTLForm()

    # return render(request, 'upload_ttl.html', {'form': form})

def add_namespace(request):
    if request.method == 'POST':
        namespace_name = request.POST.get('namespace_name')
        config = {
            'com.bigdata.rdf.sail.namespace': namespace_name,
            'com.bigdata.rdf.store.AbstractTripleStore.textIndex': True,
            'com.bigdata.rdf.store.AbstractTripleStore.justify': True,
            'com.bigdata.rdf.store.AbstractTripleStore.quads': True
        }

        response = requests.post(f"{BLAZEGRAPH_URL}/namespace", data=config)
        return response
        # if response.status_code == 201:
        #     return redirect('namespace_success')
        # else:
        #     return render(request, 'add_namespace.html', {'error': response.text})
    response = HttpResponse("Here's the text of the web page.")
    return response
    # return render(request, 'add_namespace.html')
