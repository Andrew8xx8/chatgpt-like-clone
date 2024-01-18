# Path to the application repository on the server.
APP_PATH := "chatgpt-like-clone"
# String used to specify the domain for SSH commands.
SSH_APP_DOMAIN := "avk@left-gpt.8xx8.ru"

# Commands with the 'remote_' prefix are meant to be executed on the server in the application folder.

# Pull from Github
remote_pull:
	git reset --hard
	git pull origin main:main

# Restart APP srvice
remote_update:
	docker-compose down
	docker-compose build
	docker-compose up -d

# Commands without the 'remote_' prefix are executed locally.
start_ssh_agent:
	eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa

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
