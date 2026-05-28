module.exports = {
  apps: [
    {
      name: "seismocluster-backend",
      script: "C:\\seismocluster\\.venv\\Scripts\\uvicorn.exe",
      args: "api.main:app --host 0.0.0.0 --port 8000",
      cwd: "C:\\seismocluster\\backend",
      interpreter: "none",
      watch: false,
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 10,
      env: {
        PYTHONPATH: "C:\\seismocluster\\backend",
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      out_file: "C:\\seismocluster\\logs\\backend-out.log",
      error_file: "C:\\seismocluster\\logs\\backend-error.log",
    },
  ],
};
