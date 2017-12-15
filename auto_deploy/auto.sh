python add.py
sleep 2 
python $1 $2 $3:$4 > $4 &
sleep 2
python dicover.py
sleep 2 
python edit_loc.py
sleep 2
python map.py
sleep 2
python deploy.py

