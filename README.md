# graycord
Graylog API log parser to discord 
 

# GrayCord

## Graylog + Discord = GrayCord

#
Graycord does a good job as a standalone syslog server but I found a shortcoming where it wasnt able to send alerts to discord. 

## Installation

Use docker pull [Docker](https://hub.docker.com/r/mikehanson/graycord).

```bash
docker pull mikehanson/graycord
```

## Usage

Variables that can be passed to docker img. 
```python
PASSWORD = **None** 
USERNAME = **None** 
HOSTNAME = **None** 
TOKEN = **None** 
CHANNEL = **None** 
PORT = **None** 
SEARCH_QUERY = **None**  
INTERVAL = **None** 
```

## Example 

```python 

sudo docker run -e PASSWORD="passwordForGrayLog" -e HOSTNAME='ip/hostname for graylog' -e TOKEN='discord-bot-token' docker_img_name

```


## DockerHub 
[https://hub.docker.com/r/mikehanson/graycord](https://hub.docker.com/r/mikehanson/graycord)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)