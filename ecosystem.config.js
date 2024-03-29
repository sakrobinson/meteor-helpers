   module.exports = {
     apps : [{
       name: 'meteor_chron',
       script: '/usr/bin/python3',
       args: 'run.py',
       instances: 1,
       autorestart: false,
       watch: false,
       max_memory_restart: '1G',
       cron_restart: '0 1 * * *', // This will restart at 1:00 PM every day
       out_file: '/path/to/logfile.log', // Need to add logging
       error_file: '/path/to/errorfile.log', // Need to add logging
       merge_logs: true,
       env: {
        TZ: "America/Denver"
       }
     }]
   };