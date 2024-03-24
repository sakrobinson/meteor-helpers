   module.exports = {
     apps : [{
       name: 'run_py',
       script: '/usr/bin/python3',
       args: '~/meteor-helpersrun.py',
       instances: 1,
       autorestart: false,
       watch: false,
       max_memory_restart: '1G',
       cron_restart: '0 7 * * *', // This will restart at 7:00 AM every day
       out_file: '/path/to/your/logfile.log',
       error_file: '/path/to/your/errorfile.log',
       merge_logs: true,
       env: {
        TZ: "America/Denver"
       }
     }]
   };