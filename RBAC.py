1. can't create a new resource in a resource group
- check access control to verify the user has the appropriate role assignment
- if the user is part of a custom role verify that the role definition can deploy that resource

2. attempt to add a role assignment in your subscription and you recerive 'role assignment limit exceeded'
- in your subscription, a limit of 2,000 role assignments
- consider assigning roles to groups instead of individual users

3. attempt to create or update a custom role but get an error
- confirm the user has the Microsoft.Authorization/roleDefinition/write permission

4. attempt to create a new custom role and you receive 'role definition limit exceeded'
- in you tenant, there is a limit of 2,000 custom roles

5. make a change in Access Control or add a custom role and change is NOT reflected in the portal or in the console
- these changes can take time to take effect
- logout and re-login to force the refresh

########################################### Owner/Contributor/Reader/(Administrator:manage access) ###########################################
