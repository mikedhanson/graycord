import requests    # for api calls 
import json        # json 
import argparse
import os          
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time        # for time, dummy 
import datetime    # for time, dummy 
import discord     # For discord bot 
import asyncio     # for muiltithreading 
import socket      # 

global start_time 
start_time = time.time()

### DOCKER PARAMS 
uname = os.getenv('USERNAME', 'admin')
password = os.getenv('PASSWORD')
hostname = os.getenv('HOSTNAME')
port = os.getenv('PORT', '9000')
token = os.getenv('TOKEN')
discord_channel = os.getenv('CHANNEL')
SEARCH_QUERY = os.getenv('SEARCH_QUERY', 'logdesc:"Admin login successful"')
interval = os.getenv('INTERVAL', 10)

# connect to discord client
client = discord.Client()

@client.event
async def on_message(message):
    #guild = message.guild
    if message.content == '!info':
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        await message.channel.send(f'Number of API Calls: {API_Count}')
        await message.channel.send(f'Uptime: {elapsed_time}')
        await message.channel.send(f'Host Name: {socket.gethostname()}')
        await message.channel.send(f'Number of alerts this session: { Alerts_this_session }')

headers = {
    'X-Requested-By': 'cli',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

def ping(hostname):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', hostname]
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(command, stdout=DEVNULL, stderr=DEVNULL)
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False

    return is_up

@client.event
async def parse_logs():
    await client.wait_until_ready()
    channel = client.get_channel(int(discord_channel))  # garylog channel
    global API_Count
    API_Count = 0
    global Alerts_this_session
    Alerts_this_session = 0

    #check_time_zone()
    response = ping(hostname)
    while(response is True):

        curTime = datetime.datetime.now()
        curTime_formated = curTime.strftime("%Y-%m-%d %X")
        last_n_min = curTime - datetime.timedelta(seconds=interval)
        last_n_min_formated = last_n_min.strftime("%Y-%m-%d %X")

        params = (
            ('query', SEARCH_QUERY),
            ('from', last_n_min_formated), #'2020-01-01 00:00:00'
            ('to', curTime_formated),
            ('decorate', 'true'),
        )

        url = "http://" + hostname + ":" + port + "/api/search/universal/absolute"
        data = requests.get(url, headers=headers, params=params, auth=(uname, password)).json()
        API_Count += 1

        if data["total_results"] != 0:
            logs = data["messages"]

            for log in logs:
                #index = logs.index(log)
                if "login" in log['message']['action']:
                    login_msg = {
                        "What": log['message']['logdesc'],
                        "User": log['message']['user'],
                        "Time": log['message']['time'],
                        "Source IP": log['message']['srcip'],
                        "Profile": log['message']['profile'],
                        "Level": log['message']['level'],
                        "log_id": log['message']['_id'],
                        "Device": log['message']['source'],
                    }
                    format_login_msg = '\n'.join([f'{key}: {value}' for key, value in login_msg.items()]) #each item to new line as a string           
                    get_title = log['message']['logdesc']
                    embedVar = discord.Embed(title=get_title, color=0x00ff00)
                    embedVar.add_field(name="Details", value=format_login_msg, inline=False)
                    embedVar.description = "[Click here to view this log?]( http://" + hostname + ":" + port + "/messages/graylog_1/" + login_msg.get('log_id') + ")"
                    await channel.send(embed=embedVar)
                    Alerts_this_session += 1

                if "tunnel-up" in log['message']['action'] :  
                    vpn_msg = { 
                        "What"        : log['message']['logdesc'], 
                        "User"        : log['message']['user'],  
                        "Time"        : log['message']['time'],
                        "Remote IP"   : log['message']['remip'],
                        "Level"       : log['message']['level'],
                        "log_id"      : log['message']['_id'],
                        "Device"      : log['message']['source'], 
                    }
                    formated_vpn_msg = '\n'.join([f'{key}: {value}' for key, value in vpn_msg.items()]) #each item to new line as a string
                    
                    get_title = log['message']['logdesc']

                    embed_val = discord.Embed(title=get_title, color=0x00ff00)
                    embed_val.add_field(name="Details", value=formated_vpn_msg, inline=False)
                    embed_val.description = "[Click here to view this log?]( http://" + hostname + ":" + port + "/messages/graylog_1/" + vpn_msg.get('log_id') + ")"
                    await channel.send(embed=embed_val)
                    Alerts_this_session += 1

                if "critical" in log['message']['action'] :
                    await channel.send(f" Critical Alert: { log['message']['msg'] }")
                    Alerts_this_session += 1

        await asyncio.sleep(interval)
        response = ping(hostname)

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    print("Bot Name:", client.user.name, "User_id:", client.user.id)
    await client.wait_until_ready()
    
    channel = client.get_channel(int(discord_channel))
    await channel.send(f"Bot Running on {socket.gethostname()}")

client.loop.create_task(parse_logs())
client.run(token)
