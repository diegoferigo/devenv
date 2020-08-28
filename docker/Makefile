default: latest intel nvidia

latest: intel
	docker tag diegoferigo/devenv:intel diegoferigo/devenv:latest

intel:
	docker build --rm \
		--build-arg from=ubuntu:focal \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--tag diegoferigo/devenv:intel \
		.

nvidia:
	docker build --rm \
		--build-arg from=diegoferigo/cuda:10.2-cudnn8-runtime-ubuntu20.04 \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--tag diegoferigo/devenv:nvidia \
		.

push_latest:
	docker push diegoferigo/devenv:latest

push_intel:
	docker push diegoferigo/devenv:intel
	
push_nvidia:
	docker push diegoferigo/devenv:nvidia
