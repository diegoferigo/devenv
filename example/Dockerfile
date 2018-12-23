ARG from=diegoferigo/devenv:intel
FROM ${from}

RUN apt-get update &&\
    apt-get install -y --no-install-recommends zenity &&\
    rm -rf /var/lib/apt/lists/*

CMD zenity \
        --info \
        --title "X11 forwarding example" \
        --text="Welcome to devenv!" \
        --ok-label "Close"
