SERVER_CONTAINER="server"
sudo docker build . -t $SERVER_CONTAINER
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

sudo docker run -v /home/nikita_khramov/forger/sign-here-detector:/forger/sign-here-detector -v /home/nikita_khramov/forger/signheredetectordataset:/forger/signheredetectordataset -p 5000:5000 --name $SERVER_CONTAINER $SERVER_CONTAINER