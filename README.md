# GrayCord
Graylog API log parser to discord 

## Graylog + Discord = GrayCord

#
Graylog does a good job as a standalone syslog server but I found a shortcoming where it wasn’t able to send alerts to discord. So, I took on the challenge to dive into python3 and learn all about docker.

## Installation

Use docker pull [Docker](https://hub.docker.com/r/mikehanson/graycord).

```bash
docker pull mikehanson/graycord
```

## Usage

Variables that can be passed to docker img. 
```python
PASSWORD        - Graylog password
USERNAME        - Graylog username 
HOSTNAME        - Graylog server ip/hostname
TOKEN           - Discord token
CHANNEL         - Discord channel ID
PORT            - Graylog port (ie. 9000)
SEARCH_QUERY    - Graylog Search query. Anything you can search on via graylog UI
INTERVAL        - API call in seconds. Default is 10 
```

## Example 

```bash 

sudo docker run -e PASSWORD="passwordForGrayLog" -e HOSTNAME='ip/hostname for graylog' -e TOKEN='discord-bot-token' docker_img_name

```

## Search Query Examples 

```bash 
Fortigate Logs: 

1. Admin login events       - 'logdesc:"Admin login successful"'
2. View logs rated critical - 'level:\"critical\"'
3.  Multiple different logs  - 'logdesc:"Admin login successful" OR action:\\"tunnel\\-up\\" OR level:\"critical\"'
```

## Get docker here 
https://docs.docker.com/get-docker/

## DockerHub 
[https://hub.docker.com/r/mikehanson/graycord](https://hub.docker.com/r/mikehanson/graycord)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)