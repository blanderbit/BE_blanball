# BE_blanball

## Install docker desktop 

>1. sudo apt update
>2. sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
>3. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
>4. sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
>5. sudo apt install docker-ce

## Install docker-compose

>1. sudo curl -L "https://github.com/docker/compose/releases/download/1.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
>2. sudo chmod +x /usr/local/bin/docker-compose

## Run project

In the main directory `BE_blanball/project` run the command `sudo docker-compose up` or `sudo docker-compose up -d` this command will start the project without taking up your console


<!-- # cd project 

# celery -A project worker -l info" -->


<!-- const ws = new WebSocket("ws://localhost:8000/ws/")

ws.onmessage = function(e){
    console.log(e)
} -->

<!-- ws.send(JSON.stringify({
    action: "list",
    request_id: new Date().getTime()
})) -->

\

<!-- aioredis==1.3.1
amqp==5.1.1
asgiref==3.5.0
async-timeout==4.0.2
attrs==21.4.0
autobahn==22.7.1
Automat==20.2.0
autopep8==1.6.0
billiard==3.6.4.0
certifi==2022.5.18.1
cffi==1.15.0
charset-normalizer==2.0.12
click==8.1.3
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.2.0
colorama==0.4.4
constantly==15.1.0
coreapi==2.3.3
coreschema==0.0.4
cryptography==37.0.2
defusedxml==0.7.1
Deprecated==1.2.13
distlib==0.3.4
djoser==2.1.0
filelock==3.7.1
hiredis==2.0.0
hpack==4.0.0
hyperframe==6.0.1
hyperlink==21.0.0
idna==3.3
incremental==21.3.0
inflection==0.5.1
itypes==1.2.0
Jinja2==3.1.2
jsonschema==4.5.1
kombu==5.2.4
MarkupSafe==2.1.1
msgpack==1.0.3
oauthlib==3.2.0
openapi-codec==1.3.2
packaging==21.3
platformdirs==2.5.2
priority==2.0.0
prompt-toolkit==3.0.30
protobuf==3.20.1
pyasn1==0.4.8
pyasn1-modules==0.2.8
pycodestyle==2.8.0
pycparser==2.21
pyOpenSSL==22.0.0
pyparsing==3.0.9
pyrsistent==0.18.1
python3-openid==3.2.0
pytz==2022.1
redis==4.3.4
requests==2.28.1
requests-oauthlib==1.3.1
ruamel.yaml==0.17.21
ruamel.yaml.clib==0.2.6
service-identity==21.1.0
simplejson==3.17.6
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.2.0
sqlparse==0.4.2
style==1.1.0
swagger-spec-validator==2.7.4
toml==0.10.2
Twisted==22.4.0
txaio==21.2.1
typing_extensions==4.0.0
tzdata==2022.1
update==0.0.1
uritemplate==4.1.1
urllib3==1.26.9
vine==5.0.0
virtualenv==20.16.2
wcwidth==0.2.5
wrapt==1.14.1
zope.interface==5.4.0
tzlocal==2.1 -->