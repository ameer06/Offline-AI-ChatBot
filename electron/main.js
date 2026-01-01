/**
 * Electron Main Process
 * Handles window creation, backend process management, and system integration
 */

const { app, BrowserWindow, ipcMain, Menu, Tray } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;
let tray;

// Backend server configuration
const BACKEND_PORT = 5000;
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`;

/**
 * Create the main application window
 */
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 800,
        minHeight: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        icon: path.join(__dirname, '../build/icon.ico'),
        show: false // Don't show until ready
    });

    // Load the frontend
    mainWindow.loadFile(path.join(__dirname, '../frontend/index.html'));

    // Show window when ready
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Handle window close
    mainWindow.on('close', (event) => {
        if (!app.isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
        return false;
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

/**
 * Start the Python Flask backend server
 */
function startBackend() {
    console.log('Starting Flask backend...');

    const pythonPath = 'python'; // Use 'python3' on macOS/Linux if needed
    const scriptPath = path.join(__dirname, '../backend/app.py');

    backendProcess = spawn(pythonPath, [scriptPath], {
        cwd: path.join(__dirname, '../backend')
    });

    backendProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
    });

    backendProcess.on('close', (code) => {
        console.log(`Backend process exited with code ${code}`);
    });

    // Wait for backend to start
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('Backend should be ready');
            resolve();
        }, 3000); // Wait 3 seconds for backend to start
    });
}

/**
 * Stop the backend server
 */
function stopBackend() {
    if (backendProcess) {
        console.log('Stopping backend...');
        backendProcess.kill();
        backendProcess = null;
    }
}

/**
 * Create system tray icon
 */
function createTray() {
    // You can add a tray icon here if you have one
    // tray = new Tray(path.join(__dirname, '../build/tray-icon.png'));

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Show App',
            click: () => {
                mainWindow.show();
            }
        },
        {
            label: 'Quit',
            click: () => {
                app.isQuitting = true;
                app.quit();
            }
        }
    ]);

    // tray.setContextMenu(contextMenu);
    // tray.setToolTip('Local AI Chatbot');
}

/**
 * IPC Handlers for communication with renderer process
 */

// Get available models from Ollama
ipcMain.handle('get-models', async () => {
    try {
        const axios = require('axios');
        const response = await axios.get(`${BACKEND_URL}/api/models`);
        return response.data;
    } catch (error) {
        console.error('Error fetching models:', error);
        return { error: error.message };
    }
});

// Set active model
ipcMain.handle('set-model', async (event, modelName) => {
    try {
        const axios = require('axios');
        const response = await axios.post(`${BACKEND_URL}/api/models/active`, {
            model: modelName
        });
        return response.data;
    } catch (error) {
        console.error('Error setting model:', error);
        return { error: error.message };
    }
});

// Download a new model
ipcMain.handle('download-model', async (event, modelName) => {
    try {
        const axios = require('axios');
        const response = await axios.post(`${BACKEND_URL}/api/models/download`, {
            model: modelName
        });
        return response.data;
    } catch (error) {
        console.error('Error downloading model:', error);
        return { error: error.message };
    }
});

/**
 * App lifecycle events
 */

app.whenReady().then(async () => {
    // Start backend first
    await startBackend();

    // Then create window
    createWindow();

    // Create tray
    createTray();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    // Don't quit on window close for macOS
    if (process.platform !== 'darwin') {
        stopBackend();
        app.quit();
    }
});

app.on('before-quit', () => {
    app.isQuitting = true;
    stopBackend();
});

app.on('quit', () => {
    stopBackend();
});

// Handle any unhandled errors
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});
