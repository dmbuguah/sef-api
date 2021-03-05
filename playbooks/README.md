# playbooks

Based on ubuntu server 16.04


## File structure
The playbooks folder has the following structure

```javascript
│
├── playbooks
│   ├── ansible.cfg  // the ansible config file
│   ├── roles/        // 'core' roles that are shared by other roles. can be thought of as libraries are not designed to be 'executable' by themselves
│   ├── README.md    // this file
│   └── <xyz>.yml    // playbook entry points for the roles defined in 'roles/'
│
│
```

ansible-playbook -vvv -i prod  -lprod prod.yml --vault-password-file pass 
