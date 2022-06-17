#! /usr/bin/env bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $dir

order="$1"
options=(
	"build"
	"develop"
	"production"
	"stop"
)

if [[ -z "$order" ]]; then
	echo
	echo "DESREGISTRADORES CLI"
	echo "----------"
	echo "What do you want to do?"

	i=0;
	for opt in "${options[@]}"; do
		echo "[$i]: $opt"
		i=$((i+1))
	done

	echo
	echo "Emter an option:"
	read order
	echo

	re="^[0-9]*$"
	if [[ $order =~ $re ]]; then
		order=${options[$order]}
		echo $order
	fi
fi

if [[ "$order" == "build" ]]; then
	NODE_ENV=production
	cd client
	node_modules/.bin/react-scripts build
	cd ..

	cd server
	node_modules/.bin/strapi build
	cd ..

elif [[ "$order" == "develop" ]]; then
	FASTAPI_ENV=development
	cd geo-server
	.venv/bin/uvicorn src.main:app --reload --port 1338 &>/dev/null &
	echo "$!" > /tmp/uvicorn.pid
	cd ..

	NODE_ENV=development
	cd server
	node_modules/.bin/strapi develop

	kill $(cat /tmp/uvicorn.pid)
elif [[ "$order" == "production" ]]; then
	FASTAPI_ENV=production
	cd geo-server
	nohup .venv/bin/uvicorn src.main:app --port 1338 &>/dev/null &
	echo "$!" > /tmp/uvicorn.pid
	cd ..

	NODE_ENV=production
	cd server
	nohup node_modules/.bin/strapi start &>/dev/null &
	echo "$!" > /tmp/strapi.pid
	cd ..
elif [[ "$order" == "stop" ]]; then
	if [[ -f "/tmp/fastapi.pid" ]]; then
		kill $(cat /tmp/uvicorn.pid)
	fi
	if [[ -f  "/tmp/strapi.pid" ]]; then
		kill $(cat /tmp/strapi.pid)
	fi
else
	echo "Unkown order"
fi
