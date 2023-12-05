SERVER_CONTAINER="server"
cd /home/nikita_khramov/forger
sudo docker build . -f /home/nikita_khramov/forger/forgeserver/Dockerfile -t $SERVER_CONTAINER
PWD=$(pwd)

if [ "$(sudo docker ps -a -q -f name=$SERVER_CONTAINER)" ]; then
    if [ "$(sudo docker ps -aq -f status=running -f name=$SERVER_CONTAINER)" ]; then
        sudo docker stop $SERVER_CONTAINER
    fi

    if [ "$(sudo docker ps -aq -f status=restarting -f name=$SERVER_CONTAINER)" ]; then
        sudo docker stop $SERVER_CONTAINER
    fi

    sudo docker rm -f $SERVER_CONTAINER
fi

sudo docker run --gpus all -d -v /home/nikita_khramov/forger/checkpoints:/root/forger/checkpoints -v /home/nikita_khramov/forger/signheredetector:/root/forger/signheredetector -v /home/nikita_khramov/forger/signheredetectordataset:/root/forger/signheredetectordataset -p 5000:5000 --name $SERVER_CONTAINER --restart unless-stopped $SERVER_CONTAINER
sudo docker exec $SERVER_CONTAINER wandb login 41acefe7cea08aefe86fe2e5748565b8dda71b4a
sudo docker logs $SERVER_CONTAINER