#!/bin/bash
echo "999999" > minimum.txt
while true; 
do
    echo "0" > counter.txt
    echo "Start loop"
    for i in $(seq 0.5 0.5 $1)
    do
        sleep=$i
        if [ $(curl -X POST --write-out %{http_code} --silent --output /dev/null -d "{\"sleep\" : $sleep}" "localhost:8080/sleep" ) -eq "200"  ] ; then echo $(($(<counter.txt)+1)) >counter.txt; fi &
    done 
    #wait
    globalsleep=$(($1+1))
    sleep $globalsleep
    count=$(<counter.txt)
    minimum=$(<minimum.txt)
    if [ "$count" -lt "$minimum" ] ; then
        echo "$count" >minimum.txt;
    fi

    minimum=$(<minimum.txt)
    echo "Success : $count"
    echo "Minimum : $minimum"
done
