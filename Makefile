# Path to the application repository on the server.
APP_PATH := "chatgpt-like-clone"
# String used to specify the domain for SSH commands.
SSH_APP_DOMAIN := "ubuntu@chatgpt-like.ai.dualboot.dev/"

# Commands with the 'remote_' prefix are meant to be executed on the server in the application folder.

# Pull from Github
remote_pull:
	git reset --hard
	git pull origin main:main

# Stop APP srvice
remote_stop:
	docker-compose down

# Start APP srvice
remote_start:
	docker-compose up -d

# Init APP srvice
remote_init:
	make remote_pull
	docker-compose build
	make remote_start

# Update APP srvice
remote_update:
	make remote_stop
	docker-compose build
	make remote_start

# Commands without the 'remote_' prefix are executed locally.
start_ssh_agent:
	eval "$(ssh-agent -s)" && ssh-add ./ssh/ssh.pem

# Actual deployment command
deploy:
	make start_ssh_agent
	ssh -A $(SSH_APP_DOMAIN) "cd $(APP_PATH) && make remote_pull && make remote_update"

ssh:
	ssh -A $(SSH_APP_DOMAIN)

ssh_to_app:
	make start_ssh_agent
	ssh -At $(SSH_APP_DOMAIN) "cd $(APP_PATH) && docker-compose exec app bash"

.SILENT:
