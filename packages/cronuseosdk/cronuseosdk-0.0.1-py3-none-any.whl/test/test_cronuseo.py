from cronuseosdk import Cronuseo


conuseo = Cronuseo("http://localhost:8080/api/v1", "super", "JLE+1Z3c/jIQL+i+ORhI+jLbM5pXvdxNrKvIcrKVFss=")
response = conuseo.checkPermission("shashimal", "write", "doc")
assert response == True

response = conuseo.checkPermissions("shashimal", ["write", "read", "update"], "doc")
assert response == ["write", "read"]