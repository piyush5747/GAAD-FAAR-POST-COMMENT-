<!DOCTYPE html>
<html>
<head>
    <title>  Facebook Comment Master</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .task-box {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .live-logs {
            height: 400px;
            overflow-y: auto;
            background: #1a1a1a;
            color: #00ff00;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h2 class="text-center mb-4"> Create by piyush  Advanced Facebook Comment System</h2>
        
        <form id="mainForm" enctype="multipart/form-data">
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label class="form-label">JSON Cookies</label>
                        <textarea class="form-control" name="cookies" rows="5" required></textarea>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Post ID</label>
                        <input type="text" class="form-control" name="post_id" required>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="form-label">Name Prefix</label>
                            <input type="text" class="form-control" name="prefix" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Name Suffix</label>
                            <input type="text" class="form-control" name="suffix" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Comments File</label>
                        <input type="file" class="form-control" name="comments_file" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Delay (Seconds)</label>
                        <input type="number" class="form-control" name="delay" value="10" min="5" required>
                    </div>
                </div>
            </div>
            
            <button type="submit" class="btn btn-success w-100">Start Commenting</button>
        </form>

        <div class="mt-4">
            <h4>Active Tasks</h4>
            <div id="tasksContainer"></div>
        </div>

        <div class="mt-4">
            <h4>Live Monitoring</h4>
            <div class="live-logs" id="liveLogs"></div>
        </div>
    </div>

    <script>
        const form = document.getElementById('mainForm');
        const tasksContainer = document.getElementById('tasksContainer');
        const liveLogs = document.getElementById('liveLogs');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            
            try {
                const response = await fetch('/start', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                if(result.task_id) {
                    startTaskMonitoring(result.task_id);
                }
            } catch(error) {
                alert('Error: ' + error.message);
            }
        });

        function startTaskMonitoring(taskId) {
            const taskBox = document.createElement('div');
            taskBox.className = 'task-box';
            taskBox.innerHTML = `
                <h5>Task ID: ${taskId}</h5>
                <div id="stats-${taskId}">Loading...</div>
                <button onclick="stopTask('${taskId}')" class="btn btn-danger btn-sm">Stop</button>
                <hr>
            `;
            tasksContainer.prepend(taskBox);
            
            // Start polling for updates
            setInterval(async () => {
                const response = await fetch(`/status/${taskId}`);
                const data = await response.json();
                
                if(data.status) {
                    document.getElementById(`stats-${taskId}`).innerHTML = `
                        Status: ${data.status}<br>
                        Success: ${data.success || 0}<br>
                        Failed: ${data.failed || 0}<br>
                        Total Cookies: ${data.cookies_used || 0}
                    `;
                }
                
                // Update logs
                const logsResponse = await fetch(`/logs/${taskId}`);
                const logs = await logsResponse.json();
                liveLogs.innerHTML = logs.join('<br>');
                liveLogs.scrollTop = liveLogs.scrollHeight;
            }, 2000);
        }

        function stopTask(taskId) {
            fetch(`/stop/${taskId}`);
        }
    </script>
</body>
</html>