sleep 10
pm2 start main.py --watch --time --name bot_discord
sleep 5
pm2 monit