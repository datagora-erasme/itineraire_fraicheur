const { spawn } = require('child_process');
// const fs = require('fs');
// const path = require('path');

async function loadGraph(filePath, picklePath) {
  const pythonProcess = spawn('python', ['load_network.py', filePath, picklePath]);
  let status = '';

  pythonProcess.stdout.on('data', (data) => {
    status = data.toString();
  });

  return new Promise((resolve, reject) => {
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}`));
      } else {
        resolve(status.split("\n")[0])
      }
    });
  });
}

module.exports = {
    loadGraph
}