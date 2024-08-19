import requests
import json 
from django.shortcuts import render, redirect
from rdflib import Graph
from .models import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadTTLForm
from django.conf import settings
from django.http import HttpResponse, JsonResponse



def homepage(request):
    return HttpResponse("Welcome to the homepage!")

@csrf_exempt
def get_files(request):
    files = UploadedFile.objects.all().values('name', 'graph_id', 'size', 'id')
    file_list = list(files)
    return JsonResponse({'files': file_list})

@csrf_exempt
def create_database(request):
    if request.method == 'POST':
        data = request.POST
        namespace = data.get('namespace')
        properties = {
            'com.bigdata.rdf.store.DataLoader': 'com.bigdata.rdf.data.RDFDataLoader',
            'com.bigdata.rdf.store.DataLoader.context': 'com.bigdata.rdf.data.RDFDataLoaderContext',
            'com.bigdata.rdf.sail.isolates': 'true',
            'com.bigdata.rdf.sail.quads': 'true',
            'com.bigdata.rdf.sail.axioms': 'true',
            'com.bigdata.rdf.sail.includeInferred': 'true',
            'com.bigdata.rdf.sail.incremental': 'false',
        }

        url = f'{settings.BLAZEGRAPH_URL}{namespace}'
        response = requests.post(url, json={'properties': properties})

        if response.status_code == 200:
            return JsonResponse({'message': 'Database created successfully'})
        else:
            return JsonResponse({'error': 'Failed to create database'})

    return JsonResponse({'error': 'Invalid request method'})

def upload_ttl(request):
    if request.method == 'POST':
        form = UploadTTLForm(request.POST, request.FILES)
        if form.is_valid():
            ttl_file = request.FILES['ttl_file']
            graph = Graph()
            graph.parse(ttl_file, format="ttl")

            data = graph.serialize(format="nt").decode("utf-8")

            response = requests.post(f"{settings.BLAZEGRAPH_URL}/namespace/kb/sparql", 
                                     data=data, 
                                     headers={"Content-Type": "application/x-turtle"})
            if response.status_code == 200:
                return JsonResponse({'message': 'success'})
            else:
                # return render(request, 'upload_ttl1.html',1 {'form': form, 'error': response.text})
                return JsonResponse({'error': 'Failed'})
            
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

        response = requests.post(f"{settings.BLAZEGRAPH_URL}/namespace", data=config)
        if response.status_code == 201:
            return JsonResponse({"message": 'namespace_success'})
        else:
            return JsonResponse({'error': response.text})
    response = HttpResponse("Here's the text of the web page.")
    return response
    # return render(request, 'add_namespace.html')

csrf_exempt
def connect_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip_address = data.get('ipAddress')
            port = data.get('port')
            database_type = data.get('databaseType')

            if not ip_address or not port or not database_type:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            url = f"http://{ip_address}:{port}/blazegraph/namespace/{database_type}/sparql"
            response = requests.get(url)

            if response.status_code == 200:
                return JsonResponse({"success": True, "message": "Connected successfully"})
            else:
                return JsonResponse({"success": False, "message": "Failed to connect"}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def get_active_database(request):
    if request.method == 'GET':
        try:
            url = f"{settings.BLAZEGRAPH_URL}namespace"
            response = requests.get(url)
            data = response.json()
            active_databases = [namespace for namespace in data if namespace['isDefault']]
            if active_databases:
                active_database = active_databases[0]
                return JsonResponse({'active_database': active_database})
            else:
                return JsonResponse({"message": "No active database found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "Failed to fetch active database"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_active_repository(request):
    if request.method == 'GET':
        try:
            url = f"{settings.BLAZEGRAPH_URL}namespace"
            response = requests.get(url)
            data = response.json()
            active_repositories = [namespace for namespace in data if not namespace['isDefault']]
            if active_repositories:
                active_repository = active_repositories[0]
                return JsonResponse({'active_repository': active_repository})
            else:
                return JsonResponse({"message": "No active repository found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": "Failed to fetch active repository"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)