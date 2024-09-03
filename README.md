# blaze_integration
## Overview
This project provides a way for a ui client to ineract with the blaze server to connect and build databases through django.
### BaseUrl
- localhost/rdf/
  homepage
### Endpoints Available
#### - get_files/<br />
      method: GET
      body: None
      response: {[files], status=200}
      description: retrieve uploaded files
#### - upload_file/<br />
      method: POST
      body: {name: "", graph_id: "", size: "", file: ""}
      response: {message: success, status=200}
      description: upload file
#### - upload_ttl/<br />
      method: POST
      body: {ttl_file: ""}
      response: {message: success, status=200}
      description: upload ttl files
#### - namespace/add/<br />
      method: POST
      body: {port: "", namespace: "", properties: ""}
      response: {message: namespace_success, status=201}
      description: create or add a namespace 
#### - connect_database/
      connect to a database
#### - db_create/<br />
      method: POST
      body: {port: "", installationPath: "", minMemory: "", maxMemory: "", name_space: ""}
      response: {message: created successfully, status=201}
      description: create a database
#### - db_logs/<br />
      method: GET
      body: {name: "name_space"}
      response: {data: [], status=200}
      description: view database logs
#### - db_containers/<br />
      method: GET
      body: None
      response: {data: [], status=200}
      description: view running containers
#### - db_destroy/<br />
      method: POST
      body: {name: "name_space"}
      response: {data: removed successfully, status=200}
      description: delete database by path
#### - active-database/<br />
      method: GET
      body: {port: "", namespace: ""}
      response: {active_database: {}, status=200}
      description: retrieve active databases
#### - active-repository/<br />
      method: GET
      body: {port: "", namespace: ""}
      response: {active_repository: {}, status=200}
      description: retrieve active repositories
  

