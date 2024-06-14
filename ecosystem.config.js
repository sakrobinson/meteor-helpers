module.exports = {
  apps: [{
    name: 'meteor_chron',
    script: '/usr/bin/python3',
    args: 'run.py',
    instances: 1,
    autorestart: false,
    watch: false,
    max_memory_restart: '1G',
    cron_restart: '0 16 * * *', // This will restart at 4:00 PM every day (using 24-hour format)
    out_file: '/path/to/logfile.log', // Path to log file
    error_file: '/path/to/errorfile.log', // Path to error log file
    merge_logs: true,
    env: {
      TZ: 'America/Denver'
    }
  }]
};
