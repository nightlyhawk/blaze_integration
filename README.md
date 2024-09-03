# blaze_integration
## Overview
This project provides a way for a ui client to ineract with the blaze server to connect and build databases through django.
### BaseUrl
- url/rdf/
  homepage
### Endpoints Available
  - get_files/<br />
      method: GET<br />
      body: None<br />
      response: {[files], status=200}<br />
      description: retrieve uploaded files
  - upload_file/<br />
      method: POST<br />
      body: {name: "", graph_id: "", size: "", file: ""}<br />
      response: {message: success, status=200}<br />
      description: upload file
  - upload_ttl/<br />
      method: POST<br />
      body: {ttl_file: ""}<br />
      response: {message: success, status=200}<br />
      description: upload ttl files
  - namespace/add/<br />
      method: POST<br />
      body: {port: "", namespace: "", properties: ""}<br />
      response: {message: namespace_success, status=201}<br />
      description: create or add a namespace 
  - connect_database/
      connect to a database
  - db_create/<br />
      method: POST<br />
      body: {port: "", installationPath: "", minMemory: "", maxMemory: "", name_space: ""}<br />
      response: {message: created successfully, status=201}<br />
      description: create a database
  - db_logs/<br />
      method: GET<br />
      body: {name: "name_space"}<br />
      response: {data: [], status=200}<br />
      description: view database logs
  - db_containers/<br />
      method: GET<br />
      body: None<br />
      response: {data: [], status=200}<br />
      description: view running containers
  - db_destroy/<br />
      method: POST<br />
      body: {name: "name_space"}<br />
      response: {data: removed successfully, status=200}<br />
      description: delete database by path
  - active-database/<br />
      method: GET<br />
      body: {port: "", namespace: ""}<br />
      response: {active_database: {}, status=200}<br />
      description: retrieve active databases
  - active-repository/<br />
      method: GET<br />
      body: {port: "", namespace: ""}<br />
      response: {active_repository: {}, status=200}<br />
      description: retrieve active repositories
  

