import requests
import json 
from django.shortcuts import render, redirect
from rdflib import Graph
from .models import UploadedFile
from .decorators import error_catch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadTTLForm
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import os
import docker



def homepage(request):
    return HttpResponse("Welcome to the homepage!")

@csrf_exempt
@error_catch
def get_files(request):
    files = UploadedFile.objects.all().values('name', 'graph_id', 'size', 'id')
    file_list = list(files)
    return JsonResponse({'files': file_list}, status=200)

@csrf_exempt
@error_catch
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
        print('hereee')
        url = f'{settings.BLAZEGRAPH_URL}{namespace}'
        response = requests.post(url, json={'properties': properties})

        if response.status_code == 200:
            return JsonResponse({'message': 'Database created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to create database'}, status=400)

    return JsonResponse({'error': f'Invalid request method {request.method}'}, status=400)

@error_catch
def upload_ttl(request):
    if request.method == 'POST':
        form = UploadTTLForm(request.POST, request.FILES)
        if form.is_valid():
            ttl_file = request.FILES['ttl_file']
            graph = Graph()
            graph.parse(ttl_file, format="ttl")

            data = graph.serialize(format="nt").decode("utf-8")

            response = requests.post(f"{settings.BLAZEGRAPH_URL}namespace/kb/sparql", 
                                     data=data, 
                                     headers={"Content-Type": "application/x-turtle"})
            if response.status_code == 200:
                return JsonResponse({'message': 'success'}, status=200)
            else:
                # return render(request, 'upload_ttl1.html',1 {'form': form, 'error': response.text})
                return JsonResponse({'error': 'Failed'}, status=400)
        return JsonResponse({'error': 'Invalid formdata'}, status=400)    
    # response = HttpResponse("Here's the text of the web page.")
    # return response
    else:
        form = UploadTTLForm()

    # return render(request, 'upload_ttl.html', {'form': form})

@error_catch
def add_namespace(request):
    if request.method == 'POST':
        namespace_name = request.POST.get('namespace_name')
        config = {
            'com.bigdata.rdf.sail.namespace': namespace_name,
            'com.bigdata.rdf.store.AbstractTripleStore.textIndex': True,
            'com.bigdata.rdf.store.AbstractTripleStore.justify': True,
            'com.bigdata.rdf.store.AbstractTripleStore.quads': True
        }

        response = requests.post(f"{settings.BLAZEGRAPH_URL}namespace", data=config)
        if response.status_code == 201:
            return JsonResponse({"message": 'namespace_success'}, status=200)
        else:
            return JsonResponse({'error': response.text}, status=400)
    response = HttpResponse("Here's the text of the web page.")
    return response
    # return render(request, 'add_namespace.html')

@csrf_exempt
@error_catch
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
                return JsonResponse({"success": True, "message": "Connected successfully"}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Failed to connect"}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
@csrf_exempt
@error_catch
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
@error_catch
def get_active_repository(request):
    if request.method == 'GET':
        try:
            url = f"{settings.BLAZEGRAPH_URL}namespace"
            response = requests.get(url)
            print('here', response)
            data = response.json()
            active_repositories = [namespace for namespace in data if not namespace['isDefault']]
            if active_repositories:
                active_repository = active_repositories[0]
                return JsonResponse({'active_repository': active_repository})
            else:
                return JsonResponse({"message": "No active repository found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

client = docker.from_env()

def create_container(port, path, min, max, name):
    print(port, path, min, max, name)
    client.containers.run("lyrasis/blazegraph:2.1.5", 
                          detach=True, 
                          ports={'8080/tcp': port},
                          environment=[f"JAVA_OPTS= -Xms{min} -Xmx{max}"],
                          name= f"blazegraph_{name}",
                          volumes={
                                'blazegraph_data': {
                                    'bind': f'/var/{path}', 
                                    'mode': 'rw'
                                }
                            }
                        )
def run_container(name):
    client.containers.run(name, detach=True)

def stop_container(name):
    container = client.containers.get(name)
    container.stop()

def remove_container(name):
    container = client.containers.get(name)
    container.remove()

def view_containers():
    containers = client.containers.list()
    return containers

def retrieve_logs(name):
    container = client.containers.get(name)
    for log in container.logs():
        print(log)
    return container.logs()

@csrf_exempt
@error_catch
def createActualDB(request):
    if request.method == "POST":
        data = json.loads(request.body)
        compose_content = f"""
        version: '3.7'

        services:
            blazegraphs:
                image: lyrasis/blazegraph:2.1.5
                container_name: blazegraph_{data.get('name_space')}
                enviroment:
                - JAVA_OPTS= -Xms{data.get('minMemory')} -Xmx{data.get('maxMemory')}
                ports:
                - {data.get('port')}:8080
                volumes:
                - blazegraph_data:{data.get('installationPath')}
        """
        with open("docker-compose.yaml", "w") as f:
            f.write(compose_content)
        
        # os.system("sudo docker compose up -d")
        create_container(data.get('port'), 
                         data.get('installationPath'), data.get('minMemory'), 
                         data.get('maxMemory'), data.get('name_space'))
        for log in client.containers.get(f"blazegraph_{data.get('name_space')}").logs():
            print(log)

        return JsonResponse({"message": "created successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
@error_catch    
def destroyDB(request):
    if request.method == "POST":
        data = json.loads(request.body)
        stop_container(data.get('name'))
        remove_container(data.get('name'))
        return JsonResponse({"message": "removed successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
@error_catch
def retrieveDBlogs(request):
    if request.method == "GET":
        data = json.loads(request.body)
        res = retrieve_logs(data.get('name'))
        # Check if the result is in bytes and decode it
        if isinstance(res, bytes):
            res = res.decode('utf-8')

        return JsonResponse({"data": res}, status=200)
    else:
        return JsonResponse({"error": "Invalid method"}, status=400)
    
@csrf_exempt
@error_catch
def retrieveDBcontainers(request):
    if request.method == "GET":
        containers = view_containers()
        containers_info = []
        for container in containers:
            containers_info.append({
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "N/A",
                "ports": container.attrs['NetworkSettings']['Ports']
            })
        # Check if the result is in bytes and decode it

        return JsonResponse({"data": containers_info}, status=200, safe=False)
    else:
        return JsonResponse({"error": "Invalid method"}, status=400)