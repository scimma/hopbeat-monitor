##
## For tagging the container:
##
CNT_NAME := scimma/hopbeat-monitor

TAG      := $(shell git log -1 --pretty=%H || echo MISSING )
CNT_IMG  := $(CNT_NAME):$(TAG)
CNT_LTST := $(CNT_NAME):latest

REGION  := us-west-2
AWSREG  := 585193511743.dkr.ecr.us-west-2.amazonaws.com
MAJOR   := 0
MINOR   := 0
RELEASE := 6

RELEASE_TAG := $(MAJOR).$(MINOR).$(RELEASE)

.PHONY: test set-release-tags push clean client server all

all: container

print-%  : ; @echo $* = $($*)

container: Dockerfile
	@if [ ! -z "$$(git status --porcelain)" ]; then echo "Directory is not clean. Commit your changes."; exit 1; fi
	docker build -f $< -t $(CNT_IMG) .
	docker tag $(CNT_IMG) $(CNT_LTST)

set-release-tags:
	@$(eval RELEASE_TAG := $(shell echo $(GITHUB_REF) | awk -F- '{print $$2}'))
	@echo RELEASE_TAG =  $(RELEASE_TAG)
	@$(eval MAJOR_TAG   := $(shell echo $(RELEASE_TAG) | awk -F. '{print $$1}'))
	@echo MAJOR_TAG = $(MAJOR_TAG)
	@$(eval MINOR_TAG   := $(shell echo $(RELEASE_TAG) | awk -F. '{print $$2}'))
	@echo MINOR_TAG = $(MINOR_TAG)

push: 
	@(echo $(RELEASE_TAG) | grep -P '^[0-9]+\.[0-9]+\.[0-9]+$$' > /dev/null ) || (echo Bad release tag: $(RELEASE_TAG) && exit 1)
	./bin/awsDockerLogin $(REGION) $(AWSREG) >/dev/null 2>/dev/null
	docker tag $(CNT_IMG) $(AWSREG)/$(CNT_NAME):$(RELEASE_TAG)
	docker tag $(CNT_IMG) $(AWSREG)/$(CNT_NAME):$(MAJOR)
	docker tag $(CNT_IMG) $(AWSREG)/$(CNT_NAME):$(MAJOR).$(MINOR)
	docker push $(AWSREG)/$(CNT_NAME):$(RELEASE_TAG)
	docker push $(AWSREG)/$(CNT_NAME):$(MAJOR)
	docker push $(AWSREG)/$(CNT_NAME):$(MAJOR).$(MINOR)
#	rm -f $(HOME)/.docker/config.json

clean:
	rm -f *~
	rm -f downloads/*
	if [ -d downloads ]; then  rmdir downloads else /bin/true; fi
