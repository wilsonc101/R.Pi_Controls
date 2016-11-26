DAEMON_1="/usr/local/pi_control/R.Pi_Controls/init/start_in_virtenv.sh"
PIDFILE_1="/var/run/pi_controls.pid"

case "$1" in
  start)
    echo "Starting Pi Controls...."
    /sbin/start-stop-daemon --start --pidfile $PIDFILE_1 -b --make-pidfile --exec $DAEMON_1
    echo "....done"
    ;;

  stop)
    echo "Stopping Pi Controls...."
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE_1
    /usr/bin/pkill -f pi_controls.py
    echo "....done"
    ;;

  restart)
    echo "Stopping Pi Controls...."
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE_1
    /usr/bin/pkill -f pi_controls.py
    echo "....done"

    sleep 2s

    echo "Starting Pi Controls...."
    /sbin/start-stop-daemon --start --pidfile $PIDFILE_1 -b --make-pidfile --exec $DAEMON_1
    echo "....done"
    ;;

  *)
    echo "Usage: /etc/init.d/pi_control {start|stop|restart}"
    exit 1
    ;;

esac

