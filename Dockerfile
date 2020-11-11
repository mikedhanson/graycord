#base image
FROM python:3

# add script to root dir
ADD GrayCord.py /

# configure timezone
ENV TZ America/Chicago

#Set Environment Vars for docker
ENV PASSWORD = **None** \
	USERNAME = **None** \
	HOSTNAME = **None** \
	TOKEN = **None** \ 
	CHANNEL = **None** \ 
	PORT = **None** \ 
	SEARCH_QUERY = **None** \ 
	INTERVAL = **None** 

# copy the dependencies file to the working directory
COPY requirements.txt ./

#install dependencies 
RUN pip3 --default-timeout=100 install -r requirements.txt --no-build-isolation 

# cmd to run container at start
CMD [ "python3", "./GrayCord.py" ]